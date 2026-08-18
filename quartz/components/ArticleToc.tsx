import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const TOC_LABELS: Record<string, { aria: string; empty: string }> = {
  ko: { aria: "이 글의 흐름", empty: "읽는 흐름을 불러오는 중" },
  en: { aria: "In this note", empty: "Loading sections" },
  ja: { aria: "この記事の流れ", empty: "セクションを読み込み中" },
}

const ArticleToc: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  if (fileData.slug === "index" || !fileData.frontmatter?.title) return null
  const langKey = String(fileData.frontmatter?.lang ?? "ko")
  const t = TOC_LABELS[langKey] ?? TOC_LABELS.ko
  return <aside class="ewa-article-toc" data-ewa-toc aria-label={t.aria}><span class="ewa-toc-label">IN THIS NOTE</span><nav data-ewa-toc-list><span class="ewa-toc-empty">{t.empty}</span></nav></aside>
}

ArticleToc.afterDOMLoaded = `
(() => {
  const boot = () => {
    document.querySelectorAll('[data-ewa-toc]').forEach((toc) => {
      const article = document.querySelector('.ewa-frame article')
      const list = toc.querySelector('[data-ewa-toc-list]')
      if (!article || !list || toc.getAttribute('data-ready') === 'true') return
      const headings = Array.from(article.querySelectorAll('h2, h3'))
      if (!headings.length) { toc.remove(); return }
      list.innerHTML = headings.map((heading, index) => {
        if (!heading.id) heading.id = 'note-section-' + (index + 1)
        return '<a class="ewa-toc-item ewa-toc-item--' + heading.tagName.toLowerCase() + '" href="#' + heading.id + '">' + heading.textContent + '</a>'
      }).join('')
      toc.setAttribute('data-ready', 'true')
    })
  }
  boot()
  document.addEventListener('nav', boot)
  document.addEventListener('render', boot)
})()
`

export default (() => ArticleToc) satisfies QuartzComponentConstructor
