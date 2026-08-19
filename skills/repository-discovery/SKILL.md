---
name: repository-discovery
description: Systematically discovers a repository's architecture, conventions, execution paths, validation commands, ownership boundaries, and agent guidance before planning or modifying code. Use when entering an unfamiliar codebase, when a request spans multiple areas, or when implementation risk depends on understanding repository structure first.
license: Apache-2.0
compatibility: Works in Agent Skills hosts that can read repository files and version-control metadata.
metadata:
  maturity: stable
  risk: R0
  category: understand
  network: "false"
  side-effects: none
---

# Repository Discovery

## Purpose

Build a compact evidence-backed map of an unfamiliar repository before proposing changes. Prefer repository evidence over assumptions and stop discovery when additional reading no longer changes the implementation boundary.

## Workflow

1. **Establish repository shape**
   - Identify languages, package managers, build systems, workspace/monorepo boundaries, generated code, infrastructure, and deployment entry points.
   - Read root guidance such as `README`, `AGENTS.md`, `CLAUDE.md`, contribution docs, and tool-specific rules.
2. **Find execution paths**
   - Locate application/library entry points, public APIs, CLI commands, background jobs, tests, and build/release workflows relevant to the request.
3. **Map conventions**
   - Identify formatting, linting, testing, dependency, migration, and documentation conventions from configuration and existing examples.
4. **Map ownership and boundaries**
   - Identify modules that should remain independent, shared interfaces, generated/vendor directories, and files that should not be hand-edited.
5. **Identify validation commands**
   - Extract the smallest repository-native commands that can validate a future change.
6. **Report evidence and unknowns**
   - Summarize relevant paths and facts, distinguish assumptions from evidence, and list unresolved questions only when they materially affect the task.

## Required behavior

- Read repository guidance before recommending implementation.
- Cite concrete files/paths for architectural claims.
- Prefer targeted discovery to indiscriminate full-repository reading.
- Distinguish verified facts, inferences, and unknowns.
- End with the likely change surface and validation surface when discovery is being used to prepare implementation.

## Do not

- Modify repository files.
- Install dependencies or run destructive commands.
- Assume a framework or deployment model from file names alone.
- Produce a large architecture inventory unrelated to the requested task.

## Success criteria

The next agent or human can start planning with a reliable map of the relevant code, constraints, conventions, and validation commands without rediscovering the repository from scratch.
