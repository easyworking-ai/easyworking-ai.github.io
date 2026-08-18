import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

type Lang = "ko" | "en" | "ja"

const T = {
  ko: { name: "일하는 AI", tagline: "AI를 실제 일에 붙이는 사람들을 위한 현장 기록.", links: { home: "홈", notes: "현장 기록" } },
  en: { name: "Working AI", tagline: "Field notes for people putting AI into real work.", links: { home: "Home", notes: "Field notes" } },
  ja: { name: "働くAI", tagline: "AIを実際の仕事に組み込む人のための現場記録。", links: { home: "ホーム", notes: "現場記録" } },
} as const

const SiteFooter: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const lang: Lang = (String(fileData.frontmatter?.lang ?? "ko") as Lang) ?? "ko"
  const t = T[lang] ?? T.ko
  const home = lang === "ko" ? "/" : `/${lang}/`
  return (
    <footer class="ewa-site-footer">
      <div class="ewa-footer-brand"><span class="ewa-brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><strong>{t.name}</strong></div>
      <p>{t.tagline}</p>
      <div class="ewa-footer-links"><a href={home}>{t.links.home}</a><a href="/wiki/concepts/agent-runtime-reliability">{t.links.notes}</a><a href="https://github.com/easyworking-ai/easyworking-ai.github.io">GitHub</a></div>
      <small>© 2026 EasyWorking-AI. Sources are credited on each note.</small>
    </footer>
  )
}

export default (() => SiteFooter) satisfies QuartzComponentConstructor
