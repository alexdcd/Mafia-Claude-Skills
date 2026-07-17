// Re-downloads every unique source repo@commit and verifies each entry:
// the skill folder exists, contains SKILL.md, and its content hash matches.
// Fails loudly if the list has drifted from reality. Used by CI on every push.
import { readFileSync } from 'node:fs'
import { existsSync } from 'node:fs'
import { join } from 'node:path'
import { bundleHash, fetchRepoAtCommit } from './lib.mjs'

const list = JSON.parse(readFileSync(new URL('../list.json', import.meta.url), 'utf8'))

const ids = new Set()
const problems = []
const cache = new Map()
const checkoutFor = (repo, commit) => {
  const key = `${repo}@${commit}`
  if (!cache.has(key)) {
    console.log(`fetching ${key}`)
    cache.set(key, fetchRepoAtCommit(repo, commit))
  }
  return cache.get(key)
}

for (const skill of list.skills) {
  if (ids.has(skill.id)) problems.push(`${skill.id}: duplicate id`)
  ids.add(skill.id)
  for (const field of ['id', 'name', 'source', 'techs', 'note', 'addedAt']) {
    if (skill[field] === undefined) problems.push(`${skill.id}: missing field "${field}"`)
  }
  const { repo, path, commit, sha256: expected } = skill.source ?? {}
  if (!repo || !path || !/^[0-9a-f]{40}$/.test(commit ?? '') || !/^[0-9a-f]{64}$/.test(expected ?? '')) {
    problems.push(`${skill.id}: incomplete source pin`)
    continue
  }
  try {
    const skillDir = join(checkoutFor(repo, commit), path)
    if (!existsSync(join(skillDir, 'SKILL.md'))) {
      problems.push(`${skill.id}: ${path} has no SKILL.md at ${repo}@${commit.slice(0, 7)}`)
      continue
    }
    const actual = bundleHash(skillDir)
    if (actual !== expected) problems.push(`${skill.id}: hash mismatch (expected ${expected.slice(0, 12)}…, got ${actual.slice(0, 12)}…)`)
  } catch (error) {
    problems.push(`${skill.id}: ${error.message}`)
  }
}

if (problems.length) {
  console.error(`\n${problems.length} problem(s):`)
  for (const problem of problems) console.error(`  ✗ ${problem}`)
  process.exit(1)
}
console.log(`✓ ${list.skills.length} skills verified against their pinned sources`)
