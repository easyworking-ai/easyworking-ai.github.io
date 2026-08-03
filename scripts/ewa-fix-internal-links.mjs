import { readFile, readdir, writeFile } from "node:fs/promises"
import path from "node:path"

const root = process.cwd()
const publicDir = path.join(root, "public")

async function collectHtmlFiles(dir) {
  const entries = await readdir(dir, { withFileTypes: true })
  const files = []
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      files.push(...(await collectHtmlFiles(fullPath)))
    } else if (entry.isFile() && entry.name.endsWith(".html")) {
      files.push(fullPath)
    }
  }
  return files
}

function targetSlugFromTag(tag) {
  const match = tag.match(/\bdata-slug="([^"]+)"/)
  if (!match) return null
  const slug = decodeURIComponent(match[1]).replace(/^\/+|\/+$/g, "")
  if (!slug || slug === "index") return null
  return slug
}

const files = await collectHtmlFiles(publicDir)
const generatedPaths = new Set(files.map((file) => path.relative(publicDir, file)))
let changedFiles = 0
let rewrittenLinks = 0

for (const file of files) {
  const source = await readFile(file, "utf8")
  const output = source.replace(/<a\b[^>]*>/g, (tag) => {
    const slug = targetSlugFromTag(tag)
    if (!slug) return tag

    if (!generatedPaths.has(`${slug}.html`)) return tag

    const nextTag = tag.replace(/\bhref="[^"]*"/, `href="/${slug}.html"`)
    if (nextTag !== tag) rewrittenLinks += 1
    return nextTag
  })

  if (output !== source) {
    await writeFile(file, output)
    changedFiles += 1
  }
}

console.log(`Repaired ${rewrittenLinks} internal HTML links in ${changedFiles} generated files.`)
