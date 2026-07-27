import { PageFrame } from "./types"
import SiteHeaderConstructor from "../SiteHeader"
import SiteFooterConstructor from "../SiteFooter"
import ArticleChromeConstructor from "../ArticleChrome"
import ArticleTocConstructor from "../ArticleToc"
import AudioPlayerConstructor from "../AudioPlayer"
import WorkCtaConstructor from "../WorkCta"

const SiteHeader = SiteHeaderConstructor()
const SiteFooter = SiteFooterConstructor()
const ArticleChrome = ArticleChromeConstructor()
const ArticleToc = ArticleTocConstructor()
const AudioPlayer = AudioPlayerConstructor()
const WorkCta = WorkCtaConstructor()

export const EwaFrame: PageFrame = {
  name: "ewa",
  render({ componentData, pageBody: Content, footer: _Footer }) {
    return (
      <>
        <SiteHeader {...componentData} />
        <main class="ewa-frame">
          <ArticleChrome {...componentData} />
          <AudioPlayer {...componentData} />
          <ArticleToc {...componentData} />
          <Content {...componentData} />
          <WorkCta {...componentData} />
        </main>
        <SiteFooter {...componentData} />
        <script src="/static/ewa-i18n.js" defer></script>
        <script src="/static/ewa-runtime.js" defer></script>
      </>
    )
  },
}
