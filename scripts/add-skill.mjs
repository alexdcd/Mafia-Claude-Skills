// Adds a skill to list.json pinning commit + hash automatically.
// Usage: node scripts/add-skill.mjs <owner/repo> <path/inside/repo> --techs a,b --note "why" [--id custom-id]
import { readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { bundleHash, fetchRepoAtCommit, parseFrontmatter, resolveHeadCommit } from './lib.mjs'

const args = process.argv.slice(2)
const positional = args.filter((arg) => !arg.startsWith('--'))
const option = (flag) => { const at = args.indexOf(flag); return at >= 0 ? args[at + 1] : undefined }
const [repo, path] = positional
if (!repo || !path) {
  console.error('Usage: node scripts/add-skill.mjs <owner/repo> <path/inside/repo> --techs a,b --note "why" [--id custom-id]')
  process.exit(1)
}

const listUrl = new URL('../list.json', import.meta.url)
const list = JSON.parse(readFileSync(listUrl, 'utf8'))

const commit = resolveHeadCommit(repo)
console.log(`pinning ${repo}@${commit.slice(0, 7)}`)
const skillDir = join(fetchRepoAtCommit(repo, commit), path)
const front = parseFrontmatter(skillDir)
const id = option('--id') ?? path.split('/').at(-1)
if (list.skills.some((skill) => skill.id === id)) {
  console.error(`"${id}" already exists in the list — remove it first or pass --id`)
  process.exit(1)
}

list.skills.push({
  id,
  name: front.name || id,
  description: front.description || '',
  source: { repo, path, commit, sha256: bundleHash(skillDir) },
  techs: (option('--techs') ?? '').split(',').map((tech) => tech.trim()).filter(Boolean),
  note: option('--note') ?? '',
  addedAt: new Date().toISOString().slice(0, 10)
})
list.skills.sort((a, b) => a.id.localeCompare(b.id))
list.updatedAt = new Date().toISOString()
writeFileSync(listUrl, JSON.stringify(list, null, 2) + '\n')
console.log(`✓ added "${id}" (${list.skills.length} skills total). Review the entry, then commit.`)
