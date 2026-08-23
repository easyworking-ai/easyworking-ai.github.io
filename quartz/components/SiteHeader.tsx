import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

type Lang = "ko" | "en" | "ja"

const BRAND = {
  ko: { name: "일하는 AI", home: "일하는 AI 홈", tagline: "WORKING AI / FIELD NOTES", menu: "주요 메뉴", openMenu: "메뉴 열기", search: "검색 열기", closeSearch: "검색 닫기", placeholder: "찾고 싶은 주제를 입력하세요" },
  en: { name: "Working AI", home: "Working AI home", tagline: "WORKING AI / FIELD NOTES", menu: "Main menu", openMenu: "Open menu", search: "Open search", closeSearch: "Close search", placeholder: "Search a topic" },
  ja: { name: "働くAI", home: "働くAIホーム", tagline: "WORKING AI / FIELD NOTES", menu: "メインメニュー", openMenu: "メニューを開く", search: "検索を開く", closeSearch: "検索を閉じる", placeholder: "調べたいトピックを入力" },
} as const

const NAV_ITEMS: Array<{ key: string; ko: string; en: string; ja: string }> = [
  { key: "this-week.html", ko: "이번 주", en: "This Week", ja: "今週" },
  { key: "radio.html", ko: "라디오", en: "Radio", ja: "ラジオ" },
  { key: "youtube/", ko: "유튜브", en: "YouTube", ja: "YouTube" },
  { key: "guides.html", ko: "가이드", en: "Guides", ja: "ガイド" },
  { key: "learn.html", ko: "학습하기", en: "Learn", ja: "学ぶ" },
  { key: "play.html", ko: "체험하기", en: "Play", ja: "体験" },
]

const SiteHeader: QuartzComponent = ({ allFiles, fileData }: QuartzComponentProps) => {
  const lang: Lang = (String(fileData.frontmatter?.lang ?? "ko") as Lang) ?? "ko"
  const t = BRAND[lang] ?? BRAND.ko
  const prefix = lang === "ko" ? "" : `/${lang}`

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
          (lang === "ko"
            ? !slug.startsWith("en/") && !slug.startsWith("ja/")
            : slug.startsWith(`${lang}/`)) &&
          file.frontmatter?.title,
      )
    })
    .map((file) => ({
      title: String(file.frontmatter?.title ?? file.slug),
      slug: `/${file.slug}.html`,
      description: String(file.frontmatter?.description ?? ""),
    }))

  return (
    <div class="ewa-site-header" data-ewa-header>
      <a class="ewa-brand" href={lang === "ko" ? "/" : `${prefix}/`} aria-label={t.home}>
        <span class="ewa-brand-mark" aria-hidden="true">
          <i></i>
          <i></i>
          <i></i>
        </span>
        <span>
          <strong>{t.name}</strong>
          <small>{t.tagline}</small>
        </span>
      </a>
      <nav class="ewa-main-nav" aria-label={t.menu}>
        {NAV_ITEMS.map((item) => (
          <a
            href={`${prefix}/${item.key}`}
            class="ewa-nav-link"
            data-nav-key={item.key}
          >
            {item[lang]}
          </a>
        ))}
      </nav>
      <button type="button" class="ewa-menu-toggle" data-ewa-menu-toggle aria-label={t.openMenu}>
        <span></span>
        <span></span>
        <span></span>
      </button>
      <div class="ewa-mobile-nav" data-ewa-mobile-nav hidden>
        {NAV_ITEMS.map((item) => (
          <a class="ewa-mobile-nav-link" href={`${prefix}/${item.key}`}>
            {item[lang]}
          </a>
        ))}
      </div>
      <div class="ewa-header-actions">
        <div class="ewa-search" data-ewa-search>
          <button
            type="button"
            class="ewa-icon-button"
            data-ewa-search-trigger
            aria-label={t.search}
          >
            ⌕<span>Search</span>
          </button>
          <div class="ewa-search-panel" data-ewa-search-panel hidden>
            <div class="ewa-search-head">
              <span>SEARCH</span>
              <button type="button" data-ewa-search-close aria-label={t.closeSearch}>
                Esc
              </button>
            </div>
            <input
              type="search"
              data-ewa-search-input
              placeholder={t.placeholder}
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
          <button type="button" data-lang="ko" class={lang === "ko" ? "is-active" : ""} aria-label="한국어">
            KO
          </button>
          <button type="button" data-lang="en" class={lang === "en" ? "is-active" : ""} aria-label="English">
            EN
          </button>
          <button type="button" data-lang="ja" class={lang === "ja" ? "is-active" : ""} aria-label="日本語">
            JA
          </button>
        </div>
        <button type="button" class="ewa-theme-button" data-ewa-theme aria-label={lang === "ko" ? "다크 모드 전환" : lang === "ja" ? "ダークモード切替" : "Toggle dark mode"}>
          <span aria-hidden="true">◐</span>
        </button>
      </div>
    </div>
  )
}

export default (() => SiteHeader) satisfies QuartzComponentConstructor
