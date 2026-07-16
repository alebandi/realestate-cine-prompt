import io
import runpy
from unittest import mock

import app
from prompt_templates import PROMPT_TEMPLATE

SAMPLE_ANSWERS = [
    "villa",        # property type
    "sea",          # view
    "modern",       # style
    "golden hour",  # time of day
    "drone",        # camera movement
    "10",           # duration
]


def _run_generate_prompt(answers):
    with mock.patch("builtins.input", side_effect=answers), mock.patch(
        "sys.stdout", new_callable=io.StringIO
    ) as fake_stdout:
        app.generate_prompt()
    return fake_stdout.getvalue()


def test_generate_prompt_prints_expected_prompt():
    output = _run_generate_prompt(SAMPLE_ANSWERS)

    expected_prompt = PROMPT_TEMPLATE.format(
        property_type="villa",
        view="sea",
        style="modern",
        time="golden hour",
        camera="drone",
        duration="10",
    )

    assert expected_prompt in output


def test_generate_prompt_includes_header_and_user_values():
    output = _run_generate_prompt(SAMPLE_ANSWERS)

    assert "GENERATED PROMPT" in output
    assert "=" * 60 in output
    assert "showcasing a villa." in output
    assert "beautiful sea." in output
    assert "10 seconds." in output


def test_generate_prompt_consumes_all_inputs_in_order():
    inputs = iter(SAMPLE_ANSWERS)
    calls = []

    def fake_input(prompt=""):
        calls.append(prompt)
        return next(inputs)

    with mock.patch("builtins.input", side_effect=fake_input), mock.patch(
        "sys.stdout", new_callable=io.StringIO
    ):
        app.generate_prompt()

    assert len(calls) == len(SAMPLE_ANSWERS)
    assert any("Property type" in prompt for prompt in calls)
    assert any("Camera movement" in prompt for prompt in calls)


def test_generate_prompt_handles_empty_inputs():
    output = _run_generate_prompt([""] * len(SAMPLE_ANSWERS))

    assert "GENERATED PROMPT" in output


def test_module_runs_as_script():
    with mock.patch("builtins.input", side_effect=SAMPLE_ANSWERS), mock.patch(
        "sys.stdout", new_callable=io.StringIO
    ) as fake_stdout:
        runpy.run_module("app", run_name="__main__")

    assert "GENERATED PROMPT" in fake_stdout.getvalue()
