import pytest

from app.services.prompt_service import build_system_prompt


def test_includes_the_profile() -> None:
    prompt = build_system_prompt('{"name": "Adam"}', None)

    assert '<profile>\n{"name": "Adam"}\n</profile>' in prompt


def test_includes_the_notes_after_the_profile() -> None:
    prompt = build_system_prompt("{}", "## Hobbies\n- Chess\n")

    assert prompt.endswith("<profile>\n{}\n</profile>\n\n<notes>\n## Hobbies\n- Chess\n</notes>")


@pytest.mark.parametrize("notes", [None, "", "  \n"])
def test_leaves_out_empty_notes(notes: str | None) -> None:
    prompt = build_system_prompt("{}", notes)

    assert prompt.endswith("</profile>")
    assert "<notes>\n" not in prompt
