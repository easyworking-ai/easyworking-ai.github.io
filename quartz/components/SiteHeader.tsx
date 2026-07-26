import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

function itemTitle(file: QuartzComponentProps["allFiles"][number]): string {
  return String(file.frontmatter?.title ?? file.slug ?? "Untitled")
}

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
        file.frontmatter?.title,
      )
    })
    .map((file) => ({
      title: itemTitle(file),
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
          <small>FIELD NOTES / 2026</small>
        </span>
      </a>
      <nav class="ewa-main-nav" aria-label="주요 메뉴">
        <details class="ewa-nav-menu">
          <summary>
            Explore <span aria-hidden="true">+</span>
          </summary>
          <div class="ewa-nav-panel">
            <a href="/wiki/concepts/agent-runtime-reliability">
              <b>개념</b>
              <small>작동 원리와 실행 구조</small>
            </a>
            <a href="/tags/ai-agent">
              <b>연구</b>
              <small>근거와 출처를 따라가기</small>
            </a>
            <a href="/tags/agent-operations">
              <b>운영</b>
              <small>현업에서 재현하는 방법</small>
            </a>
            <a href="/tags/ai-infrastructure">
              <b>도구</b>
              <small>작업 환경과 기술 선택</small>
            </a>
          </div>
        </details>
        <a href="/wiki/concepts/agent-runtime-reliability">첫 번째 글</a>
        <a href="#ewa-content-map">사이트 지도</a>
        <a href="/work-with-me" class="ewa-nav-work">
          함께 일하기
        </a>
      </nav>
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
              <span>SEARCH THE FIELD NOTES</span>
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
        <button type="button" class="ewa-theme-button" data-ewa-theme aria-label="다크 모드 전환">
          <span aria-hidden="true">◐</span>
        </button>
        <a class="ewa-header-cta" href="/work-with-me">
          함께 일하기 <span aria-hidden="true">↗</span>
        </a>
      </div>
    </div>
  )
}

SiteHeader.afterDOMLoaded = `
(() => {
  const boot = () => {
    const header = document.querySelector('[data-ewa-header]')
    if (!header || header.getAttribute('data-ready') === 'true') return
    header.setAttribute('data-ready', 'true')
    const search = header.querySelector('[data-ewa-search]')
    const panel = header.querySelector('[data-ewa-search-panel]')
    const input = header.querySelector('[data-ewa-search-input]')
    const open = header.querySelector('[data-ewa-search-trigger]')
    const close = header.querySelector('[data-ewa-search-close]')
    const results = header.querySelector('[data-ewa-search-results]')
    const theme = header.querySelector('[data-ewa-theme]')
    const setSearch = (visible) => {
      if (!panel || !input) return
      panel.hidden = !visible
      if (visible) input.focus()
    }
    open?.addEventListener('click', () => setSearch(true))
    close?.addEventListener('click', () => setSearch(false))
    input?.addEventListener('input', () => {
      const query = input.value.trim().toLowerCase()
      results?.querySelectorAll('a').forEach((item) => {
        item.hidden = query !== '' && !(item.getAttribute('data-search-text') || '').toLowerCase().includes(query)
      })
    })
    document.addEventListener('keydown', (event) => { if (event.key === 'Escape') setSearch(false) })
    document.addEventListener('click', (event) => { if (search && !search.contains(event.target)) setSearch(false) })
    theme?.addEventListener('click', () => {
      const root = document.documentElement
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'
      root.setAttribute('data-theme', next)
      localStorage.setItem('ewa-theme', next)
    })
    const savedTheme = localStorage.getItem('ewa-theme')
    if (savedTheme) document.documentElement.setAttribute('data-theme', savedTheme)
  }
  boot()
  document.addEventListener('nav', boot)
  document.addEventListener('render', boot)
})()
`

export default (() => SiteHeader) satisfies QuartzComponentConstructor
