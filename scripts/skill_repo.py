#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from skilllib.system import (
    ROUTING_BENCHMARKS_PATH,
    ROUTING_LOG_PATH,
    classify_query,
    load_routing_benchmarks,
    read_routing_events,
    record_routing_event,
    render_global_instructions,
    run_routing_benchmarks,
    summarize_routing_metrics,
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
    subparsers.add_parser("metrics", help="Summarize routing telemetry metrics.")
    subparsers.add_parser("benchmark", help="Run the routing benchmark suite.")
    subparsers.add_parser("render-global", help="Print the generated global instructions file.")

    classify_parser = subparsers.add_parser("classify", help="Show the layered routing decision for a query.")
    classify_parser.add_argument("--no-log", action="store_true", help="Do not append the routing decision to telemetry.")
    classify_parser.add_argument("query", nargs="+", help="The query to classify.")

    trace_parser = subparsers.add_parser("trace", help="Show recent routing telemetry events.")
    trace_parser.add_argument("--limit", type=int, default=10, help="How many recent events to show.")

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

    if args.command == "render-global":
        print(render_global_instructions(), end="")
        return 0

    if args.command == "classify":
        query = " ".join(args.query)
        decision = classify_query(query)
        if not args.no_log:
            record_routing_event(query, decision, log_path=ROUTING_LOG_PATH, source="classify")
        print(f"knowledge: {', '.join(decision.knowledge_skills) or '-'}")
        print(f"overlays: {', '.join(decision.overlay_skills) or '-'}")
        print(f"primary: {decision.primary_skill or '-'}")
        print(f"confidence: {decision.confidence:.3f}")
        print(f"fallback: {decision.fallback_reason or '-'}")
        return 0

    if args.command == "trace":
        events = read_routing_events(limit=args.limit)
        if not events:
            print(f"trace: no events found at {ROUTING_LOG_PATH}")
            return 0

        for event in events:
            selected = ", ".join(event.get("selected_skills", [])) or "-"
            print(
                f"{event['timestamp']} | query={event['query']} | selected={selected} | confidence={float(event.get('confidence', 0.0)):.3f} | fallback={event.get('fallback_reason') or '-'}"
            )
        return 0

    if args.command == "metrics":
        metrics = summarize_routing_metrics(log_path=ROUTING_LOG_PATH)
        print(f"log_path: {metrics['log_path']}")
        print(f"total_queries: {metrics['total_queries']}")
        print(f"matched_queries: {metrics['matched_queries']}")
        print(f"fallback_queries: {metrics['fallback_queries']}")
        print(f"match_rate: {metrics['match_rate']:.3f}")
        print(f"fallback_rate: {metrics['fallback_rate']:.3f}")
        print(f"average_selected_skill_count: {metrics['average_selected_skill_count']:.3f}")
        print(f"knowledge_activation_rate: {metrics['knowledge_activation_rate']:.3f}")
        print(f"low_confidence_rate: {metrics['low_confidence_rate']:.3f}")
        print(f"primary_skill_counts: {metrics['primary_skill_counts']}")
        print(f"overlay_skill_counts: {metrics['overlay_skill_counts']}")
        print(f"fallback_reasons: {metrics['fallback_reasons']}")
        print(f"recent_fallback_queries: {metrics['recent_fallback_queries']}")
        return 0

    if args.command == "benchmark":
        result = run_routing_benchmarks(load_routing_benchmarks(ROUTING_BENCHMARKS_PATH))
        print(f"benchmarks: {len(result.cases)} case(s)")
        if result.failures:
            print(f"status: failed ({len(result.failures)} failure(s))")
            for failure in result.failures:
                print(f"- {failure['name']}: expected {failure['expected']} but got {failure['actual']}")
            return 1

        print("status: ok")
        return 0

    if args.command == "ci":
        sync_global_instructions()
        write_index()

        errors = validate_repository()
        exit_code = _print_validation(errors)
        if exit_code:
            return exit_code

        benchmark_result = run_routing_benchmarks(load_routing_benchmarks(ROUTING_BENCHMARKS_PATH))
        if benchmark_result.failures:
            print("benchmarks: failed")
            for failure in benchmark_result.failures:
                print(f"- {failure['name']}: expected {failure['expected']} but got {failure['actual']}")
            return 1

        _run_tests()
        print("ci: ok")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())