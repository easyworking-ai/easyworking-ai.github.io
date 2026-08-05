import importlib.util
import shutil
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("publish_weekly_radio.py")
spec = importlib.util.spec_from_file_location("radio_pipeline", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load {SCRIPT}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RadioPipelineTests(unittest.TestCase):
    def make_draft(self, status="draft") -> str:
        lines = []
        for lang in ("ko", "en", "ja"):
            lines.append(f"## Dialogue: {lang}\n")
            for index in range(1, 21):
                speaker = "iro" if index % 2 else "loop"
                section = "opening" if index <= 4 else "topic-1" if index <= 12 else "closing"
                text = {
                    "ko": "이번 주 소식을 실제 업무 관점에서 살펴봅니다.",
                    "en": "Let's look at this week's story from a work perspective.",
                    "ja": "今週の話題を仕事の視点から見ていきます。",
                }[lang]
                lines.append(f"### {index:03d} · {speaker} · {section}\n\n{text}\n")
        draft = textwrap.dedent("""---
 schema_version: 1
 episode: 2
 status: %s
 date: 2026-08-10
 created_at: 2026-08-10T09:00:00+09:00
 approved_at:
 published_at:
 title_ko: 테스트 제목
 title_en: Test title
 title_ja: テストタイトル
 summary_ko: 테스트 요약입니다.
 summary_en: Test summary.
 summary_ja: テスト概要です。
---

## Sources

- [Source A](https://example.com/a)
- [Source B](https://example.com/b)
- [Source C](https://example.com/c)

## Editorial notes

- topic-1: 무엇이 달라지는지 확인

%s
""" % (status, "\n".join(lines)))
        return draft.replace("\n ", "\n")

    def test_parse_and_validate_markdown_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "draft-ep02.md"
            path.write_text(self.make_draft(), encoding="utf-8")
            draft = module.parse_draft(path)
            module.validate_draft(draft, latest=1)
            self.assertEqual(draft["episode"], 2)
            self.assertEqual(len(draft["_dialogues"]["ko"]), 20)
            self.assertEqual(draft["_dialogues"]["ko"][0]["speaker"], "iro")

    def test_forbidden_korean_phrase_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "draft-ep02.md"
            path.write_text(self.make_draft().replace("실제 업무 관점", "신호 관점", 1), encoding="utf-8")
            draft = module.parse_draft(path)
            with self.assertRaises(module.PipelineError):
                module.validate_draft(draft, latest=1)

    def test_status_update_preserves_markdown_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "draft-ep02.md"
            original = self.make_draft()
            path.write_text(original, encoding="utf-8")
            module.update_draft_status(path, "approved", timestamp_key="approved_at")
            updated = path.read_text(encoding="utf-8")
            self.assertIn("status: approved", updated)
            self.assertRegex(updated, r"approved_at: .+")
            self.assertIn("## Dialogue: ko", updated)
            self.assertIn("### 020 · loop · closing", updated)

    def test_episode_metadata_and_static_page_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            record = {
                "num": 2,
                "title": {"ko": "새 제목", "en": "New title", "ja": "新しいタイトル"},
                "date": "2026-08-10",
                "duration": "~3분",
                "summary": {"ko": "새 요약", "en": "New summary", "ja": "新しい概要"},
                "audio": {
                    "ko": "/static/radio/episode-02-ko.mp3",
                    "en": "/static/radio/episode-02-en.mp3",
                    "ja": "/static/radio/episode-02-ja.mp3",
                },
            }
            source = module.ROOT / "content/radio.md"
            page = tmp_path / "radio.md"
            shutil.copy2(source, page)
            updated = module.update_radio_page(page, "ko", record)
            page.write_text(updated, encoding="utf-8")
            text = page.read_text(encoding="utf-8")
            self.assertIn("EP 02", text)
            self.assertIn("새 제목", text)
            self.assertIn("episode-02-ko.mp3", text)
            self.assertIn('data-ep="2"', text)

            data = {"episodes": [{"num": 1}], "latest": 1}
            result = module.update_episodes(data, record)
            self.assertEqual(result["latest"], 2)
            self.assertEqual([ep["num"] for ep in result["episodes"]], [1, 2])
            self.assertEqual(data["latest"], 1)


if __name__ == "__main__":
    unittest.main()
