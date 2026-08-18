import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

type Lang = "ko" | "en" | "ja"

const T = {
  ko: { home: "일하는 AI", dek: "실행 조건과 참고 근거를 확인한 현장 기록", dateLocale: "ko-KR", dateOpts: { year: "numeric", month: "long", day: "numeric" } },
  en: { home: "Working AI", dek: "Field notes with run conditions and sources verified", dateLocale: "en-US", dateOpts: { year: "numeric", month: "long", day: "numeric" } },
  ja: { home: "働くAI", dek: "実行条件と根拠を確認した現場記録", dateLocale: "ja-JP", dateOpts: { year: "numeric", month: "long", day: "numeric" } },
} as const

const ArticleChrome: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const frontmatter = fileData.frontmatter
  const cssclass = String(frontmatter?.cssclass ?? "")
  const isHubPage = /(?:^|\s)(?:home|this-week|guides|learn-hub|play-hub)(?:\s|$)/.test(cssclass)
  const slug = String(fileData.slug ?? "")
  // 홈(KO/EN/JA)과 허브 페이지는 크롬 미표시 — 홈은 자체 h1 보유
  if (slug === "index" || slug.endsWith("/index") || !frontmatter?.title || isHubPage) return null
  const lang: Lang = (String(frontmatter?.lang ?? "ko") as Lang) ?? "ko"
  const t = T[lang] ?? T.ko
  const title = String(frontmatter.title)
  const description = String(frontmatter.description ?? t.dek)
  const section = String(frontmatter.section ?? "FIELD NOTE")
  const date = (fileData.dates?.modified ?? fileData.dates?.created) as Date | undefined
  const formattedDate = date ? new Intl.DateTimeFormat(t.dateLocale, t.dateOpts as Intl.DateTimeFormatOptions).format(date) : ""
  const homeHref = lang === "ko" ? "/" : `/${lang}/`

  return (
    <div class="ewa-article-chrome">
      <div class="ewa-article-breadcrumb"><a href={homeHref}>{t.home}</a><span aria-hidden="true">/</span><span>{section}</span></div>
      <div class="ewa-article-kicker"><span class="ewa-signal-dot"></span>{section} <i></i> VERIFIED FIELD NOTE</div>
      <h1>{title}</h1>
      <p class="ewa-article-dek">{description}</p>
      <div class="ewa-article-meta"><time dateTime={date?.toISOString()}>{formattedDate}</time></div>
    </div>
  )
}

export default (() => ArticleChrome) satisfies QuartzComponentConstructor
