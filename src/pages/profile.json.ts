import type { APIRoute } from "astro";
import { profile } from "../data/profile";
import { projects } from "../data/projects";
import { about, focusAreas, hero } from "../data/site";

export const GET: APIRoute = () =>
    new Response(JSON.stringify({ profile, about, hero, focusAreas, projects }, null, 2), {
        headers: { "Content-Type": "application/json" },
    });