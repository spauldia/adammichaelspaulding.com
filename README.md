# adammichaelspaulding.com

My personal website, with an "Ask about Adam" chatbot. The site is built with Astro and hosted on GitHub Pages. The chatbot runs on a Python API on AWS Lambda that calls Claude.

## Layout

| Folder | What it holds |
|---|---|
| `src/` | The site. Content is in `src/data/` || `api/` | The chat API: FastAPI on AWS Lambda, with DynamoDB rate limits and a monthly spending cap |
| `infra/` | Terraform for the AWS resources |
| `.github/workflows/` | The site deploy, and the chat API's tests, evals and deploy |

The chatbot answers from `/profile.json`, which is built from `src/data/`, plus a private notes file kept outside this repo.

## Running the site locally

You'll need Node 24.

```bash
npm install
npm run dev
```

The chat widget calls the live API, which accepts requests from `http://localhost:4321`.

## Testing the chat API

You'll need uv. Run from `api/`:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Deploying

- Pushing to `main` deploys the site. Pushes that only change `api/` or `infra/` skip the site deploy.
- Pull requests that change `api/` or `src/data/` run the API tests and evals.
- Pushing to `main` with changes in `api/` deploys the API through GitHub OIDC, so no AWS keys are stored in GitHub.
- Changes in `infra/` are applied by hand with `terraform plan` and `terraform apply`.

## Updating the resume

Edit the Word file, then run `resume-pipeline publish <file>.docx` from the [resume pipeline](https://github.com/spauldia/resume-pipeline). Word exports the PDF, and a GitHub Action in the private `spauldia/resume` repo commits `public/Adam_Spaulding_Resume.pdf` and `src/data/resume.json` here after checking that the PDF is one page and contains every line of the resume.

Don't edit `src/data/resume.json` by hand; the next publish replaces it.
