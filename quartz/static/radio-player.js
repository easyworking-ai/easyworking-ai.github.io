// 라디오 에피소드 선택기
// episodes.json에서 에피소드·오디오·오픈소스 링크를 불러온다.
(function () {
  const EPISODES_URL = "/static/radio/episodes.json";
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
  const linksEl = document.getElementById("ep-links");

  if (!audio || !source) return;

  fetch(EPISODES_URL)
    .then(function (response) {
      if (!response.ok) throw new Error("episodes.json request failed");
      return response.json();
    })
    .then(function (data) {
      const episodes = Array.isArray(data.episodes) ? data.episodes : [];
      if (episodes.length === 0) return;

      const latestNum = Number(data.latest) || Math.max.apply(null, episodes.map(function (ep) { return ep.num; }));
      rebuildList(episodes, currentLang, latestNum);

      // JSON의 latest를 기준으로 최신 에피소드와 링크를 초기 표시한다.
      const latest = episodes.find(function (ep) { return ep.num === latestNum; }) || episodes[episodes.length - 1];
      selectEpisode(latest, currentLang, latestNum);
    })
    .catch(function () {
      // JSON 로드 실패 시 정적 HTML fallback을 그대로 표시한다.
    });

  function localized(value, lang, fallback) {
    if (!value) return fallback || "";
    if (typeof value === "string") return value;
    return value[lang] || value.ko || value.en || value.ja || fallback || "";
  }

  function rebuildList(episodes, lang, latestNum) {
    if (!listEl) return;
    listEl.innerHTML = "";

    episodes.slice().sort(function (a, b) { return a.num - b.num; }).forEach(function (ep) {
      const item = document.createElement("div");
      item.className = "ewa-radio-archive-item" + (ep.num === latestNum ? " is-active" : "");
      item.setAttribute("data-ep", ep.num);
      item.setAttribute("data-lang", lang);
      item.setAttribute("role", "button");
      item.setAttribute("tabindex", "0");

      const num = document.createElement("span");
      num.className = "ewa-radio-archive-num";
      num.textContent = "EP " + String(ep.num).padStart(2, "0");

      const body = document.createElement("div");
      const title = document.createElement("h4");
      title.textContent = localized(ep.title, lang, "Episode " + ep.num);
      const meta = document.createElement("span");
      meta.textContent = (ep.date || "") + " · " + (ep.duration || "") + " · 한국어 · English · 日本語";
      body.appendChild(title);
      body.appendChild(meta);
      item.appendChild(num);
      item.appendChild(body);

      const activate = function () { selectEpisode(ep, lang, latestNum); };
      item.addEventListener("click", activate);
      item.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          activate();
        }
      });
      listEl.appendChild(item);
    });
  }

  function renderOpenSourceLinks(ep, lang) {
    if (!linksEl) return;
    const items = Array.isArray(ep.openSourceLinks) ? ep.openSourceLinks : [];
    linksEl.innerHTML = "";
    linksEl.hidden = items.length === 0;
    if (items.length === 0) return;

    const labels = {
      ko: "방송에서 언급한 오픈소스·개발 프로젝트",
      en: "Open-source projects mentioned",
      ja: "番組で紹介したオープンソース・開発プロジェクト",
    };
    const heading = document.createElement("div");
    heading.className = "ewa-radio-links-title";
    heading.textContent = labels[lang] || labels.ko;

    const list = document.createElement("ul");
    items.forEach(function (entry) {
      if (!entry || !/^https?:\/\//i.test(entry.url || "")) return;
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.href = entry.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = localized(entry.name, lang, entry.url);
      const description = document.createElement("span");
      description.textContent = localized(entry.description, lang, "");
      li.appendChild(link);
      if (description.textContent) li.appendChild(description);
      list.appendChild(li);
    });
    linksEl.appendChild(heading);
    linksEl.appendChild(list);
  }

  function selectEpisode(ep, lang, latestNum) {
    const title = localized(ep.title, lang, "Episode " + ep.num);
    const summary = localized(ep.summary, lang, "");
    const audioUrl = localized(ep.audio, lang, "");

    if (titleEl) titleEl.textContent = title;
    if (summaryEl) summaryEl.textContent = summary;
    if (dateEl) dateEl.textContent = ep.date || "";
    if (durationEl) durationEl.textContent = "⏱ " + (ep.duration || "");
    if (numEl) numEl.textContent = "EP " + String(ep.num).padStart(2, "0");
    if (labelEl) {
      const labels = {
        ko: ep.num === latestNum ? "Episode " + ep.num + " · 최신 에피소드" : "Episode " + ep.num,
        en: ep.num === latestNum ? "Episode " + ep.num + " · Latest" : "Episode " + ep.num,
        ja: ep.num === latestNum ? "Episode " + ep.num + " · 最新エピソード" : "Episode " + ep.num,
      };
      labelEl.textContent = labels[lang] || labels.ko;
    }

    if (audioUrl) {
      source.src = audioUrl;
      audio.load();
    }
    renderOpenSourceLinks(ep, lang);

    document.querySelectorAll(".ewa-radio-archive-item").forEach(function (item) {
      item.classList.toggle("is-active", Number(item.getAttribute("data-ep")) === ep.num);
    });
  }
})();
