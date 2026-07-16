import string

from prompt_templates import PROMPT_TEMPLATE

EXPECTED_FIELDS = {
    "property_type",
    "view",
    "style",
    "time",
    "camera",
    "duration",
}


def _template_fields(template):
    return {
        field_name
        for _, field_name, _, _ in string.Formatter().parse(template)
        if field_name
    }


def test_template_is_non_empty_string():
    assert isinstance(PROMPT_TEMPLATE, str)
    assert PROMPT_TEMPLATE.strip()


def test_template_exposes_exactly_expected_placeholders():
    assert _template_fields(PROMPT_TEMPLATE) == EXPECTED_FIELDS


def test_template_formats_without_missing_or_extra_keys():
    values = {field: field.upper() for field in EXPECTED_FIELDS}

    result = PROMPT_TEMPLATE.format(**values)

    assert "{" not in result
    assert "}" not in result
    for value in values.values():
        assert value in result


def test_template_substitutes_values_in_context():
    result = PROMPT_TEMPLATE.format(
        property_type="villa",
        view="sea view",
        style="modern",
        time="golden hour",
        camera="drone",
        duration="10",
    )

    assert "showcasing a villa." in result
    assert "beautiful sea view." in result
    assert "modern design" in result
    assert "Shot during golden hour" in result
    assert "Smooth drone camera movement" in result
    assert "10 seconds." in result


def test_template_missing_key_raises_key_error():
    try:
        PROMPT_TEMPLATE.format(property_type="villa")
    except KeyError:
        pass
    else:
        raise AssertionError("Expected KeyError for missing placeholders")
