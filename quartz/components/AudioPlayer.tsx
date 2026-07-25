import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const AudioPlayer: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  if (fileData.slug === "index" || !fileData.frontmatter?.audio) return null
  const frontmatter = fileData.frontmatter
  const audio = String(frontmatter.audio)
  const subtitle = frontmatter.srt ? String(frontmatter.srt) : ""
  const title = String(frontmatter.audioTitle ?? frontmatter.title ?? "Audio version")
  const provider = frontmatter.audioProvider ? String(frontmatter.audioProvider) : ""

  return (
    <section class="ewa-audio-player" data-ewa-audio data-srt={subtitle} aria-label="오디오 학습 플레이어">
      <div class="ewa-audio-heading"><div><span class="ewa-section-kicker">LISTEN / SHADOW / REPEAT</span><strong>{title}</strong></div>{provider && <small>{provider}</small>}</div>
      <audio controls preload="metadata" src={audio}></audio>
      <div class="ewa-audio-controls"><button type="button" data-audio-prev>Previous</button><button type="button" data-audio-replay>Replay</button><button type="button" data-audio-next>Next</button><label>Speed <select data-audio-rate><option value="0.75">0.75x</option><option value="0.9">0.9x</option><option value="1" selected>1x</option><option value="1.15">1.15x</option></select></label><a href={audio} download>MP3 ↓</a>{subtitle && <a href={subtitle} download>SRT ↓</a>}</div>
      {subtitle && <div class="ewa-transcript" data-audio-transcript><p>대본을 불러오는 중입니다.</p></div>}
    </section>
  )
}

AudioPlayer.afterDOMLoaded = `
(() => {
  const parseSrt = (text) => text.trim().split(/\\n\\s*\\n/).map((block) => {
    const lines = block.split(/\\n/).map((line) => line.trim()).filter(Boolean)
    const time = lines.find((line) => line.includes('-->'))
    if (!time) return null
    const [start, end] = time.split('-->').map((value) => value.trim())
    const toSeconds = (value) => { const match = value.replace(',', '.').match(/(\\d+):(\\d+):(\\d+)(?:\\.(\\d+))?/); return match ? Number(match[1]) * 3600 + Number(match[2]) * 60 + Number(match[3]) + Number('0.' + (match[4] || '0')) : 0 }
    return { start: toSeconds(start), end: toSeconds(end), text: lines.slice(lines.indexOf(time) + 1).join(' ') }
  }).filter(Boolean)
  const boot = () => {
    document.querySelectorAll('[data-ewa-audio]').forEach((player) => {
      if (player.getAttribute('data-ready') === 'true') return
      const audio = player.querySelector('audio')
      const transcript = player.querySelector('[data-audio-transcript]')
      const rate = player.querySelector('[data-audio-rate]')
      const cues = []
      let current = -1
      if (!audio) return
      const renderCue = (index) => { current = Math.max(0, Math.min(index, cues.length - 1)); transcript?.querySelectorAll('[data-cue-index]').forEach((node) => node.classList.toggle('is-active', Number(node.getAttribute('data-cue-index')) === current)); transcript?.querySelector('[data-cue-index="' + current + '"]')?.scrollIntoView({ block: 'nearest', behavior: 'smooth' }) }
      audio.addEventListener('timeupdate', () => { const index = cues.findIndex((cue) => audio.currentTime >= cue.start && audio.currentTime <= cue.end); if (index >= 0 && index !== current) renderCue(index) })
      player.querySelector('[data-audio-prev]')?.addEventListener('click', () => { renderCue(current - 1); audio.currentTime = cues[current]?.start || 0; audio.play() })
      player.querySelector('[data-audio-next]')?.addEventListener('click', () => { renderCue(current + 1); audio.currentTime = cues[current]?.start || 0; audio.play() })
      player.querySelector('[data-audio-replay]')?.addEventListener('click', () => { audio.currentTime = cues[current]?.start || 0; audio.play() })
      rate?.addEventListener('change', () => { audio.playbackRate = Number(rate.value) })
      const srt = player.getAttribute('data-srt')
      if (srt && transcript) fetch(srt).then((response) => response.text()).then((text) => { cues.push(...parseSrt(text)); transcript.innerHTML = cues.map((cue, index) => '<button type="button" data-cue-index="' + index + '">' + cue.text + '</button>').join(''); transcript.querySelectorAll('[data-cue-index]').forEach((button) => button.addEventListener('click', () => { renderCue(Number(button.getAttribute('data-cue-index'))); audio.currentTime = cues[current].start; audio.play() })) }).catch(() => { transcript.innerHTML = '<p>대본을 불러오지 못했습니다.</p>' })
      player.setAttribute('data-ready', 'true')
    })
  }
  boot()
  document.addEventListener('nav', boot)
  document.addEventListener('render', boot)
})()
`

export default (() => AudioPlayer) satisfies QuartzComponentConstructor
