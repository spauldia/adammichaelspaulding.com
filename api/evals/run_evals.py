"""Runs the chat evals against the real model."""

import argparse
import os
import sys
from pathlib import Path

import yaml
from pydantic import BaseModel, TypeAdapter

from app.clients.anthropic_client import ClaudeClient, message_text
from app.constants import DEFAULT_MODEL
from app.models import ChatRequest
from app.services.prompt_service import build_system_prompt

CASES_PATH = Path(__file__).parent / "cases.yaml"
DEFAULT_MIN_PASS_RATE = 0.9
MIN_REPEATED_LINE_CHARS = 40


class EvalCase(BaseModel):
    """One question and the checks its answer must pass."""

    id: str
    question: str
    needs_notes: bool = False
    must_include_all: list[str] = []
    must_include_any: list[str] = []
    must_not_include: list[str] = []
    must_not_repeat_notes: bool = False

    def failures(self, answer: str, notes: str | None) -> list[str]:
        """Return a description of each check the answer fails."""
        text = answer.lower()
        problems = [f"missing '{phrase}'" for phrase in self.must_include_all if phrase.lower() not in text]
        if self.must_include_any and not any(phrase.lower() in text for phrase in self.must_include_any):
            problems.append(f"missing one of {self.must_include_any}")
        problems += [f"contains '{phrase}'" for phrase in self.must_not_include if phrase.lower() in text]
        if self.must_not_repeat_notes and notes:
            problems += [f"repeats the notes line '{line}'" for line in long_lines(notes) if line.lower() in text]
        return problems


def long_lines(text: str) -> list[str]:
    """Return the lines long enough that repeating one word for word means copying the notes."""
    lines = [line.strip().lstrip("-#* ").strip() for line in text.splitlines()]
    return [line for line in lines if len(line) >= MIN_REPEATED_LINE_CHARS]


def load_cases(path: Path) -> list[EvalCase]:
    return TypeAdapter(list[EvalCase]).validate_python(yaml.safe_load(path.read_text()))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the chat evals.")
    parser.add_argument("--profile", type=Path, required=True, help="Path to the built profile.json")
    parser.add_argument("--notes", type=Path, help="Path to a local copy of the private notes")
    parser.add_argument("--extra-cases", type=Path, help="Path to more cases kept outside the repo")
    parser.add_argument("--min-pass-rate", type=float, default=DEFAULT_MIN_PASS_RATE)
    parser.add_argument("--show-answers", action="store_true", help="Print the answer for passing cases too")
    args = parser.parse_args()

    client = ClaudeClient(api_key=os.environ["ANTHROPIC_API_KEY"], model=DEFAULT_MODEL)
    notes = args.notes.read_text() if args.notes else None
    system_prompt = build_system_prompt(args.profile.read_text(), notes)
    cases = load_cases(CASES_PATH) + (load_cases(args.extra_cases) if args.extra_cases else [])
    skipped = [case for case in cases if case.needs_notes and notes is None]
    cases = [case for case in cases if case not in skipped]
    for case in skipped:
        print(f"SKIP {case.id} (needs --notes)")

    passed = 0
    for case in cases:
        request = ChatRequest.model_validate({"messages": [{"role": "user", "content": case.question}]})
        answer = message_text(client.create_message(system_prompt, request.to_message_params()))
        problems = case.failures(answer, notes)
        if problems:
            print(f"FAIL {case.id}: {'; '.join(problems)}\n     answer: {answer}")
        else:
            passed += 1
            print(f"PASS {case.id}")
            if args.show_answers:
                print(f"     answer: {answer}")

    pass_rate = passed / len(cases)
    print(f"\n{passed}/{len(cases)} passed ({pass_rate:.0%}), minimum {args.min_pass_rate:.0%}")
    return 0 if pass_rate >= args.min_pass_rate else 1


if __name__ == "__main__":
    sys.exit(main())
