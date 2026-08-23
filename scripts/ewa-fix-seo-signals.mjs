import { copyFile, readFile, readdir, writeFile } from "node:fs/promises"
import path from "node:path"

const root = process.cwd()
const publicDir = path.join(root, "public")
const baseUrl = "https://easyworking-ai.github.io"

const noindexFolderRoutes = new Set([
  "/guides/",
  "/en/guides/",
  "/ja/guides/",
  "/learn/",
  "/en/learn/",
  "/ja/learn/",
  "/wiki/",
  "/wiki/concepts/",
  "/youtube/chatGPT/",
  "/youtube/chatgpt/",
  "/youtube/claude/",
  "/youtube/n8n/",
  "/en/youtube/chatGPT/",
  "/en/youtube/chatgpt/",
  "/en/youtube/claude/",
  "/en/youtube/n8n/",
  "/ja/youtube/chatGPT/",
  "/ja/youtube/chatgpt/",
  "/ja/youtube/claude/",
  "/ja/youtube/n8n/",
])

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

function toPosix(value) {
  return value.split(path.sep).join("/")
}

function routeFromRelative(relativePath) {
  const rel = toPosix(relativePath)
  if (rel === "index.html") return "/"
  if (rel.endsWith("/index.html")) return `/${rel.slice(0, -"index.html".length)}`
  return `/${rel}`
}

function languageFromRelative(relativePath) {
  const rel = toPosix(relativePath)
  if (rel.startsWith("en/")) return "en"
  if (rel.startsWith("ja/")) return "ja"
  return "ko"
}

function routeKey(route) {
  if (route === "/") return "/"
  for (const lang of ["/en/", "/ja/"]) {
    if (route.startsWith(lang)) return `/${route.slice(lang.length)}`
  }
  return route
}

function canonicalUrl(route) {
  return `${baseUrl}${route}`
}

function escapeHtml(value) {
  return value.replace(/&/g, "&amp;").replace(/"/g, "&quot;")
}

function hasNoindex(source) {
  return /<meta\s+name=["']robots["'][^>]*content=["'][^"']*noindex/i.test(source)
}

function upsertMeta(source, name, content) {
  const escaped = escapeHtml(content)
  const re = new RegExp(`<meta\\s+name=["']${name}["'][^>]*>`, "i")
  const tag = `<meta name="${name}" content="${escaped}"/>`
  if (re.test(source)) return source.replace(re, tag)
  return source.replace(/<\/head>/i, `${tag}</head>`)
}

function upsertProperty(source, property, content) {
  const escaped = escapeHtml(content)
  const re = new RegExp(`<meta\\s+property=["']${property}["'][^>]*>`, "i")
  const tag = `<meta property="${property}" content="${escaped}"/>`
  if (re.test(source)) return source.replace(re, tag)
  return source.replace(/<\/head>/i, `${tag}</head>`)
}

function upsertLink(source, rel, attrs) {
  const attrText = Object.entries(attrs)
    .map(([key, value]) => `${key}="${escapeHtml(value)}"`)
    .join(" ")
  const re = new RegExp(`<link\\s+rel=["']${rel}["'][^>]*>`, "i")
  const tag = `<link rel="${rel}" ${attrText}/>`
  if (re.test(source)) return source.replace(re, tag)
  return source.replace(/<\/head>/i, `${tag}</head>`)
}

function appendLink(source, rel, attrs) {
  const attrText = Object.entries(attrs)
    .map(([key, value]) => `${key}="${escapeHtml(value)}"`)
    .join(" ")
  const identity = attrs.hreflang ? `[^>]*hreflang=["']${escapeHtml(attrs.hreflang)}["']` : ""
  const re = new RegExp(`<link\\s+rel=["']${rel}["']${identity}[^>]*>`, "i")
  if (re.test(source)) return source
  return source.replace(/<\/head>/i, `<link rel="${rel}" ${attrText}/></head>`)
}

const files = await collectHtmlFiles(publicDir)
const records = []

for (const file of files) {
  const relative = toPosix(path.relative(publicDir, file))
  const source = await readFile(file, "utf8")
  const route = routeFromRelative(relative)
  const isStatic = relative.startsWith("static/")
  const is404 = relative === "404.html"
  const noindex = hasNoindex(source) || noindexFolderRoutes.has(route) || route.startsWith("/tags/")
  records.push({
    file,
    relative,
    route,
    language: languageFromRelative(relative),
    key: routeKey(route),
    source,
    isStatic,
    is404,
    noindex,
  })
}

const indexable = records.filter((record) => !record.isStatic && !record.is404 && !record.noindex)
const availableByKey = new Map()
for (const record of indexable) {
  if (!availableByKey.has(record.key)) availableByKey.set(record.key, new Map())
  availableByKey.get(record.key).set(record.language, record.route)
}

let changedFiles = 0
let canonicalCount = 0
let alternateCount = 0
let noindexCount = 0

for (const record of records) {
  let output = record.source

  if (record.isStatic || record.is404) continue

  if (record.noindex) {
    const before = output
    output = upsertMeta(output, "robots", "noindex,follow")
    if (output !== before) noindexCount += 1
  } else {
    output = upsertLink(output, "canonical", { href: canonicalUrl(record.route) })
    output = upsertProperty(output, "og:url", canonicalUrl(record.route))
    output = upsertProperty(output, "twitter:url", canonicalUrl(record.route))
    canonicalCount += 1

    const translations = availableByKey.get(record.key)
    if (translations && translations.size > 1) {
      for (const [lang, route] of translations) {
        output = appendLink(output, "alternate", { hreflang: lang, href: canonicalUrl(route) })
        alternateCount += 1
      }
      if (translations.has("ko")) {
        output = appendLink(output, "alternate", {
          hreflang: "x-default",
          href: canonicalUrl(translations.get("ko")),
        })
        alternateCount += 1
      }
    }
  }

  if (output !== record.source) {
    await writeFile(record.file, output)
    changedFiles += 1
  }
}

const robotsSource = path.join(root, "quartz/static/robots.txt")
await copyFile(robotsSource, path.join(publicDir, "robots.txt"))

const sitemapPath = path.join(publicDir, "sitemap.xml")
if (
  await readFile(sitemapPath, "utf8")
    .then(() => true)
    .catch(() => false)
) {
  const sitemap = await readFile(sitemapPath, "utf8")
  const indexableRoutes = new Set(indexable.map((record) => record.route))
  const seen = new Set()
  const output = sitemap.replace(
    /<url>\s*<loc>(.*?)<\/loc>([\s\S]*?)<\/url>/g,
    (block, rawLoc, tail) => {
      const url = new URL(rawLoc)
      let route = url.pathname
      if (route !== "/" && !route.endsWith("/") && !route.endsWith(".html")) route += ".html"
      if (!indexableRoutes.has(route) || seen.has(route)) return ""
      seen.add(route)
      return `<url>\n    <loc>${canonicalUrl(route)}</loc>${tail}</url>`
    },
  )
  await writeFile(sitemapPath, output)
  console.log(`Rewrote sitemap locs: ${seen.size}`)
}

console.log(
  `Applied SEO signals to ${changedFiles} HTML files; canonical=${canonicalCount}, alternate=${alternateCount}, noindex=${noindexCount}.`,
)
