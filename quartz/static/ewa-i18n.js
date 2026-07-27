// 다국어 언어 전환기 + 라우팅 런타임
// 루트(/) = 한국어(기본), /en/ = 영어, /ja/ = 일본어
(() => {
  const LANGS = ['ko', 'en', 'ja']
  const DEFAULT_LANG = 'ko'
  const STORAGE_KEY = 'ewa-lang'

  const detectLang = () => {
    // 1. localStorage
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      if (saved && LANGS.includes(saved)) return saved
    } catch (_) {}
    // 2. URL path
    const path = window.location.pathname
    for (const lang of LANGS) {
      if (lang !== DEFAULT_LANG && path.startsWith(`/${lang}/`)) return lang
    }
    // 3. browser
    const browser = (navigator.language || '').slice(0, 2).toLowerCase()
    if (LANGS.includes(browser)) return browser
    return DEFAULT_LANG
  }

  const switchLang = (lang) => {
    try { localStorage.setItem(STORAGE_KEY, lang) } catch (_) {}
    const path = window.location.pathname
    // 현재 경로에서 언어 prefix를 추출하거나 제거
    let base = path
    for (const l of LANGS) {
      if (l !== DEFAULT_LANG && path.startsWith(`/${l}/`)) {
        base = path.slice(`/${l}`.length)
        break
      }
    }
    if (!base.startsWith('/')) base = '/' + base
    // 루트 인덱스 정규화
    if (base === '/' || base === '/index.html') base = '/'
    
    const target = lang === DEFAULT_LANG ? base : `/${lang}${base === '/' ? '/' : base}`
    window.location.href = target
  }

  const getCurrentLang = () => {
    const path = window.location.pathname
    for (const lang of LANGS) {
      if (lang !== DEFAULT_LANG && path.startsWith(`/${lang}/`)) return lang
    }
    return DEFAULT_LANG
  }

  // 언어 전환기 부팅
  const bootLangSwitcher = () => {
    document.querySelectorAll('[data-ewa-lang-switcher]').forEach((switcher) => {
      if (switcher.dataset.runtimeReady === 'true') return
      const current = getCurrentLang()
      switcher.querySelectorAll('[data-lang]').forEach((btn) => {
        const lang = btn.dataset.lang
        if (lang === current) btn.classList.add('is-active')
        btn.addEventListener('click', () => switchLang(lang))
      })
      switcher.dataset.runtimeReady = 'true'
    })
  }

  // 전역 접근
  window.EWA = window.EWA || {}
  window.EWA.lang = { detect: detectLang, current: getCurrentLang, switch: switchLang }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bootLangSwitcher)
  else bootLangSwitcher()
  document.addEventListener('nav', bootLangSwitcher)
  document.addEventListener('render', bootLangSwitcher)
})()
