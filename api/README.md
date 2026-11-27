# Ask About Adam: chat API

The backend for the "Ask about Adam" chat on [adammichaelspaulding.com](https://adammichaelspaulding.com). Visitors, mostly recruiters, ask about my experience, projects or background, and Claude answers using only what I've written: the site's resume, about page and projects, plus a private notes file.

It's a small FastAPI app on AWS Lambda behind a Function URL. DynamoDB keeps per-visitor rate limits and the month's model spend. The AWS side stays within the free tier, and model spend is capped at $4.50 a month.

## How a question is answered

```
Browser (ChatWidget.astro)
   │  POST /chat  { messages: [...] }
   ▼
Lambda function URL (CORS: adammichaelspaulding.com and localhost only)
   │
   ▼
ChatOrchestrator
   1. Rate limit: 10 questions per 10 minutes and 30 per day for each visitor
   2. Budget: stop answering once this month's model spend reaches $4.50
   3. Ask Claude Haiku 5.5 with a cached system prompt built from
      /profile.json (the public site) and notes.md (private, in S3)
   4. Record the response's cost in DynamoDB
   │
   ▼
{ kind: "answer", reply }  or  { kind: "rate_limited" }  or  { kind: "budget" }
```

The widget shows a friendly message for `rate_limited` and `budget` instead of an error. If Claude fails or refuses, the visitor gets a short fixed reply instead of a stack trace.

## Guardrails

| Concern | How it's handled |
|---|---|
| Making things up | The system prompt allows only facts from the profile and notes. When neither covers a question, the bot says so and suggests emailing me. |
| Off-topic or loaded questions | The prompt keeps answers about my work and background, and handles questions like "was he ever fired?" without confirming or denying anything outside the profile |
| Prompt injection | Visitor messages are passed as conversation turns, never pasted into the system prompt. The evals include attempts to override the instructions. |
| Cost | A hard monthly cap on model spend, tracked in micro-dollars in DynamoDB, plus a $1 AWS budget alert on the account |
| Abuse | Rate limits per visitor. Visitors are identified by a salted HMAC of their IP address, so no IP address is ever stored. Counters expire on their own through DynamoDB TTL. |
| Secrets | The Anthropic key and the IP salt live in SSM Parameter Store, and GitHub Actions deploys through OIDC, so no AWS keys are stored in GitHub |

## Layout

| Path | What's there |
|---|---|
| `app/main.py` | The FastAPI app and the Lambda handler (Mangum) |
| `app/api.py` | Routes: `POST /chat` and `GET /health` |
| `app/orchestrators/chat_orchestrator.py` | One question from start to finish: limits, Claude, cost |
| `app/services/` | The system prompt, rate limits and monthly budget |
| `app/clients/` | Thin wrappers for Anthropic, DynamoDB, S3, SSM and the profile JSON |
| `app/config.py` | Settings from `CHAT_*` environment variables |
| `tests/` | Unit tests, with AWS faked by moto |
| `evals/` | 26 questions run against the real model, with checks on each answer |
| `scripts/build_lambda.sh` | Builds the ARM Lambda zip |

The Terraform for the function, table, notes bucket and deploy role is in [`../infra`](../infra).

## Running it locally

You'll need [uv](https://docs.astral.sh/uv/). From `api/`:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

The evals call the real model, so they need an Anthropic key and a built profile. Build the site first from the repo root (`npm run build`), then from `api/`:

```bash
ANTHROPIC_API_KEY=... uv run python -m evals.run_evals --profile ../dist/profile.json
```

Add `--notes path/to/notes.md` to include the cases that depend on the private notes, and `--show-answers` to see every answer, not just the failures. A run passes at 90% or better.

## Deploying

- Pull requests that touch `api/` or `src/data/` run the tests and the evals. A change to the resume or projects can change what the bot says, so those run the evals too.
- A push to `main` that touches `api/` builds the zip and deploys it through OIDC.
- Infrastructure changes are applied by hand from `../infra` with `terraform plan` and `terraform apply`.
- `notes.md` is updated directly in its S3 bucket and never committed.
