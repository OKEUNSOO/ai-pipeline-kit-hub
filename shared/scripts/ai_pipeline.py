#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_OUTPUTS = [
    "00_data_contract.md",
    "01_dataset_profile.md",
    "02_analysis_plan.md",
    "02_eda_report.md",
    "03_problem_definition.md",
    "04_kpi_summary.md",
    "04_metrics.json",
    "05_analysis.py",
    "05_analysis.ipynb",
    "05_analysis_report.md",
    "06_dashboard.html",
    "07_executive_report.md",
    "08_validation_report.md",
]
WORKFLOW_STEPS = [
    {"no": 1, "step": "Data Contract & Profile", "outputs": ["00_data_contract.md", "01_dataset_profile.md"]},
    {"no": 2, "step": "Analysis Plan & EDA", "outputs": ["02_analysis_plan.md", "02_eda_report.md"]},
    {"no": 3, "step": "Problem Definition", "outputs": ["03_problem_definition.md"]},
    {"no": 4, "step": "KPI Summary & Metrics JSON", "outputs": ["04_kpi_summary.md", "04_metrics.json"]},
    {"no": 5, "step": "Reproducible Notebook & Analysis", "outputs": ["05_analysis.py", "05_analysis.ipynb", "05_analysis_report.md"]},
    {"no": 6, "step": "Dashboard HTML", "outputs": ["06_dashboard.html"]},
    {"no": 7, "step": "Executive & Validation Reports", "outputs": ["07_executive_report.md", "08_validation_report.md"]},
]


