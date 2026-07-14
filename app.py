from prompt_templates import PROMPT_TEMPLATE


def generate_prompt():
    print("\n🎬 RealEstate Cine Prompt Generator\n")
    print("Generate cinematic AI video prompts for real estate visualization.\n")

    property_type = input("Property type (villa/apartment/chalet): ")
    view = input("View (sea/city/mountain/lake): ")
    style = input("Style (luxury/modern/minimalist): ")
    time = input("Time of day (sunset/golden hour/daylight): ")
    camera = input("Camera movement (drone/walkthrough/orbit/pan): ")
    duration = input("Video duration (seconds): ")

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


if __name__ == "__main__":
    generate_prompt()
