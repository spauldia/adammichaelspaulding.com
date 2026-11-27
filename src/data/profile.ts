import resume from "./resume.json";

export interface Link {
  label: string;
  href: string;
}

export interface Role {
  title: string;
  team: string | null;
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
  about: [resume.summary],
  email: "spaulding872@gmail.com",
  links: [
    { label: "LinkedIn", href: "https://www.linkedin.com/in/adammichaelspaulding" },
    { label: "GitHub", href: "https://github.com/spauldia" },
  ],
  skills: resume.skills,
  jobs: resume.jobs,
  education: resume.education,
};
