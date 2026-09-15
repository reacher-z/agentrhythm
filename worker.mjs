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
    return env.ASSETS.fetch(request);
  }
};
