---
name: workflow-tdd
description: 'Test-first engineering workflow for implementation and issue handling. Use for building features, fixing bugs, handling regressions, or reproducing issues before changing code. Triggers on: implement, build feature, issue, bug fix, regression, failing test, test first, tdd.'
argument-hint: 'Describe the implementation or issue to handle, for example: "fix regression in auth", "implement API endpoint", or "reproduce and fix failing test".'
---

# Workflow TDD

## Purpose

Apply a strict test-first loop to implementation and bug-fix tasks.

## Mandatory Loop

1. Reproduce first:
   - If an issue is reported, add or update a focused test that demonstrates the current failure.
   - If no test exists, create the narrowest failing test that captures the expected behavior.
2. Implement second:
   - Make the smallest code change that turns the focused test green.
3. Verify third:
   - Run the focused test again.
   - Run the relevant broader suite to catch regressions.
4. Update process artifacts last:
   - Only update instructions, skills, or automation after the implementation and verification loop is green.

## Hard Rules

- No implementation without a failing test or an explicit reason the behavior cannot be tested.
- No commit while tests are red.
- When an issue changes expected behavior, the test case changes before the code change.
- Keep the first failing test small so debugging cost stays low.