import argparse
import json
from pathlib import Path


EXIT_CODES = {
    "candidate_success": 0,
    "tool_error": 1,
    "protocol_error": 2,
    "invalid_response": 2,
    "unsupported_result": 2,
    "unreadable_input": 2,
}


def classify_response(response):
    if not isinstance(response, dict) or response.get("jsonrpc") != "2.0" or "id" not in response:
        return "invalid_response"
    if ("result" in response) == ("error" in response):
        return "invalid_response"
    if "error" in response:
        error = response["error"]
        if not isinstance(error, dict):
            return "invalid_response"
        if type(error.get("code")) is not int or not isinstance(error.get("message"), str):
            return "invalid_response"
        return "protocol_error"
    result = response["result"]
    if not isinstance(result, dict) or not isinstance(result.get("content"), list):
        return "invalid_response"
    flag = result.get("isError", False)
    if not isinstance(flag, bool):
        return "invalid_response"
    if "structuredContent" in result:
        return "unsupported_result"
    for item in result["content"]:
        if not isinstance(item, dict):
            return "invalid_response"
        if item.get("type") != "text":
            return "unsupported_result"
        if not isinstance(item.get("text"), str):
            return "invalid_response"
    return "tool_error" if flag else "candidate_success"


def reject_nonfinite(_value):
    raise ValueError("Non-finite JSON number")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Classify a synthetic text-only MCP response offline.")
    parser.add_argument("response", type=Path)
    args = parser.parse_args(argv)
    try:
        response = json.loads(args.response.read_text(encoding="utf-8"), parse_constant=reject_nonfinite)
        classification = classify_response(response)
    except OSError:
        classification = "unreadable_input"
    except (ValueError, UnicodeError):
        classification = "invalid_response"
    code = EXIT_CODES[classification]
    print(json.dumps({"classification": classification, "exit_code": code}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
