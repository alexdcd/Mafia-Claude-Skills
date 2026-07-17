import { createHash } from 'node:crypto'
import { execFileSync } from 'node:child_process'
import { mkdtempSync, readdirSync, readFileSync, statSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, relative } from 'node:path'

export const sha256 = (buffer) => createHash('sha256').update(buffer).digest('hex')

const walkFiles = (root, dir = root, out = []) => {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name)
    if (entry.isSymbolicLink()) throw new Error(`Symlink not allowed in skill: ${path}`)
    if (entry.isDirectory()) walkFiles(root, path, out)
    else if (entry.isFile()) out.push(relative(root, path))
  }
  return out.sort()
}

// Deterministic content hash of a skill folder: sha256 over
// "<relpath>\0<sha256(file)>\n" lines, files sorted by relative path.
export const bundleHash = (skillDir) => {
  const lines = walkFiles(skillDir).map(
    (rel) => `${rel}\0${sha256(readFileSync(join(skillDir, rel)))}\n`
  )
  return sha256(lines.join(''))
}

export const resolveHeadCommit = (repo) => {
  const output = execFileSync('git', ['ls-remote', `https://github.com/${repo}`, 'HEAD'], { encoding: 'utf8' })
  const commit = output.split('\t')[0]?.trim()
  if (!/^[0-9a-f]{40}$/.test(commit ?? '')) throw new Error(`Could not resolve HEAD of ${repo}`)
  return commit
}

// Downloads repo@commit via codeload (does not consume API rate limit)
// and returns the extracted root directory.
export const fetchRepoAtCommit = (repo, commit) => {
  const dir = mkdtempSync(join(tmpdir(), 'skill-list-'))
  const url = `https://codeload.github.com/${repo}/tar.gz/${commit}`
  execFileSync('bash', ['-c', `curl -fsSL "${url}" | tar -xz -C "${dir}"`])
  const [root] = readdirSync(dir)
  if (!root) throw new Error(`Empty tarball for ${repo}@${commit}`)
  return join(dir, root)
}

export const parseFrontmatter = (skillDir) => {
  const raw = readFileSync(join(skillDir, 'SKILL.md'), 'utf8')
  const match = raw.match(/^---\n([\s\S]*?)\n---/)
  const fields = {}
  if (match) {
    for (const line of match[1].split('\n')) {
      const kv = line.match(/^([A-Za-z_-]+):\s*(.*)$/)
      if (kv) fields[kv[1]] = kv[2].replace(/^['"]|['"]$/g, '').trim()
    }
  }
  return fields
}

export const assertSkillDir = (skillDir) => {
  statSync(join(skillDir, 'SKILL.md'))
}
