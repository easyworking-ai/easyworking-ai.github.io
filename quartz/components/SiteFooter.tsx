import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const SiteFooter: QuartzComponent = ({ cfg }: QuartzComponentProps) => (
  <footer class="ewa-site-footer">
    <div class="ewa-footer-brand"><span class="ewa-brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><strong>{cfg.pageTitle}</strong></div>
    <p>AI를 실제 일에 붙이는 사람들을 위한 현장 기록.</p>
    <div class="ewa-footer-links"><a href="/">Home</a><a href="/wiki/concepts/agent-runtime-reliability">Field notes</a><a href="https://github.com/easyworking-ai/easyworking-ai.github.io">GitHub</a></div>
    <small>© 2026 EasyWorking-AI. Sources are credited on each note.</small>
  </footer>
)

export default (() => SiteFooter) satisfies QuartzComponentConstructor
