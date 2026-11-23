export interface Project {
    name: string;
    summary: string;
    highlights: string[];
    tech: string[];
    codeUrl: string;
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
    },
];