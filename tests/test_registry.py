from app.tools.registry import TOOLS, TOOLS_SCHEMA


def test_tools_schema_matches_tools_registry():
    tool_names = set(TOOLS)
    schema_names = {tool["function"]["name"] for tool in TOOLS_SCHEMA}
    assert schema_names == tool_names

    run_tests_schema = next(
        tool["function"] for tool in TOOLS_SCHEMA if tool["function"]["name"] == "run_tests"
    )
    assert run_tests_schema["parameters"] == {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }
