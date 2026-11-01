export interface NavLink {
  label: string;
  href: string;
}

export interface FocusArea {
  title: string;
  text: string;
}

export const nav: NavLink[] = [
  { label: "About", href: "/about/" },
  { label: "Projects", href: "/projects/" },
  { label: "Resume", href: "/resume/" },
];

export const hero = {
  headline: "From prescriptions to pipelines.",
  subline:
    "Former clinical pharmacist, now a backend & platform engineer building data infrastructure and production AI.",
};

export const focusAreas: FocusArea[] = [
  {
    title: "Data platforms",
    text: "Pipelines that move millions of rows into PostgreSQL every day on AWS, built to be fast, reliable, and cheap to run.",
  },
  {
    title: "Production AI",
    text: "AI agents that write and test integration code, with guardrails, evals, and safety checks built in.",
  },
  {
    title: "Integrations",
    text: "ERP integrations for more than 35 distributors, from on-premises connectors to cloud APIs.",
  },
];

export const about = {
  lead:
    "Backend and platform engineer at Pepper, an AI-first platform for independent distributors. " +
    "The work centers on cloud data infrastructure and production AI: the pipelines that bring each customer's ERP data into the product, " +
    "and the AI systems that set up new customers.",
  before: [
    "Adam spent six years as a clinical pharmacist in hospital emergency medicine and critical care, at Boston Medical Center, " +
      "Waterbury Hospital, Orange Regional Medical Center, and LewisGale Medical Center, where the last role was clinical pharmacy manager.",
    "That career started with a PharmD and an ASHP-accredited residency at Buffalo General Medical Center, and went on to include board " +
      "certification in pharmacotherapy (BCPS), adjunct faculty appointments at Northeastern University and the University of Connecticut, " +
      "and published research and talks on emergency medicine pharmacotherapy. Adam also earned a Master of Business Administration (MBA).",
  ],
  switch: [
    "The turn toward engineering started with a statistics problem. As a clinical pharmacy manager running research studies, " +
      "Adam learned R to analyze the data and soon found the code more interesting than the p-values. Meanwhile, the next decade " +
      "in hospital pharmacy was starting to look a lot like the last six years. So Adam traded a stable, well-paid pharmacy career " +
      "for a data job at a food distributor, a move that surprised nearly everyone except Adam.",
    "At Ginsberg's Foods, the reporting work started in R and moved to Python and SQL as the projects got bigger. That led to " +
      "running the company's data warehouse, and from there to software engineering at Pepper. Emergency medicine and production systems turn out to have a lot in common. Both depend on accurate data " +
      "and calm decisions under pressure, and both need safety checks before anything reaches a patient or a customer.",
  ],
  interests: "Reading, fitness and nutrition, Stoic philosophy, and mindfulness practice rooted in Zen Buddhism.",
};

export const contact = {
  title: "Get in touch",
  text: "Email is the best way to reach Adam. LinkedIn works too.",
};
