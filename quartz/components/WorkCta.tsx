import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const WorkCta: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const slug = String(fileData.slug ?? "")
  if (slug === "index" || slug === "work-with-me" || !fileData.frontmatter?.title) return null

  return (
    <aside class="ewa-inline-cta" aria-label="AI 시스템 구축 문의">
      <div>
        <span class="ewa-inline-cta-kicker">WORK WITH ME / AI OPERATIONS</span>
        <h2>읽은 내용을 실제 업무에 붙이고 싶다면</h2>
        <p>
          현재 업무 흐름을 1시간 동안 함께 살펴보고, AI를 적용했을 때 효과가 큰 지점을 정리해
          드립니다. 진단 리포트는 가져가셔도 됩니다.
        </p>
      </div>
      <a
        class="ewa-primary-action"
        href="mailto:aieeiee030303@gmail.com?subject=[AI 진단 신청] 회사명&body=회사명:%0A담당자명:%0A주요 업무:%0A현재 AI 사용 여부:%0A궁금한 점:"
      >
        무료 진단 신청 <span aria-hidden="true">→</span>
      </a>
    </aside>
  )
}

export default (() => WorkCta) satisfies QuartzComponentConstructor
