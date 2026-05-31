#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).with_name("ai_pipeline.py")
spec = importlib.util.spec_from_file_location("ai_pipeline", MODULE_PATH)
ai_pipeline = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(ai_pipeline)


class RuntimeRootTests(unittest.TestCase):
    def test_default_runtime_root_uses_documents_folder(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(ai_pipeline.runtime_root(), Path.home() / "Documents" / "data-ai-pipeline")

    def test_runtime_root_override_still_wins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {"AI_PIPELINE_RUNTIME_ROOT": tmp}, clear=True):
                self.assertEqual(ai_pipeline.runtime_root(), Path(tmp).resolve())

    def test_create_run_records_analyst_output_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.csv"
            source.write_text("id,value\n1,10\n", encoding="utf-8")
            runtime = Path(tmp) / "runtime"
            with patch.dict(os.environ, {"AI_PIPELINE_RUNTIME_ROOT": str(runtime)}, clear=True):
                created = ai_pipeline.create_run(source_paths=[str(source)])
                run = ai_pipeline.read_run(str(created["run_id"]))

                self.assertEqual(run["pipeline_version"], "analyst-v2")
                self.assertEqual(run["expected_outputs"], ai_pipeline.EXPECTED_OUTPUTS)
                self.assertIn("04_metrics.json", ai_pipeline.EXPECTED_OUTPUTS)
                self.assertIn("05_analysis.py", ai_pipeline.EXPECTED_OUTPUTS)
                self.assertIn("05_analysis.ipynb", ai_pipeline.EXPECTED_OUTPUTS)
                self.assertIn("08_validation_report.md", ai_pipeline.EXPECTED_OUTPUTS)

    def test_workflow_and_validation_handle_multi_output_steps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.csv"
            source.write_text("id,value\n1,10\n", encoding="utf-8")
            runtime = Path(tmp) / "runtime"
            with patch.dict(os.environ, {"AI_PIPELINE_RUNTIME_ROOT": str(runtime)}, clear=True):
                created = ai_pipeline.create_run(source_paths=[str(source)])
                run_id = str(created["run_id"])
                output_dir = Path(created["output_dir"])

                workflow = ai_pipeline.workflow_status(run_id)
                self.assertEqual(workflow["total_steps"], 7)
                self.assertEqual(workflow["steps"][0]["output"], "00_data_contract.md, 01_dataset_profile.md")
                self.assertEqual(
                    workflow["steps"][4]["output"],
                    "05_analysis.py, 05_analysis.ipynb, 05_analysis_report.md",
                )
                self.assertEqual(workflow["steps"][0]["status"], "pending")

                (output_dir / "00_data_contract.md").write_text("# 계약\n", encoding="utf-8")
                workflow = ai_pipeline.workflow_status(run_id)
                self.assertEqual(workflow["steps"][0]["status"], "partial")

                for name in ai_pipeline.EXPECTED_OUTPUTS:
                    (output_dir / name).write_text("ok\n", encoding="utf-8")
                validation = ai_pipeline.validate_outputs(run_id)
                self.assertTrue(validation["complete"])
                self.assertEqual(validation["missing"], [])


if __name__ == "__main__":
    unittest.main()
