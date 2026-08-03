import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const NAV_ITEMS = [
  { href: "/this-week.html", ko: "이번 주", en: "This Week", ja: "今週" },
  { href: "/radio.html", ko: "라디오", en: "Radio", ja: "ラジオ" },
  { href: "/guides.html", ko: "가이드", en: "Guides", ja: "ガイド" },
  { href: "/learn.html", ko: "학습하기", en: "Learn", ja: "学ぶ" },
  { href: "/play.html", ko: "체험하기", en: "Play", ja: "体験" },
]

const SiteHeader: QuartzComponent = ({ allFiles }: QuartzComponentProps) => {
  const searchItems = allFiles
    .filter((file) => {
      const slug = String(file.slug ?? "")
      return Boolean(
        file.slug &&
        slug !== "index" &&
        slug !== "404" &&
        slug !== "readme" &&
        !slug.endsWith("/index") &&
        !slug.startsWith("tags/") &&
        !slug.startsWith("en/") &&
        !slug.startsWith("ja/") &&
        file.frontmatter?.title,
      )
    })
    .map((file) => ({
      title: String(file.frontmatter?.title ?? file.slug),
      slug: `/${file.slug}`,
      description: String(file.frontmatter?.description ?? ""),
    }))

  return (
    <div class="ewa-site-header" data-ewa-header>
      <a class="ewa-brand" href="/" aria-label="일하는 AI 홈">
        <span class="ewa-brand-mark" aria-hidden="true">
          <i></i>
          <i></i>
          <i></i>
        </span>
        <span>
          <strong>일하는 AI</strong>
          <small>WORKING AI / FIELD NOTES</small>
        </span>
      </a>
      <nav class="ewa-main-nav" aria-label="주요 메뉴">
        {NAV_ITEMS.map((item) => (
          <a href={item.href} class="ewa-nav-link" data-nav-key={item.href.replace("/", "")}>
            {item.ko}
          </a>
        ))}
      </nav>
      <button type="button" class="ewa-menu-toggle" data-ewa-menu-toggle aria-label="메뉴 열기">
        <span></span>
        <span></span>
        <span></span>
      </button>
      <div class="ewa-mobile-nav" data-ewa-mobile-nav hidden>
        {NAV_ITEMS.map((item) => (
          <a href={item.href} class="ewa-mobile-nav-link">{item.ko}</a>
        ))}
      </div>
      <div class="ewa-header-actions">
        <div class="ewa-search" data-ewa-search>
          <button
            type="button"
            class="ewa-icon-button"
            data-ewa-search-trigger
            aria-label="검색 열기"
          >
            ⌕<span>Search</span>
          </button>
          <div class="ewa-search-panel" data-ewa-search-panel hidden>
            <div class="ewa-search-head">
              <span>SEARCH</span>
              <button type="button" data-ewa-search-close aria-label="검색 닫기">
                Esc
              </button>
            </div>
            <input
              type="search"
              data-ewa-search-input
              placeholder="찾고 싶은 주제를 입력하세요"
              autocomplete="off"
            />
            <div class="ewa-search-results" data-ewa-search-results>
              {searchItems.map((item) => (
                <a href={item.slug} data-search-text={`${item.title} ${item.description}`}>
                  <strong>{item.title}</strong>
                  <small>{item.description}</small>
                </a>
              ))}
            </div>
          </div>
        </div>
        <div class="ewa-lang-switcher" data-ewa-lang-switcher>
          <button type="button" data-lang="ko" class="is-active" aria-label="한국어">
            KO
          </button>
          <button type="button" data-lang="en" aria-label="English">
            EN
          </button>
          <button type="button" data-lang="ja" aria-label="日本語">
            JA
          </button>
        </div>
        <button type="button" class="ewa-theme-button" data-ewa-theme aria-label="다크 모드 전환">
          <span aria-hidden="true">◐</span>
        </button>
      </div>
    </div>
  )
}

export default (() => SiteHeader) satisfies QuartzComponentConstructor
