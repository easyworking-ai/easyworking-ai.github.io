import { QuartzComponent, QuartzComponentConstructor } from "./types"

// 무료 진단 신청 CTA — 사용 중지
const WorkCta: QuartzComponent = () => null

export default (() => WorkCta) satisfies QuartzComponentConstructor
