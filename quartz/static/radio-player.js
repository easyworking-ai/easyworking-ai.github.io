// 라디오 에피소드 선택기
// episodes.json에서 메타데이터를 불러와 에피소드 전환 처리
(function () {
  const EPISODES_URL = "/static/radio/episodes.json";
  const lang = document.documentElement.lang || document.querySelector("html[lang]")?.getAttribute("lang") || "ko";

  // 페이지에서 현재 언어 추출 (URL 기준: /en/radio, /ja/radio, /radio)
  const path = window.location.pathname;
  let currentLang = "ko";
  if (path.includes("/en/")) currentLang = "en";
  else if (path.includes("/ja/")) currentLang = "ja";

  const audio = document.getElementById("ep-audio");
  const source = document.getElementById("ep-source");
  const titleEl = document.getElementById("ep-title");
  const summaryEl = document.getElementById("ep-summary");
  const dateEl = document.getElementById("ep-date");
  const durationEl = document.getElementById("ep-duration");
  const labelEl = document.getElementById("ep-label");
  const numEl = document.getElementById("ep-num");
  const listEl = document.getElementById("ep-list");

  if (!audio || !source) return;

  // 에피소드 데이터 로드 (새 에피소드가 추가되면 자동 반영)
  fetch(EPISODES_URL)
    .then((r) => r.json())
    .then((data) => {
      const episodes = data.episodes || [];
      if (episodes.length === 0) return;

      // 에피소드 목록 동적 생성 (JSON에 새 에피소드 추가 시 자동 표시)
      rebuildList(episodes, currentLang);

      // 클릭 이벤트 바인딩
      document.querySelectorAll(".ewa-radio-archive-item").forEach(function (item) {
        item.addEventListener("click", function () {
          const epNum = parseInt(this.getAttribute("data-ep"), 10);
          const ep = episodes.find(function (e) { return e.num === epNum; });
          if (ep) selectEpisode(ep, currentLang, episodes.length);
        });
      });
    })
    .catch(function () {
      // JSON 로드 실패 시 정적 HTML에 있는 에피소드 그대로 사용
    });

  function rebuildList(episodes, lang) {
    if (!listEl) return;
    // 이미 항목이 있으면 유지 (정적 fallback), 없으면 생성
    if (listEl.children.length >= episodes.length) return;

    listEl.innerHTML = "";
    episodes.forEach(function (ep) {
      const div = document.createElement("div");
      div.className = "ewa-radio-archive-item";
      div.setAttribute("data-ep", ep.num);
      div.setAttribute("data-lang", lang);
      if (ep.num === episodes[0].num) div.classList.add("is-active");

      const title = (ep.title && ep.title[lang]) || ep.title.ko;
      const date = ep.date || "";
      const dur = ep.duration || "~3분";
      const langs = "한국어 · English · 日本語";

      div.innerHTML =
        '<span class="ewa-radio-archive-num">EP ' + String(ep.num).padStart(2, "0") + "</span>" +
        "<div><h4>" + title + "</h4>" +
        "<span>" + date + " · " + dur + " · " + langs + "</span></div>";

      div.addEventListener("click", function () {
        selectEpisode(ep, lang, episodes.length);
      });

      listEl.appendChild(div);
    });
  }

  function selectEpisode(ep, lang, total) {
    const title = (ep.title && ep.title[lang]) || ep.title.ko;
    const summary = (ep.summary && ep.summary[lang]) || ep.summary.ko;
    const audioUrl = (ep.audio && ep.audio[lang]) || ep.audio.ko;
    const date = ep.date || "";
    const dur = ep.duration || "~3분";

    if (titleEl) titleEl.textContent = title;
    if (summaryEl) summaryEl.textContent = summary;
    if (dateEl) dateEl.textContent = date;
    if (durationEl) durationEl.textContent = "⏱ " + dur;
    if (numEl) numEl.textContent = "EP " + String(ep.num).padStart(2, "0");
    if (labelEl) {
      const latestLabel = {
        ko: "Episode " + ep.num + " · 최신 에피소드",
        en: "Episode " + ep.num + " · Latest",
        ja: "Episode " + ep.num + " · 最新エピソード",
      };
      const oldLabel = {
        ko: "Episode " + ep.num,
        en: "Episode " + ep.num,
        ja: "Episode " + ep.num,
      };
      labelEl.textContent = ep.num === total ? (latestLabel[lang] || latestLabel.ko) : (oldLabel[lang] || oldLabel.ko);
    }

    // 오디오 소스 교체
    source.src = audioUrl;
    audio.load();

    // 활성 에피소드 표시
    document.querySelectorAll(".ewa-radio-archive-item").forEach(function (item) {
      item.classList.remove("is-active");
    });
    const active = document.querySelector('.ewa-radio-archive-item[data-ep="' + ep.num + '"]');
    if (active) active.classList.add("is-active");
  }
})();
