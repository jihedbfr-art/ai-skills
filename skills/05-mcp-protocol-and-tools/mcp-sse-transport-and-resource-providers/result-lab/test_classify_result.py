import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from classify_result import classify_response, main


ROOT = Path(__file__).parent


class ResponseLabTest(unittest.TestCase):
    def test_six_fixture_outcomes(self):
        expected = {
            "success.json": "candidate_success",
            "tool-error.json": "tool_error",
            "protocol-error.json": "protocol_error",
            "invalid-flag.json": "invalid_response",
            "mixed-envelope.json": "invalid_response",
            "untrusted-content.json": "candidate_success",
        }
        for name, outcome in expected.items():
            with self.subTest(fixture=name):
                payload = json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))
                self.assertEqual(classify_response(payload), outcome)

    def test_rejects_invalid_shapes(self):
        payloads = [
            None, [], {}, {"jsonrpc": "1.0", "id": 1, "result": {}},
            {"jsonrpc": "2.0", "result": {"content": []}},
            {"jsonrpc": "2.0", "id": 1, "result": []},
            {"jsonrpc": "2.0", "id": 1, "result": {"content": "bad"}},
            {"jsonrpc": "2.0", "id": 1, "result": {"content": [None]}},
            {"jsonrpc": "2.0", "id": 1, "result": {"content": [{"type": "text", "text": 1}]}},
            {"jsonrpc": "2.0", "id": 1, "error": {"code": True, "message": "synthetic"}},
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                self.assertEqual(classify_response(payload), "invalid_response")

    def test_declines_content_outside_the_lab_scope(self):
        for result in (
            {"content": [], "structuredContent": {"synthetic": True}},
            {"content": [{"type": "image", "data": "synthetic", "mimeType": "image/png"}]},
        ):
            with self.subTest(result=result):
                self.assertEqual(classify_response({"jsonrpc": "2.0", "id": 1, "result": result}), "unsupported_result")

    def test_missing_error_flag_defaults_to_candidate(self):
        self.assertEqual(classify_response({"jsonrpc": "2.0", "id": 1, "result": {"content": []}}), "candidate_success")

    def test_cli_returns_exit_codes_without_echoing_content(self):
        for fixture, code in (("success.json", 0), ("tool-error.json", 1), ("protocol-error.json", 2), ("untrusted-content.json", 0)):
            with self.subTest(fixture=fixture):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    actual = main([str(ROOT / "fixtures" / fixture)])
                self.assertEqual(actual, code)
                self.assertEqual(json.loads(out.getvalue())["exit_code"], code)
                self.assertNotIn("synthetic", out.getvalue().lower())
                self.assertNotIn("approval policy", out.getvalue())

    def test_bad_json_and_unreadable_input_are_summarized(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            for raw in ("{", '{"jsonrpc":"2.0","id":1,"result":NaN}'):
                path.write_text(raw, encoding="utf-8")
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    self.assertEqual(main([str(path)]), 2)
                self.assertEqual(json.loads(out.getvalue())["classification"], "invalid_response")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main([str(Path(directory) / "missing.json")]), 2)
            self.assertEqual(json.loads(out.getvalue())["classification"], "unreadable_input")
            self.assertNotIn(directory, out.getvalue())


if __name__ == "__main__":
    unittest.main()
