export function primarySource(resource) {
  const links = resource.source_links || {};
  return links.Paper || links.arXiv || links.Project || Object.values(links)[0];
}

export function buildQuestionSchema(resources) {
  return {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'AgentRhythm research question directory',
    url: 'https://agentrhythm.org/questions/',
    description: 'Open directory of research works organized by task, contribution and intended use, with direct links to original sources.',
    isPartOf: { '@type': 'WebSite', name: 'AgentRhythm', url: 'https://agentrhythm.org/' },
    about: ['AI evaluation', 'evidence checking', 'research agents'],
    mainEntity: {
      '@type': 'ItemList',
      numberOfItems: resources.length,
      itemListElement: resources.map((resource, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        item: {
          '@type': 'CreativeWork',
          name: resource.title,
          description: resource.relevance,
          about: resource.task,
          sameAs: primarySource(resource),
        },
      })),
    },
  };
}
