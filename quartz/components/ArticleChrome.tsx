import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

function tags(value: unknown): string[] {
  if (Array.isArray(value)) return value.map(String).filter(Boolean).slice(0, 3)
  if (typeof value === "string") return value.split(",").map((item) => item.trim()).filter(Boolean).slice(0, 3)
  return []
}

const ArticleChrome: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  if (fileData.slug === "index" || !fileData.frontmatter?.title) return null
  const frontmatter = fileData.frontmatter
  const title = String(frontmatter.title)
  const description = String(frontmatter.description ?? "실행 조건과 참고 근거를 확인한 현장 기록")
  const section = String(frontmatter.section ?? "FIELD NOTE")
  const date = (fileData.dates?.modified ?? fileData.dates?.created) as Date | undefined
  const formattedDate = date ? new Intl.DateTimeFormat("ko-KR", { year: "numeric", month: "long", day: "numeric" }).format(date) : ""
  const noteTags = tags(frontmatter.tags)
  const readingTime = fileData.readingTime as unknown as { text?: string } | undefined

  return (
    <div class="ewa-article-chrome">
      <div class="ewa-article-breadcrumb"><a href="/">일하는 AI</a><span aria-hidden="true">/</span><span>{section}</span></div>
      <div class="ewa-article-kicker"><span class="ewa-signal-dot"></span>{section} <i></i> VERIFIED FIELD NOTE</div>
      <h1>{title}</h1>
      <p class="ewa-article-dek">{description}</p>
      <div class="ewa-article-meta"><time dateTime={date?.toISOString()}>{formattedDate}</time><span>{readingTime?.text ?? "읽는 데 몇 분"}</span>{noteTags.map((tag) => <a href={`/tags/${tag}`}>#{tag}</a>)}</div>
    </div>
  )
}

export default (() => ArticleChrome) satisfies QuartzComponentConstructor
