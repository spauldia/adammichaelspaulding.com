export type ProjectDemo = { type: "chat" } | { type: "page"; href: string };

export interface Project {
    name: string;
    summary: string;
    highlights: string[];
    tech: string[];
    codeUrl: string;
    demo: ProjectDemo;
}

export const projects: Project[] = [
    {
        name: "Ask About Adam",
        summary: "A chatbot on this site that answers questions about Adam's experience, skills, projects and interests, using only facts from his resume, his about page and a private notes file he keeps for the chatbot.",
        highlights: [
            "Python and FastAPI backend on AWS Lambda, with DynamoDB for per-visitor rate limits and a monthly spending cap.",
            "Claude Haiku 5.5 answers from the public profile plus a private notes file in S3, both in a cached system prompt, so answers stay tied to facts Adam wrote.",
            "Infrastructure in Terraform (IaC). GitHub Actions runs tests and evals on every pull request and deploys with OIDC, so no AWS keys are stored in GitHub.",
            "An eval suite checks facts, off-topic questions and attempts to override the bot's instructions.",
        ],
        tech: ["Python", "FastAPI", "AWS Lambda", "DynamoDB", "Terraform", "GitHub Actions", "Claude API"],
        codeUrl: "https://github.com/spauldia/adammichaelspaulding.com/tree/main/api",
        demo: { type: "chat" },
    },
    {
        name: "Resume Pipeline",
        summary: "One command takes Adam's resume from Word to this site: Word exports the PDF, a GitHub Action checks it and publishes the resume page and the PDF together.",
        highlights: [
            "A Python command line tool drives Microsoft Word through AppleScript on macOS and COM on Windows, so the PDF matches Word's own export exactly.",
            "Parses the Word file's XML into typed Pydantic models, failing loudly when the layout changes.",
            "A reusable GitHub Action checks the PDF is one page and contains every line of the resume, then commits both files in one atomic commit through the Git Data API.",
            "The Word file stays in a private repo; the public code is tested against a made-up resume in the same layout.",
        ],
        tech: ["Python", "Pydantic", "GitHub Actions", "GitHub REST API", "Word automation"],
        codeUrl: "https://github.com/spauldia/resume-pipeline",
        demo: { type: "page", href: "/resume/" },
    },
    {
        name: "Rx Price Watch",
        summary: "A weekly data pipeline that tracks what U.S. pharmacies pay for about 6,000 drugs back to 2013, and how prices moved for drugs on the FDA shortage list.",
        highlights: [
            "Python pipeline on AWS Lambda, run every week by EventBridge Scheduler. It loads only weeks it hasn't seen, so any run is safe to repeat.",
            "DuckDB builds a Parquet data lake on S3 from CMS's weekly NADAC survey (about 680 weeks) and snapshots of the FDA shortage list.",
            "Data quality checks stop a bad file before it reaches the lake or the page, and a CloudWatch alarm emails Adam when a run fails.",
            "Matches shortages to prices by converting the FDA's 10-digit NDCs to NADAC's 11-digit format.",
            "Publishes only the JSON files that changed to S3 behind CloudFront, and costs about a third of a cent a month to run. Terraform (IaC) for all infrastructure and GitHub Actions with OIDC for deploys.",
        ],
        tech: ["Python", "DuckDB", "Parquet", "AWS Lambda", "S3", "CloudFront", "EventBridge", "Terraform", "GitHub Actions"],
        codeUrl: "https://github.com/spauldia/rx-price-watch",
        demo: { type: "page", href: "/rx-price-watch/" },
    },
];