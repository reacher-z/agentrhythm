# AgentRhythm

An open research resource directory organized around questions, evidence and runnable examples.

Public site: https://agentrhythm.org/

The `dist/` directory contains the complete static site, including the research task directory, original source links, JSON resource index, robots.txt and sitemap.xml. These pages can be read without JavaScript.

Cloudflare Workers serves the static assets using `wrangler.jsonc`. The original Sites registration is retained in `.openai/hosting.json` for provenance; Cloudflare deployment does not use that registration.

Teaching examples are not aggregate benchmark reproductions. No search ranking or citation-growth claim is made.
