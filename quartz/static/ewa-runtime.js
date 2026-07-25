(() => {
  const bootHeader = () => {
    const header = document.querySelector('[data-ewa-header]')
    if (!header || header.dataset.runtimeReady === 'true') return
    header.dataset.runtimeReady = 'true'
    const search = header.querySelector('[data-ewa-search]')
    const panel = header.querySelector('[data-ewa-search-panel]')
    const input = header.querySelector('[data-ewa-search-input]')
    const results = header.querySelector('[data-ewa-search-results]')
    const setSearch = (open) => {
      if (!panel || !input) return
      panel.hidden = !open
      if (open) input.focus()
    }
    header.querySelector('[data-ewa-search-trigger]')?.addEventListener('click', () => setSearch(true))
    header.querySelector('[data-ewa-search-close]')?.addEventListener('click', () => setSearch(false))
    input?.addEventListener('input', () => {
      const query = input.value.trim().toLowerCase()
      results?.querySelectorAll('a').forEach((item) => {
        item.hidden = Boolean(query) && !(item.dataset.searchText || '').toLowerCase().includes(query)
      })
    })
    document.addEventListener('keydown', (event) => { if (event.key === 'Escape') setSearch(false) })
    document.addEventListener('click', (event) => { if (search && !search.contains(event.target)) setSearch(false) })
    header.querySelector('[data-ewa-theme]')?.addEventListener('click', () => {
      const root = document.documentElement
      const next = root.dataset.theme === 'dark' ? 'light' : 'dark'
      root.dataset.theme = next
      try { localStorage.setItem('ewa-theme', next) } catch (_) {}
    })
    try {
      const saved = localStorage.getItem('ewa-theme')
      if (saved) document.documentElement.dataset.theme = saved
    } catch (_) {}
  }

  const bootToc = () => {
    document.querySelectorAll('[data-ewa-toc]').forEach((toc) => {
      if (toc.dataset.runtimeReady === 'true') return
      const article = document.querySelector('.ewa-frame article')
      const list = toc.querySelector('[data-ewa-toc-list]')
      if (!article || !list) return
      const headings = [...article.querySelectorAll('h2, h3')]
      if (!headings.length) { toc.remove(); return }
      list.innerHTML = headings.map((heading, index) => {
        if (!heading.id) heading.id = `note-section-${index + 1}`
        return `<a class="ewa-toc-item ewa-toc-item--${heading.tagName.toLowerCase()}" href="#${heading.id}">${heading.textContent}</a>`
      }).join('')
      toc.dataset.runtimeReady = 'true'
    })
  }

  const toSeconds = (value) => {
    const match = value.replace(',', '.').match(/(\d+):(\d+):(\d+)(?:\.(\d+))?/)
    return match ? Number(match[1]) * 3600 + Number(match[2]) * 60 + Number(match[3]) + Number(`0.${match[4] || '0'}`) : 0
  }
  const parseSrt = (text) => text.trim().split(/\n\s*\n/).map((block) => {
    const lines = block.split(/\n/).map((line) => line.trim()).filter(Boolean)
    const time = lines.find((line) => line.includes('-->'))
    if (!time) return null
    const [start, end] = time.split('-->').map((value) => value.trim())
    return { start: toSeconds(start), end: toSeconds(end), text: lines.slice(lines.indexOf(time) + 1).join(' ') }
  }).filter(Boolean)

  const bootAudio = () => {
    document.querySelectorAll('[data-ewa-audio]').forEach((player) => {
      if (player.dataset.runtimeReady === 'true') return
      const audio = player.querySelector('audio')
      const transcript = player.querySelector('[data-audio-transcript]')
      const cues = []
      let current = -1
      if (!audio) return
      const renderCue = (index) => {
        if (!cues.length) return
        current = Math.max(0, Math.min(index, cues.length - 1))
        transcript?.querySelectorAll('[data-cue-index]').forEach((node) => node.classList.toggle('is-active', Number(node.dataset.cueIndex) === current))
        transcript?.querySelector(`[data-cue-index="${current}"]`)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
      }
      audio.addEventListener('timeupdate', () => {
        const index = cues.findIndex((cue) => audio.currentTime >= cue.start && audio.currentTime <= cue.end)
        if (index >= 0 && index !== current) renderCue(index)
      })
      player.querySelector('[data-audio-prev]')?.addEventListener('click', () => { renderCue(current - 1); audio.currentTime = cues[current]?.start || 0; audio.play() })
      player.querySelector('[data-audio-next]')?.addEventListener('click', () => { renderCue(current + 1); audio.currentTime = cues[current]?.start || 0; audio.play() })
      player.querySelector('[data-audio-replay]')?.addEventListener('click', () => { renderCue(current); audio.currentTime = cues[current]?.start || 0; audio.play() })
      player.querySelector('[data-audio-rate]')?.addEventListener('change', (event) => { audio.playbackRate = Number(event.target.value) })
      const subtitle = player.dataset.srt
      if (subtitle && transcript) {
        fetch(subtitle).then((response) => response.text()).then((text) => {
          cues.push(...parseSrt(text))
          transcript.innerHTML = cues.map((cue, index) => `<button type="button" data-cue-index="${index}">${cue.text}</button>`).join('')
          transcript.querySelectorAll('[data-cue-index]').forEach((button) => button.addEventListener('click', () => {
            renderCue(Number(button.dataset.cueIndex)); audio.currentTime = cues[current].start; audio.play()
          }))
        }).catch(() => { transcript.innerHTML = '<p>대본을 불러오지 못했습니다.</p>' })
      }
      player.dataset.runtimeReady = 'true'
    })
  }

  const boot = () => { bootHeader(); bootToc(); bootAudio() }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot)
  else boot()
  document.addEventListener('nav', boot)
  document.addEventListener('render', boot)
})()
