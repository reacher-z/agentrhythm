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

    const pageSchema = url.pathname === "/questions/" || url.pathname === "/questions"
      ? {
          "@context": "https://schema.org",
          "@type": "CollectionPage",
          "name": "AgentRhythm research question directory",
          "url": "https://agentrhythm.org/questions/",
          "description": "Open directory of research works organized by task, contribution and intended use, with direct links to original sources.",
          "isPartOf": { "@type": "WebSite", "name": "AgentRhythm", "url": "https://agentrhythm.org/" },
          "about": ["AI evaluation", "evidence checking", "research agents"]
        }
      : {
          "@context": "https://schema.org",
          "@type": "WebSite",
          "name": "AgentRhythm",
          "url": "https://agentrhythm.org/",
          "description": "Open research resources organized by questions, original sources and practical evidence checks."
        };
    const schemaTag = `<script type="application/ld+json">${JSON.stringify(pageSchema)}</script>`;
    return new HTMLRewriter().on("head", {
      element(element) { element.append(schemaTag, { html: true }); }
    }).transform(response);
  }
};