def runtime_root() -> Path:
    override = os.environ.get("AI_PIPELINE_RUNTIME_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / "Documents" / "data-ai-pipeline"


def runs_dir() -> Path:
    return runtime_root() / "runs"


def latest_run_id_path() -> Path:
    return runtime_root() / ".latest_run_id"


def ensure_dirs() -> dict[str, str]:
    runs_dir().mkdir(parents=True, exist_ok=True)
    return {
        "runtime_root": str(runtime_root()),
        "runs_dir": str(runs_dir()),
        "latest_run_id_file": str(latest_run_id_path()),
    }


def emit(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload.get("success", True) else 1


def new_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{stamp}_{uuid.uuid4().hex[:8]}"


def read_latest_run_id() -> str | None:
    if not latest_run_id_path().exists():
        return None
    run_id = latest_run_id_path().read_text(encoding="utf-8").strip()
    return run_id or None


def write_latest_run_id(run_id: str) -> None:
    latest_run_id_path().parent.mkdir(parents=True, exist_ok=True)
    latest_run_id_path().write_text(run_id, encoding="utf-8")


def resolve_run_id(run_id: str | None = None) -> str | None:
    return run_id or read_latest_run_id()


def run_dir(run_id: str | None = None) -> Path:
    resolved = resolve_run_id(run_id)
    if not resolved:
        raise FileNotFoundError("no ai-pipeline run exists yet; create a run first")
    return runs_dir() / resolved


def output_dir(run_id: str | None = None) -> Path:
    return run_dir(run_id) / "outputs"


def step_outputs(step: dict[str, Any]) -> list[str]:
    outputs = step.get("outputs")
    if isinstance(outputs, list):
        return [str(item) for item in outputs]
    output = step.get("output")
    return [str(output)] if output else []


def step_output_label(step: dict[str, Any]) -> str:
    return ", ".join(step_outputs(step))


def workflow_step_record(step: dict[str, Any], status: str, output_root: Path | None = None) -> dict[str, Any]:
    outputs = step_outputs(step)
    record = {**step, "output": step_output_label(step), "outputs": outputs, "status": status}
    if output_root is None:
        record["path"] = None
        record["paths"] = []
        return record
    paths = [str(output_root / name) for name in outputs]
    record["paths"] = paths
    record["path"] = paths[0] if len(paths) == 1 else None
    return record


def run_json_path(run_id: str | None = None) -> Path:
    return run_dir(run_id) / "run.json"


def progress_path(run_id: str | None = None) -> Path:
    return run_dir(run_id) / "progress.json"


def source_metadata(path: str) -> dict[str, Any]:
    src = Path(path).expanduser().resolve()
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(f"source file not found: {src}")
    stat = src.stat()
    return {
        "path": str(src),
        "name": src.name,
        "size": stat.st_size,
        "mtime": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
    }


def normalize_source_paths(paths: Sequence[str] | str | None) -> list[str]:
    if paths is None:
        return []
    if isinstance(paths, str):
        return [paths]
    return [str(path) for path in paths if str(path).strip()]


def read_run(run_id: str | None = None) -> dict[str, Any]:
    path = run_json_path(run_id)
    if not path.exists():
        raise FileNotFoundError(f"run metadata not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_run(payload: dict[str, Any], run_id: str | None = None) -> dict[str, Any]:
    path = run_json_path(run_id or str(payload["run_id"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def create_run(run_id: str | None = None, source_paths: Sequence[str] | str | None = None) -> dict[str, Any]:
    ensure_dirs()
    resolved = run_id or new_run_id()
    out = runs_dir() / resolved / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    sources = [source_metadata(path) for path in normalize_source_paths(source_paths)]
    now = datetime.now(timezone.utc).isoformat()
    payload: dict[str, Any] = {
        "run_id": resolved,
        "status": "pending",
        "created_at": now,
        "updated_at": now,
        "pipeline_version": "analyst-v2",
        "expected_outputs": EXPECTED_OUTPUTS,
        "source_files": sources,
        "run_dir": str(runs_dir() / resolved),
        "output_dir": str(out),
    }
    write_run(payload, resolved)
    write_latest_run_id(resolved)
    write_progress(status="pending", current_step=0, run_id=resolved)
    return {
        "run_id": resolved,
        "run_dir": str(runs_dir() / resolved),
        "run_json": str(run_json_path(resolved)),
        "progress_file": str(progress_path(resolved)),
        "output_dir": str(out),
        "source_files": sources,
        **ensure_dirs(),
    }


def add_input(path: str, run_id: str | None = None) -> dict[str, Any]:
    ensure_dirs()
    resolved = resolve_run_id(run_id)
    if not resolved:
        return create_run(source_paths=[path])
    payload = read_run(resolved)
    meta = source_metadata(path)
    sources = list(payload.get("source_files") or [])
    sources = [item for item in sources if not (isinstance(item, dict) and item.get("path") == meta["path"])]
    sources.append(meta)
    payload["source_files"] = sources
    write_run(payload, resolved)
    write_latest_run_id(resolved)
    return {"run_id": resolved, "source": meta, "run_json": str(run_json_path(resolved)), "output_dir": str(output_dir(resolved))}


def list_sources(run_id: str | None = None) -> list[dict[str, Any]]:
    resolved = resolve_run_id(run_id)
    if not resolved:
        return []
    try:
        payload = read_run(resolved)
    except FileNotFoundError:
        return []
    return [item for item in payload.get("source_files", []) if isinstance(item, dict)]


def list_outputs(run_id: str | None = None) -> list[dict[str, Any]]:
    try:
        target = output_dir(run_id)
    except FileNotFoundError:
        return []
    if not target.exists():
        return []
    return [
        {"name": path.name, "path": str(path), "size": path.stat().st_size}
        for path in sorted(target.iterdir())
        if path.is_file() and path.name != ".DS_Store"
    ]


def safe_output_path(name: str, run_id: str | None = None) -> Path:
    ensure_dirs()
    output = output_dir(run_id).resolve()
    output.mkdir(parents=True, exist_ok=True)
    path = (output / name).resolve()
    if output not in path.parents and path != output:
        raise ValueError("output path escapes output directory")
    return path


def status_from_outputs(output_names: Sequence[str], progress_status: str | None = None, run_id: str | None = None) -> str:
    if progress_status in {"running", "failed"}:
        return progress_status
    try:
        target = output_dir(run_id)
    except FileNotFoundError:
        return progress_status or "pending"
    exists = [(target / name).exists() for name in output_names]
    if exists and all(exists):
        return "done"
    if any(exists):
        return "partial"
    return progress_status or "pending"


def workflow_status(run_id: str | None = None) -> dict[str, Any]:
    ensure_dirs()
    resolved = resolve_run_id(run_id)
    if not resolved:
        return {
            "run_id": None,
            "run_dir": None,
            "output_dir": None,
            "progress_file": None,
            "status": "pending",
            "current_step": 0,
            "total_steps": len(WORKFLOW_STEPS),
            "done": 0,
            "source_files": [],
            "steps": [workflow_step_record(step, "pending") for step in WORKFLOW_STEPS],
        }

    raw_progress: dict[str, Any] = {}
    progress_file = progress_path(resolved)
    if progress_file.exists():
        try:
            raw_progress = json.loads(progress_file.read_text(encoding="utf-8"))
        except Exception:
            raw_progress = {"status": "unknown", "error": "invalid progress.json"}
    progress_by_step = {
        int(step.get("no")): str(step.get("status"))
        for step in raw_progress.get("steps", [])
        if isinstance(step, dict) and step.get("no") is not None
    }
    steps = []
    for step in WORKFLOW_STEPS:
        status_value = status_from_outputs(step_outputs(step), progress_by_step.get(int(step["no"])), resolved)
        steps.append(workflow_step_record(step, status_value, output_dir(resolved)))
    done = sum(1 for step in steps if step["status"] == "done")
    failed = sum(1 for step in steps if step["status"] == "failed")
    running = sum(1 for step in steps if step["status"] == "running")
    overall = "failed" if failed else "running" if running else "complete" if done == len(steps) else "pending"
    return {
        "run_id": resolved,
        "run_dir": str(run_dir(resolved)),
        "output_dir": str(output_dir(resolved)),
        "progress_file": str(progress_file),
        "run_json": str(run_json_path(resolved)),
        "status": overall,
        "current_step": int(raw_progress.get("current_step") or 0) if isinstance(raw_progress, dict) else 0,
        "total_steps": len(WORKFLOW_STEPS),
        "done": done,
        "source_files": list_sources(resolved),
        "steps": steps,
    }


def write_progress(
    status: str,
    current_step: int = 0,
    run_id: str | None = None,
    failed_step: int | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    ensure_dirs()
    resolved = resolve_run_id(run_id)
    if not resolved:
        created = create_run()
        resolved = str(created["run_id"])
    out = output_dir(resolved)
    out.mkdir(parents=True, exist_ok=True)
    steps = []
    for step in WORKFLOW_STEPS:
        number = int(step["no"])
        outputs = step_outputs(step)
        existing = [(out / name).exists() for name in outputs]
        if failed_step == number:
            step_status = "failed"
        elif status == "complete" or (current_step and number < current_step):
            step_status = "done"
        elif current_step == number and status == "running":
            step_status = "running"
        elif existing and all(existing):
            step_status = "done"
        elif any(existing):
            step_status = "partial"
        else:
            step_status = "pending"
        steps.append(workflow_step_record(step, step_status, out))
    payload: dict[str, Any] = {
        "run_id": resolved,
        "status": status,
        "current_step": current_step,
        "total_steps": len(WORKFLOW_STEPS),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "steps": steps,
    }
    if error:
        payload["error"] = error
    progress_path(resolved).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        run_payload = read_run(resolved)
        run_payload["status"] = status
        if error:
            run_payload["error"] = error
        write_run(run_payload, resolved)
    except Exception:
        pass
    return payload


def render_workflow_table(workflow: dict[str, Any] | None = None) -> str:
    current = workflow or workflow_status()
    lines = [
        "AI Pipeline Workflow Status",
        "",
        f"Run ID: {current.get('run_id') or '-'}",
        f"Output: {current.get('output_dir') or '-'}",
        f"Status: {current.get('status')} ({current.get('done', 0)}/{current.get('total_steps', len(WORKFLOW_STEPS))})",
        "",
        "No | Step | Outputs | Status",
        "---|------|---------|--------",
    ]
    for step in current.get("steps", []):
        lines.append(f"{step.get('no')} | {step.get('step')} | {step.get('output')} | {step.get('status')}")
    return "\n".join(lines)


def validate_outputs(run_id: str | None = None) -> dict[str, Any]:
    ensure_dirs()
    resolved = resolve_run_id(run_id)
    if not resolved:
        return {
            "run_id": None,
            "output_dir": None,
            "complete": False,
            "present": [],
            "missing": EXPECTED_OUTPUTS[:],
            "workflow": workflow_status(None),
        }
    output = output_dir(resolved)
    present = [name for name in EXPECTED_OUTPUTS if (output / name).exists()]
    missing = [name for name in EXPECTED_OUTPUTS if name not in present]
    return {
        "run_id": resolved,
        "output_dir": str(output),
        "complete": not missing,
        "present": present,
        "missing": missing,
        "workflow": workflow_status(resolved),
    }


def list_runs(limit: int = 20) -> list[dict[str, Any]]:
    ensure_dirs()
    if not runs_dir().exists():
        return []
    rows: list[dict[str, Any]] = []
    for path in sorted(runs_dir().iterdir(), key=lambda item: item.stat().st_mtime, reverse=True):
        if not path.is_dir():
            continue
        row: dict[str, Any] = {"run_id": path.name, "run_dir": str(path), "output_dir": str(path / "outputs")}
        meta = path / "run.json"
        if meta.exists():
            try:
                payload = json.loads(meta.read_text(encoding="utf-8"))
                row.update(
                    {
                        "status": payload.get("status"),
                        "created_at": payload.get("created_at"),
                        "source_files": payload.get("source_files", []),
                    }
                )
            except Exception:
                row["status"] = "unknown"
        rows.append(row)
        if len(rows) >= limit:
            break
    return rows


def runtime_status() -> dict[str, Any]:
    ensure_dirs()
    run_id = read_latest_run_id()
    workflow = workflow_status(run_id)
    return {
        "runtime_root": str(runtime_root()),
        "runs_dir": str(runs_dir()),
        "latest_run_id_file": str(latest_run_id_path()),
        "latest_run_id": run_id,
        "latest_run_dir": str(run_dir(run_id)) if run_id else None,
        "latest_output_dir": str(output_dir(run_id)) if run_id else None,
        "expected_outputs": EXPECTED_OUTPUTS,
        "sources": list_sources(run_id),
        "outputs": list_outputs(run_id),
        "runs": list_runs(),
        "validation": validate_outputs(run_id),
        "workflow": workflow,
        "workflow_table": render_workflow_table(workflow),
    }


def source_paths_from_args(args: argparse.Namespace) -> list[str]:
    paths = list(args.source_paths or [])
    if args.path:
        paths.append(args.path)
    return paths


def cmd_create_run(args: argparse.Namespace) -> int:
    return emit({"success": True, **create_run(args.run_id, source_paths_from_args(args))})


def cmd_add_input(args: argparse.Namespace) -> int:
    return emit({"success": True, **add_input(args.path, args.run_id)})


def cmd_list_inputs(args: argparse.Namespace) -> int:
    return emit({"success": True, "sources": list_sources(args.run_id), "inputs": list_sources(args.run_id)})


def cmd_list_outputs(args: argparse.Namespace) -> int:
    return emit({"success": True, "outputs": list_outputs(args.run_id)})


def cmd_read_output(args: argparse.Namespace) -> int:
    path = safe_output_path(args.name, args.run_id)
    if not path.exists():
        return emit({"success": False, "error": f"output not found: {path}", "path": str(path)})
    text = path.read_text(encoding="utf-8", errors="replace")
    truncated = len(text) > args.max_chars
    return emit({"success": True, "name": path.name, "path": str(path), "content": text[: args.max_chars], "truncated": truncated})


def cmd_validate_outputs(args: argparse.Namespace) -> int:
    return emit({"success": True, "validation": validate_outputs(args.run_id)})


def cmd_reset_run(args: argparse.Namespace) -> int:
    if args.fresh:
        sources = list_sources(args.run_id)
        return emit({"success": True, "reset": "new_run", **create_run(source_paths=[str(source["path"]) for source in sources if source.get("path")])})
    resolved = resolve_run_id(args.run_id)
    if not resolved:
        return emit({"success": True, "reset": "new_run", **create_run()})
    shutil.rmtree(output_dir(resolved), ignore_errors=True)
    output_dir(resolved).mkdir(parents=True, exist_ok=True)
    write_progress(status="pending", current_step=0, run_id=resolved)
    return emit({"success": True, "reset": "outputs", "run_id": resolved, "output_dir": str(output_dir(resolved)), "run_dir": str(run_dir(resolved))})


def cmd_status(_args: argparse.Namespace) -> int:
    return emit({"success": True, "status": runtime_status()})


def cmd_workflow_status(args: argparse.Namespace) -> int:
    workflow = workflow_status(args.run_id)
    payload: dict[str, Any] = {"success": True, "workflow": workflow}
    if args.format == "table":
        payload["table"] = render_workflow_table(workflow)
    return emit(payload)


def cmd_write_progress(args: argparse.Namespace) -> int:
    return emit(
        {
            "success": True,
            "progress": write_progress(
                status=args.status,
                current_step=args.current_step,
                run_id=args.run_id,
                failed_step=args.failed_step,
                error=args.error,
            ),
        }
    )


def cmd_template_path(_args: argparse.Namespace) -> int:
    path = PLUGIN_ROOT / "assets" / "templates" / "dashboard-sample.html"
    return emit({"success": path.exists(), "path": str(path), "exists": path.exists()})


def guarded(func, args: argparse.Namespace) -> int:
    try:
        return func(args)
    except Exception as exc:
        return emit({"success": False, "error": str(exc), "error_type": exc.__class__.__name__})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Helper CLI for ai-analyst-pipeline.")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create-run", help="Create a run and record source file paths without copying data.")
    create.add_argument("--run-id")
    create.add_argument("--path", help="Convenience single source file path.")
    create.add_argument("--source-path", dest="source_paths", action="append", help="Repeatable source file path.")
    create.set_defaults(func=cmd_create_run)

    add = sub.add_parser("add-input", help="Register a source file path on the current run.")
    add.add_argument("--path", required=True)
    add.add_argument("--run-id")
    add.set_defaults(func=cmd_add_input)

    for name, func, help_text in [
        ("list-inputs", cmd_list_inputs, "List source files recorded on a run."),
        ("list-outputs", cmd_list_outputs, "List output files on a run."),
        ("validate-outputs", cmd_validate_outputs, "Validate expected output files."),
        ("workflow-status", cmd_workflow_status, "Show workflow progress."),
    ]:
        command = sub.add_parser(name, help=help_text)
        command.add_argument("--run-id")
        if name == "workflow-status":
            command.add_argument("--format", choices=["table", "json"], default="table")
        command.set_defaults(func=func)

    read = sub.add_parser("read-output", help="Read one output file from the run outputs directory.")
    read.add_argument("--name", required=True)
    read.add_argument("--run-id")
    read.add_argument("--max-chars", type=int, default=20000)
    read.set_defaults(func=cmd_read_output)

    reset = sub.add_parser("reset-run", help="Clear current run outputs, or create a fresh run with the same sources.")
    reset.add_argument("--run-id")
    reset.add_argument("--fresh", action="store_true", help="Create a fresh run using the selected run's sources.")
    reset.set_defaults(func=cmd_reset_run)

    sub.add_parser("status", help="Show runtime status.").set_defaults(func=cmd_status)

    progress = sub.add_parser("write-progress", help="Update progress.json for the current run.")
    progress.add_argument("--status", choices=["pending", "running", "complete", "failed"], required=True)
    progress.add_argument("--current-step", type=int, default=0)
    progress.add_argument("--run-id")
    progress.add_argument("--failed-step", type=int)
    progress.add_argument("--error")
    progress.set_defaults(func=cmd_write_progress)

    sub.add_parser("template-path", help="Return the dashboard template path.").set_defaults(func=cmd_template_path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return guarded(args.func, args)


if __name__ == "__main__":
    sys.exit(main())
