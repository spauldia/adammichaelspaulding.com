export interface Link {
  label: string;
  href: string;
}

export interface Role {
  title: string;
  team?: string;
  dates: string;
  highlights: string[];
}

export interface Job {
  company: string;
  description: string;
  dates: string;
  roles: Role[];
}

export interface SkillGroup {
  label: string;
  items: string;
}

export interface Degree {
  degree: string;
  school: string;
  year: string;
}

export interface Profile {
  name: string;
  headline: string;
  location: string;
  about: string[];
  email: string;
  links: Link[];
  skills: SkillGroup[];
  jobs: Job[];
  education: Degree[];
}

export const profile: Profile = {
  name: "Adam Michael Spaulding",
  headline: "Backend and Platform Engineer",
  location: "Nassau, NY",
  about: [
    "Backend engineer specializing in data pipelines and ERP integrations, with a prior career in clinical pharmacy. " +
      "Currently scaling a high-volume data platform while cutting its runtime and cost. " +
      "Previously built client integrations and automated customer onboarding with AI.",
  ],
  email: "spaulding872@gmail.com",
  links: [
    { label: "LinkedIn", href: "https://www.linkedin.com/in/adammichaelspaulding" },
    { label: "GitHub", href: "https://github.com/spauldia" },
  ],
  skills: [
    { label: "Languages", items: "Python, Java, SQL, TypeScript, JavaScript, Bash" },
    { label: "Frameworks", items: "FastAPI, Django, Spring Boot, React" },
    {
      label: "Backend and data",
      items: "REST APIs, PostgreSQL, Redis, Pydantic, Polars, pandas, DuckDB, Parquet, ETL/ELT",
    },
    {
      label: "Cloud",
      items: "AWS (ECS Fargate, Batch, Lambda, S3, DynamoDB, Aurora), Terraform, Docker, Linux, GitHub Actions CI/CD, Maven",
    },
    {
      label: "AI engineering",
      items: "Production AI agents (Claude Agent SDK), context engineering, LLM evals and safety checks, guardrails",
    },
    {
      label: "Agentic workflows",
      items: "Claude Code (custom skills, subagents), background coding agents, AI code review",
    },
    {
      label: "Engineering",
      items: "Distributed systems, event-driven pipelines, multi-tenant SaaS, performance and cost optimization, on-call",
    },
  ],
  jobs: [
    {
      company: "Pepper",
      description: "AI-first platform for independent distributors",
      dates: "Apr 2025 – Present",
      roles: [
        {
          title: "Software Engineer II",
          team: "Infrastructure Platform",
          dates: "Jun 2026 – Present",
          highlights: [
            "Drive performance, stability, and cost initiatives for the data ingestion platform (~25K pipelines/day, AWS Batch/Fargate).",
            "Led the move from JSONL to Parquet (44x smaller files, 93% less data written), part of ~$54K/yr projected AWS savings.",
            "Rebuilt PostgreSQL ingestion with concurrent upserts, parallel validation, and Polars vectorization (3x to 32x faster).",
            "Leading the consolidation of 29 client pricing systems into a single pricing engine.",
            "Switched pricing pipelines to delta ingestion and content-based triggers, ending full reloads of 6M+ rows per run.",
            "Maintain a Java connector (Maven, JUnit) that moves data between clients' IBM i ERP systems and Pepper over SFTP.",
            "Built Claude Code skills and agent runbooks that let implementation teams extend ERP integrations on their own.",
          ],
        },
        {
          title: "Software Engineer I",
          team: "AI-Powered ERP Integrations",
          dates: "Dec 2025 – Jun 2026",
          highlights: [
            "Core engineer on an AI product that turns raw ERP data into a live web app, with its ETL pipeline running within 10 minutes.",
            "Hardened the product's coding agent (Claude Agent SDK) with hallucination checks, CI-gated PRs, and A/B routing.",
            "Built an LLM feature that converts plain-English data rules into config, backed by a live eval suite.",
            "Built the self-serve portal backend (FastAPI) and its onboarding editor (React, TypeScript); first client live in 2 days.",
            "Extended the product to 7 ERPs, including QuickBooks Online (OAuth) and NetSuite.",
          ],
        },
        {
          title: "Forward Deployed Engineer",
          dates: "Apr 2025 – Dec 2025",
          highlights: [
            "Launched and stabilized ERP integrations for 35+ clients, including ETL, EDI connectors, and near-real-time pricing.",
            "Built exporters that send orders, payments, credit requests, and price edits back into each client's ERP.",
            "Owned integrations across dozens of ERPs, from scoping with client IT teams through go-live and support.",
            "Turned one-off client builds into reusable ERP integrations, so each new client starts from shared, tested code.",
          ],
        },
      ],
    },
    {
      company: "Ginsberg’s Foods",
      description: "Hudson, NY",
      dates: "Apr 2023 – Apr 2025",
      roles: [
        {
          title: "Data Programmer / Analyst",
          dates: "Jan 2024 – Apr 2025",
          highlights: [
            "Designed and ran a self-hosted data warehouse (Linux, MySQL, ClickHouse) with ETL from ERP, EDI, and web sources.",
            "Automated company reporting, built EDI integrations, and developed time-series forecasting models.",
          ],
        },
        { title: "Business Analyst", dates: "Apr 2023 – Jan 2024", highlights: [] },
      ],
    },
  ],
  education: [
    { degree: "Bachelor of Science (BS), Software Engineering", school: "Western Governors University", year: "2026" },
    {
      degree: "Master of Business Administration (MBA), summa cum laude",
      school: "Clarkson University",
      year: "2016",
    },
    {
      degree: "Doctor of Pharmacy (PharmD), summa cum laude",
      school: "Albany College of Pharmacy and Health Sciences",
      year: "2012",
    },
  ],
};
