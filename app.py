import math
import sys

from prompt_templates import PROMPT_TEMPLATE


class PromptInputError(ValueError):
    pass


def _read_required(prompt):
    try:
        value = input(prompt).strip()
    except EOFError as error:
        field = prompt.split(" (", maxsplit=1)[0].lower()
        raise PromptInputError(f"Input ended while reading {field}.") from error

    if not value:
        field = prompt.split(" (", maxsplit=1)[0]
        raise PromptInputError(f"{field} cannot be empty.")

    return value


def _read_duration():
    duration = _read_required("Video duration (seconds): ")

    try:
        duration_value = float(duration)
    except ValueError as error:
        raise PromptInputError("Video duration must be a number.") from error

    if not math.isfinite(duration_value) or duration_value <= 0:
        raise PromptInputError("Video duration must be greater than zero.")

    return duration


def generate_prompt():
    print("\n🎬 RealEstate Cine Prompt Generator\n")
    print("Generate cinematic AI video prompts for real estate visualization.\n")

    property_type = _read_required("Property type (villa/apartment/chalet): ")
    view = _read_required("View (sea/city/mountain/lake): ")
    style = _read_required("Style (luxury/modern/minimalist): ")
    time = _read_required("Time of day (sunset/golden hour/daylight): ")
    camera = _read_required("Camera movement (drone/walkthrough/orbit/pan): ")
    duration = _read_duration()

    prompt = PROMPT_TEMPLATE.format(
        property_type=property_type,
        view=view,
        style=style,
        time=time,
        camera=camera,
        duration=duration
    )

    print("\n" + "=" * 60)
    print("GENERATED PROMPT")
    print("=" * 60)

    print(prompt)

    print("=" * 60)


def main():
    try:
        generate_prompt()
    except PromptInputError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nPrompt generation cancelled.", file=sys.stderr)
        return 130

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
