// Regenerates LIST.md (the full curated table) from list.json.
import { readFileSync, writeFileSync } from 'node:fs'

const list = JSON.parse(readFileSync(new URL('../list.json', import.meta.url), 'utf8'))

const link = (skill) => `[${skill.id}](https://github.com/${skill.source.repo}/tree/${skill.source.commit}/${skill.source.path})`
const rows = list.skills
  .slice()
  .sort((a, b) => a.id.localeCompare(b.id))
  .map((skill) => `| ${link(skill)} | ${(skill.description || '').replaceAll('|', '\\|').slice(0, 120)} | ${skill.techs.join(', ') || '—'} | ${skill.upstream ? skill.upstream.repo : skill.source.repo} |`)

const content = [
  '# 📜 MafiaIA Skill List',
  '',
  'Lista curada de Agent Skills con procedencia verificable: cada entrada fijada a commit + sha256 de su repo de origen. Generado desde [`list.json`](list.json) — no editar a mano.',
  '',
  `Total: **${list.skills.length} skills** · actualizada ${list.updatedAt.slice(0, 10)}`,
  '',
  '| Skill | Descripción | Tecnologías | Origen |',
  '| --- | --- | --- | --- |',
  ...rows,
  ''
].join('\n')

writeFileSync(new URL('../LIST.md', import.meta.url), content)
console.log(`LIST.md updated (${list.skills.length} skills)`)
