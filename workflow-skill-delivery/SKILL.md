---
name: workflow-skill-delivery
description: 'Validated publish workflow for the Copilot skills repo. Use for syncing instructions, rebuilding the registry, running the full suite, and committing or pushing only after verification. Triggers on: validate skill repo, sync instructions, publish skills, commit skills, push skill repo, verify all tests, ci/cd.'
argument-hint: 'Describe the delivery action, for example: "publish skill updates", "sync routing block", or "commit and push the skills repo".'
---

# Workflow Skill Delivery

## Purpose

Gate all skill-system publication behind validation and a full green test run.

## Delivery Sequence

1. Sync managed instructions:
   - Update the managed routing block in the global Copilot instructions.
2. Refresh generated artifacts:
   - Rebuild `_index.md` from the discovered skills.
3. Validate the repo:
   - Check the registry, required layered skills, and managed markers.
4. Run the full suite:
   - Run all skill-system tests, not just the focused test.
5. Publish only if green:
   - Commit only after validation and all tests pass.
   - Push only if a remote is configured.

## Hard Rules

- Validation and tests are mandatory before commit.
- Generated files are updated before commit, not after.
- Push failures should leave a clean local commit and a clear message.
- The delivery path should be scriptable so the same gate runs for humans and automation.