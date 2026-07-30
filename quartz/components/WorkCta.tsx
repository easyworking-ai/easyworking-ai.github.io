import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

// 무료 진단 신청 CTA — 사용 중지
const WorkCta: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  return null
}

export default (() => WorkCta) satisfies QuartzComponentConstructor
