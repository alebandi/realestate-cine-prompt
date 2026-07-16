from prompt_templates import PROMPT_TEMPLATE
from utils import prompt_fields, print_boxed

FIELDS = [
    ("property_type", "Property type (villa/apartment/chalet)"),
    ("view", "View (sea/city/mountain/lake)"),
    ("style", "Style (luxury/modern/minimalist)"),
    ("time", "Time of day (sunset/golden hour/daylight)"),
    ("camera", "Camera movement (drone/walkthrough/orbit/pan)"),
    ("duration", "Video duration (seconds)"),
]


def generate_prompt():
    print("\n🎬 RealEstate Cine Prompt Generator\n")
    print("Generate cinematic AI video prompts for real estate visualization.\n")

    values = prompt_fields(FIELDS)
    prompt = PROMPT_TEMPLATE.format(**values)

    print_boxed("GENERATED PROMPT", prompt)


if __name__ == "__main__":
    generate_prompt()
