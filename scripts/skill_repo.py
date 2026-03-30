#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys

from skilllib.system import (
    REPO_ROOT,
    classify_query,
    sync_global_instructions,
    validate_repository,
    write_index,
)


def _run_tests() -> None:
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"],
        cwd=REPO_ROOT,
        check=True,
    )


def _print_validation(errors: list[str]) -> int:
    if not errors:
        print("validation: ok")
        return 0

    print("validation: failed")
    for error in errors:
        print(f"- {error}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage the Copilot skills repository.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate", help="Validate the skills registry and managed instructions.")
    subparsers.add_parser("build-index", help="Regenerate the skills registry index.")
    subparsers.add_parser("sync", help="Sync the managed routing block into global instructions.")
    subparsers.add_parser("ci", help="Sync instructions, rebuild the index, validate, and run tests.")

    classify_parser = subparsers.add_parser("classify", help="Show the layered routing decision for a query.")
    classify_parser.add_argument("query", nargs="+", help="The query to classify.")

    args = parser.parse_args()

    if args.command == "validate":
        return _print_validation(validate_repository())

    if args.command == "build-index":
        index_path = write_index()
        print(f"index: updated {index_path}")
        return 0

    if args.command == "sync":
        changed = sync_global_instructions()
        print("sync: updated global instructions" if changed else "sync: no changes")
        return 0

    if args.command == "classify":
        decision = classify_query(" ".join(args.query))
        print(f"knowledge: {', '.join(decision.knowledge_skills) or '-'}")
        print(f"overlays: {', '.join(decision.overlay_skills) or '-'}")
        print(f"primary: {decision.primary_skill or '-'}")
        return 0

    if args.command == "ci":
        sync_global_instructions()
        write_index()

        errors = validate_repository()
        exit_code = _print_validation(errors)
        if exit_code:
            return exit_code

        _run_tests()
        print("ci: ok")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())