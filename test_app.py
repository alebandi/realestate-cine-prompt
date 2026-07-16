import unittest
from contextlib import redirect_stderr
from io import StringIO
from unittest.mock import patch

import app


class PromptInputTests(unittest.TestCase):
    def test_required_input_rejects_empty_values(self):
        with patch("builtins.input", return_value="   "):
            with self.assertRaisesRegex(
                app.PromptInputError,
                "Property type cannot be empty.",
            ):
                app._read_required("Property type (villa/apartment/chalet): ")

    def test_required_input_preserves_eof_cause(self):
        with patch("builtins.input", side_effect=EOFError("stream closed")):
            with self.assertRaisesRegex(
                app.PromptInputError,
                "Input ended while reading property type.",
            ) as raised:
                app._read_required("Property type (villa/apartment/chalet): ")

        self.assertIsInstance(raised.exception.__cause__, EOFError)

    def test_duration_rejects_non_numeric_values(self):
        with patch("builtins.input", return_value="ten"):
            with self.assertRaisesRegex(
                app.PromptInputError,
                "Video duration must be a number.",
            ):
                app._read_duration()

    def test_duration_preserves_conversion_error(self):
        with patch("builtins.input", return_value="ten"):
            with self.assertRaises(app.PromptInputError) as raised:
                app._read_duration()

        self.assertIsInstance(raised.exception.__cause__, ValueError)


class MainTests(unittest.TestCase):
    def test_main_reports_expected_input_errors(self):
        stderr = StringIO()

        with patch(
            "app.generate_prompt",
            side_effect=app.PromptInputError("Property type cannot be empty."),
        ):
            with redirect_stderr(stderr):
                exit_code = app.main()

        self.assertEqual(exit_code, 2)
        self.assertEqual(
            stderr.getvalue(),
            "Error: Property type cannot be empty.\n",
        )

    def test_main_reports_interrupt_with_standard_exit_code(self):
        stderr = StringIO()

        with patch("app.generate_prompt", side_effect=KeyboardInterrupt):
            with redirect_stderr(stderr):
                exit_code = app.main()

        self.assertEqual(exit_code, 130)
        self.assertEqual(stderr.getvalue(), "\nPrompt generation cancelled.\n")

    def test_main_does_not_swallow_unexpected_errors(self):
        with patch("app.generate_prompt", side_effect=RuntimeError("boom")):
            with self.assertRaisesRegex(RuntimeError, "boom"):
                app.main()


if __name__ == "__main__":
    unittest.main()
