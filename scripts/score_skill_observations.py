#!/usr/bin/env python3
"""Score host/model observations against repository routing and behavior fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from skilllib import ROOT


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("observations", type=Path, help="JSON array of recorded agent observations")
    args = parser.parse_args()

    manifest = json.loads((ROOT / "evals" / "manifest.json").read_text(encoding="utf-8"))
    cases: dict[tuple[str, str], dict[str, object]] = {}
    behavior: dict[str, dict[str, list[str]]] = {}
    for entry in manifest["skills"]:
        name = entry["name"]
        behavior[name] = entry["behavior"]
        for expected, polarity in ((True, "positive"), (False, "negative")):
            for case in entry["routing"][polarity]:
                cases[(name, case["id"])] = {"expected_selected": expected, **case}

    observations = json.loads(args.observations.read_text(encoding="utf-8"))
    tp = fp = tn = fn = 0
    behavior_pass = behavior_total = 0
    failures: list[str] = []

    for observation in observations:
        key = (observation["skill"], observation["case_id"])
        if key not in cases:
            failures.append(f"unknown case: {key[0]}/{key[1]}")
            continue
        expected = bool(cases[key]["expected_selected"])
        actual = bool(observation["selected"])
        if expected and actual:
            tp += 1
        elif expected and not actual:
            fn += 1
        elif not expected and actual:
            fp += 1
        else:
            tn += 1

        if expected and actual:
            observed_steps = set(observation.get("observed_steps", []))
            observed_actions = set(observation.get("observed_actions", []))
            for required in behavior[key[0]]["required"]:
                behavior_total += 1
                if required in observed_steps:
                    behavior_pass += 1
                else:
                    failures.append(f"{key[0]}/{key[1]} missing required step: {required}")
            for prohibited in behavior[key[0]]["prohibited"]:
                behavior_total += 1
                if prohibited not in observed_actions:
                    behavior_pass += 1
                else:
                    failures.append(f"{key[0]}/{key[1]} performed prohibited action: {prohibited}")

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    behavior_rate = behavior_pass / behavior_total if behavior_total else 0.0
    report = {
        "routing": {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "precision": round(precision, 4), "recall": round(recall, 4)},
        "behavior": {"passed_assertions": behavior_pass, "total_assertions": behavior_total, "pass_rate": round(behavior_rate, 4)},
        "failures": failures,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
