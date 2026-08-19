# Skill evaluation harness

This directory defines routing and behavior fixtures for every canonical skill. The repository deliberately separates deterministic quality checks from nondeterministic agent behavior.

## What CI validates

`python scripts/validate_skill_contracts.py` checks that every skill has:

- at least two positive routing prompts;
- at least two negative routing prompts;
- required behavior assertions;
- prohibited behavior assertions;
- complete capability/risk metadata.

This is fixture and contract coverage. It does **not** prove that a particular agent/model routes or behaves correctly.

## Recording host/model observations

Run the fixtures through the host/model/version you want to evaluate and save observations as a JSON array. Each item uses this shape:

```json
{
  "skill": "ci-failure-triage",
  "case_id": "p1",
  "selected": true,
  "observed_steps": ["identify-failing-command", "reproduce-or-state-limitation"],
  "observed_actions": []
}
```

For a negative routing case, set `selected` to whether the host actually selected/invoked the skill. `observed_steps` and `observed_actions` are only scored for positive cases that selected the skill.

Score an observation file with:

```bash
python scripts/score_skill_observations.py path/to/observations.json
```

The scorer reports routing precision/recall plus required/prohibited behavior assertion coverage. Keep the agent host, agent version, model/version, repository fixture, and commit SHA beside published results.

## Evidence policy

Behavioral results are evidence for the exact evaluated environment, not certification and not a guarantee for future model/host versions. Do not publish a generic `verified: true` flag from these results.
