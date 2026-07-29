#!/usr/bin/env python3
"""Assemble the expanded EP02 English and Japanese radio episodes."""
from pathlib import Path
import subprocess

BASE = Path('/Users/macbook/easyworking-ai.github.io')
SCRIPT_DIR = BASE / 'scripts/ep02-voice-proofs'
OUTPUT_DIR = BASE / 'quartz/static/radio'

LANGS = {
    'en': ('en_iro_exp', 'en_loop_exp'),
    'ja': ('ja_iro_exp', 'ja_loop_exp'),
}


def run(*args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path):
    result = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def assemble(lang, iro_dir, loop_dir):
    work = SCRIPT_DIR / f'{lang}_expanded_assemble'
    work.mkdir(exist_ok=True)

    segments = []
    for index in range(1, 19):
        for speaker, folder in (('iro', iro_dir), ('loop', loop_dir)):
            source = SCRIPT_DIR / folder / f'output_{index:03d}.wav'
            if not source.exists():
                raise FileNotFoundError(source)
            normalized = work / f'{index:03d}_{speaker}.wav'
            run(
                'ffmpeg', '-y', '-i', str(source),
                '-ar', '44100', '-ac', '1',
                '-af', 'loudnorm=I=-18:TP=-1.5:LRA=11',
                str(normalized),
            )
            segments.append(normalized)

    silences = {
        'short': work / 'sil_short.wav',
        'medium': work / 'sil_medium.wav',
        'section': work / 'sil_section.wav',
    }
    for name, seconds in (('short', 0.30), ('medium', 0.60), ('section', 1.20)):
        run(
            'ffmpeg', '-y', '-f', 'lavfi',
            '-i', 'anullsrc=channel_layout=mono:sample_rate=44100',
            '-t', str(seconds), str(silences[name]),
        )

    # Five thematic blocks: intro, Opus 5, Hugging Face incident,
    # weekly roundup, and the practical experiment/outro.
    section_after_pair = {5, 10, 14, 18}
    entries = [SCRIPT_DIR / 'intro_sting.wav', silences['medium']]
    for pair_number in range(1, 19):
        iro_segment, loop_segment = segments[(pair_number - 1) * 2:(pair_number) * 2]
        entries.extend([iro_segment, silences['medium'], loop_segment])
        if pair_number in section_after_pair:
            entries.extend([silences['section'], SCRIPT_DIR / 'transition.wav', silences['section']])
        else:
            entries.append(silences['medium'])
    entries.extend([silences['section'], SCRIPT_DIR / 'outro_sting.wav'])

    concat_file = work / 'concat.txt'
    concat_file.write_text('\n'.join(f"file '{path}'" for path in entries) + '\n')
    raw = work / f'{lang}_expanded_raw.wav'
    run('ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat_file), '-c', 'copy', str(raw))

    raw_duration = duration(raw)
    fade_start = max(0.0, raw_duration - 3.0)
    final = OUTPUT_DIR / f'episode-02-{lang}.mp3'
    subprocess.run([
        'ffmpeg', '-y',
        '-i', str(raw),
        '-i', str(SCRIPT_DIR / 'bg_music.wav'),
        '-filter_complex',
        f'[1:a]volume=0.10,afade=t=in:st=0:d=2,afade=t=out:st={fade_start:.3f}:d=3[bg];'
        '[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0,'
        'loudnorm=I=-16:TP=-1.5:LRA=11',
        '-b:a', '128k', str(final),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    print(f'{lang.upper()}: {duration(final):.2f}s, {final.stat().st_size / 1024 / 1024:.2f}MB')


if __name__ == '__main__':
    for language, folders in LANGS.items():
        assemble(language, *folders)
