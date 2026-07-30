import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const ArticleChrome: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  if (fileData.slug === "index" || !fileData.frontmatter?.title) return null
  const frontmatter = fileData.frontmatter
  const title = String(frontmatter.title)
  const description = String(frontmatter.description ?? "실행 조건과 참고 근거를 확인한 현장 기록")
  const section = String(frontmatter.section ?? "FIELD NOTE")
  const date = (fileData.dates?.modified ?? fileData.dates?.created) as Date | undefined
  const formattedDate = date ? new Intl.DateTimeFormat("ko-KR", { year: "numeric", month: "long", day: "numeric" }).format(date) : ""

  return (
    <div class="ewa-article-chrome">
      <div class="ewa-article-breadcrumb"><a href="/">일하는 AI</a><span aria-hidden="true">/</span><span>{section}</span></div>
      <div class="ewa-article-kicker"><span class="ewa-signal-dot"></span>{section} <i></i> VERIFIED FIELD NOTE</div>
      <h1>{title}</h1>
      <p class="ewa-article-dek">{description}</p>
      <div class="ewa-article-meta"><time dateTime={date?.toISOString()}>{formattedDate}</time></div>
    </div>
  )
}

export default (() => ArticleChrome) satisfies QuartzComponentConstructor
