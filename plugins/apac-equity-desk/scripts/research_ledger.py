"""Append an explicit observation to a portable research-thesis ledger."""

from __future__ import annotations

import argparse
from copy import deepcopy
from typing import Any

from common import iso_now, load_data, write_output


STATES = {"strengthened", "weakened", "falsified", "unchanged"}


def update_ledger(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict) or not isinstance(data.get("ledger"), dict) or not isinstance(data.get("observation"), dict):
        raise ValueError("Input requires ledger and observation objects.")
    ledger = deepcopy(data["ledger"])
    observation = deepcopy(data["observation"])
    thesis_id = str(observation.get("thesis_id", "")).strip()
    verdict = str(observation.get("verdict", "")).strip()
    if not thesis_id or verdict not in STATES:
        raise ValueError(f"observation requires thesis_id and verdict in {sorted(STATES)}")
    theses = ledger.setdefault("theses", [])
    thesis = next((item for item in theses if str(item.get("id")) == thesis_id), None)
    if thesis is None:
        raise ValueError(f"Unknown thesis_id: {thesis_id}")
    if not observation.get("observed_at"):
        observation["observed_at"] = iso_now()
    history = thesis.setdefault("history", [])
    history.append(observation)
    thesis["status"] = verdict
    thesis["updated_at"] = observation["observed_at"]
    if verdict == "falsified" and not observation.get("reason"):
        raise ValueError("A falsified verdict requires a reason.")
    ledger["updated_at"] = observation["observed_at"]
    return ledger


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input")
    cli.add_argument("--output", required=True, help="Explicit destination; the helper never stores hidden memory")
    args = cli.parse_args()
    write_output(update_ledger(load_data(args.input)), args.output)
