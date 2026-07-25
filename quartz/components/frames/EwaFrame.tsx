import { PageFrame } from "./types"
import SiteHeaderConstructor from "../SiteHeader"
import SiteFooterConstructor from "../SiteFooter"
import ArticleChromeConstructor from "../ArticleChrome"
import ArticleTocConstructor from "../ArticleToc"
import AudioPlayerConstructor from "../AudioPlayer"

const SiteHeader = SiteHeaderConstructor()
const SiteFooter = SiteFooterConstructor()
const ArticleChrome = ArticleChromeConstructor()
const ArticleToc = ArticleTocConstructor()
const AudioPlayer = AudioPlayerConstructor()

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
        </main>
        <SiteFooter {...componentData} />
        <script src="/static/ewa-runtime.js" defer></script>
      </>
    )
  },
}
