import { buildQuestionSchema } from './question-schema.mjs';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "agentsrhythm.com" || url.hostname === "www.agentsrhythm.com" ||
        (url.hostname === "agentrhythm.org" && url.protocol === "http:")) {
      url.protocol = "https:";
      url.hostname = "agentrhythm.org";
      url.port = "";
      return Response.redirect(url.href, 301);
    }
    const response = await env.ASSETS.fetch(request);
    if (!response.headers.get("content-type")?.includes("text/html")) return response;

    let pageSchema;
    if (url.pathname === "/questions/" || url.pathname === "/questions") {
      const resourceUrl = new URL('/resources.json', url.origin);
      const resourceResponse = await env.ASSETS.fetch(new Request(resourceUrl));
      if (!resourceResponse.ok) return response;
      pageSchema = buildQuestionSchema((await resourceResponse.json()).resources);
    } else {
      pageSchema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "AgentRhythm",
        "url": "https://agentrhythm.org/",
        "description": "Open research resources organized by questions, original sources and practical evidence checks."
      };
    }
    const schemaTag = `<script type="application/ld+json">${JSON.stringify(pageSchema)}</script>`;
    return new HTMLRewriter().on("head", {
      element(element) { element.append(schemaTag, { html: true }); }
    }).transform(response);
  }
};
