from __future__ import annotations

import argparse

from agents.orchestrator_agent import run_agent_request
from agents.schemas import AgentRequest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the V3.3 lightweight Router Agent / Orchestrator."
    )
    parser.add_argument(
        "--question",
        required=True,
        help="User question for the lightweight agent.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute whitelisted workflow actions. Defaults to dry-run.",
    )
    parser.add_argument(
        "--provider",
        choices=["mock", "siliconflow"],
        default="mock",
        help="Provider requested for workflow execution. V3.3 execution only allows mock.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    request = AgentRequest(
        question=args.question,
        dry_run=not args.execute,
        provider=args.provider,
    )
    result = run_agent_request(request)

    print("Intent:")
    print(result.intent)
    print("")
    print("Selected tools:")
    if result.selected_tools:
        for tool in result.selected_tools:
            print(f"- {tool}")
    else:
        print("- None")
    print("")
    print("Risk level:")
    print(result.risk_level)
    print("")
    print("Dry run:")
    print(result.dry_run)
    print("")
    print("Final answer:")
    print(result.final_answer)
    print("")
    print("Trace path:")
    print(result.trace_path)


if __name__ == "__main__":
    main()
