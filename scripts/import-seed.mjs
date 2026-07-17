// One-off/repeatable seed import. Builds list.json from two pinned sources:
//  1. midudev/autoskills — the skills its skills-map.ts actively recommends,
//     with upstream provenance and AI-review status from its registry index.
//  2. alexdcd/Mafia-Claude-Skills — every skill under skills/ (La Mafia IA picks).
// Usage: node scripts/import-seed.mjs <autoskills-dir> <autoskills-commit> <mafia-dir> <mafia-commit>
import { existsSync, readdirSync, readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { assertSkillDir, bundleHash, parseFrontmatter } from './lib.mjs'

const [autoskillsDir, autoskillsCommit, mafiaDir, mafiaCommit] = process.argv.slice(2)
if (!autoskillsDir || !autoskillsCommit || !mafiaDir || !mafiaCommit) {
  console.error('Usage: node scripts/import-seed.mjs <autoskills-dir> <commit> <mafia-dir> <commit>')
  process.exit(1)
}

const registryPath = 'packages/autoskills/skills-registry'
const registryDir = join(autoskillsDir, registryPath)
const index = JSON.parse(readFileSync(join(registryDir, 'index.json'), 'utf8'))
const mapSource = readFileSync(join(autoskillsDir, 'packages/autoskills/skills-map.ts'), 'utf8')

// Parse SKILLS_MAP + COMBO blocks: capture id, and each "owner/repo/skill" ref.
const techsBySkill = new Map()
const blockPattern = /\{\s*id:\s*"([^"]+)"[\s\S]*?skills:\s*\[([\s\S]*?)\]/g
for (const block of mapSource.matchAll(blockPattern)) {
  const [, techId, skillRefs] = block
  for (const ref of skillRefs.matchAll(/"([^"]+)"/g)) {
    const skillId = ref[1].split('/').at(-1)
    if (!techsBySkill.has(skillId)) techsBySkill.set(skillId, new Set())
    techsBySkill.get(skillId).add(techId)
  }
}

const entries = []
let missing = 0
for (const [skillId, techs] of [...techsBySkill.entries()].sort()) {
  const skillDir = join(registryDir, skillId)
  if (!existsSync(join(skillDir, 'SKILL.md'))) { missing++; console.warn(`skip (not in registry): ${skillId}`); continue }
  const meta = index.skills[skillId]
  const front = parseFrontmatter(skillDir)
  entries.push({
    id: skillId,
    name: front.name || skillId,
    description: front.description || '',
    source: { repo: 'midudev/autoskills', path: `${registryPath}/${skillId}`, commit: autoskillsCommit, sha256: bundleHash(skillDir) },
    upstream: meta ? { repo: meta.source, commit: meta.commitSha } : undefined,
    review: meta?.review?.status === 'approved' && !meta.review.summary.includes('skipped')
      ? { status: 'approved', by: meta.review.model, at: meta.review.reviewedAt } : undefined,
    techs: [...techs].sort(),
    note: 'Seed: recomendada por el mapa de autoskills (midudev), copia auditada de su registry.',
    addedAt: '2026-07-17'
  })
}

for (const skillId of readdirSync(join(mafiaDir, 'skills')).sort()) {
  if (skillId === 'template-skill' || skillId.startsWith('.')) continue
  const skillDir = join(mafiaDir, 'skills', skillId)
  if (!existsSync(join(skillDir, 'SKILL.md'))) continue
  assertSkillDir(skillDir)
  const front = parseFrontmatter(skillDir)
  entries.push({
    id: `mafia-${skillId}`,
    name: front.name || skillId,
    description: front.description || '',
    source: { repo: 'alexdcd/Mafia-Claude-Skills', path: `skills/${skillId}`, commit: mafiaCommit, sha256: bundleHash(skillDir) },
    techs: [],
    note: 'Seed: curada a mano en Mafia-Claude-Skills (La Mafia IA).',
    addedAt: '2026-07-17'
  })
}

const duplicated = entries.map((entry) => entry.id).filter((id, position, all) => all.indexOf(id) !== position)
if (duplicated.length) throw new Error(`Duplicate ids: ${duplicated.join(', ')}`)

const list = {
  version: 1,
  name: 'MafiaIA Skill List',
  updatedAt: new Date().toISOString(),
  hashAlgorithm: 'sha256 over "<relpath>\\0<sha256(file)>\\n" lines, files sorted by relative path',
  skills: entries
}
writeFileSync(new URL('../list.json', import.meta.url), JSON.stringify(list, null, 2) + '\n')
console.log(`list.json: ${entries.length} skills (${missing} map refs not in registry, skipped)`)
