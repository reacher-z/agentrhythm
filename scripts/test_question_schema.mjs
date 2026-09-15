import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { buildQuestionSchema } from '../question-schema.mjs';

const { resources } = JSON.parse(await readFile(new URL('../dist/resources.json', import.meta.url)));
const schema = buildQuestionSchema(resources);
assert.equal(schema['@type'], 'CollectionPage');
assert.equal(schema.mainEntity['@type'], 'ItemList');
assert.equal(schema.mainEntity.numberOfItems, 29);
assert.equal(schema.mainEntity.itemListElement.length, resources.length);
for (const [index, resource] of resources.entries()) {
  const item = schema.mainEntity.itemListElement[index];
  assert.equal(item.position, index + 1);
  assert.equal(item.item.name, resource.title);
  assert.equal(item.item.description, resource.relevance);
  assert.equal(item.item.about, resource.task);
  assert.ok(item.item.sameAs.startsWith('https://'));
}
console.log(`validated ItemList schema for ${resources.length} resources`);
