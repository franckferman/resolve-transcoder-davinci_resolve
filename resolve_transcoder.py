#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from pathlib import Path

# Profils DNxHR possibles
DNXHR_PROFILES = {
    "lb": "dnxhr_lb",   # Low Bandwidth (proxy léger)
    "sq": "dnxhr_sq",   # Standard Quality
    "hq": "dnxhr_hq",   # High Quality
    "444": "dnxhr_444"  # Full RGB 4:4:4
}

def convert_file(input_file: Path, output_dir: Path, profile: str, codec: str):
    base_name = input_file.stem
    output_file = output_dir / f"{base_name}.mov"

    if codec == "dnxhr":
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", str(input_file),
            "-c:v", "dnxhd", "-profile:v", DNXHR_PROFILES[profile],
            "-pix_fmt", "yuv422p",
            "-c:a", "pcm_s16le",
            str(output_file)
        ]
    elif codec == "prores":
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", str(input_file),
            "-c:v", "prores_ks", "-profile:v", "3",
            "-pix_fmt", "yuv422p10le",
            "-c:a", "pcm_s16le",
            str(output_file)
        ]
    else:
        print(f"[!] Codec non supporté: {codec}")
        return

    print(f"[+] Conversion: {input_file} -> {output_file}")
    subprocess.run(ffmpeg_cmd, check=True)

def collect_videos(paths):
    videos = []
    exts = [".mp4", ".MP4", ".mov", ".MOV", ".mkv", ".MKV"]
    for p in paths:
        p = Path(p)
        if p.is_file() and p.suffix in exts:
            videos.append(p)
        elif p.is_dir():
            for file in p.rglob("*"):
                if file.suffix in exts:
                    videos.append(file)
    return videos

def main():
    parser = argparse.ArgumentParser(description="Transcode des vidéos pour DaVinci Resolve (DNxHR/ProRes)")
    parser.add_argument("paths", nargs="+", help="Fichiers ou dossiers à convertir")
    parser.add_argument("-o", "--output", default="converted", help="Dossier de sortie (par défaut: ./converted)")
    parser.add_argument("-c", "--codec", choices=["dnxhr", "prores"], default="dnxhr", help="Codec cible (par défaut: dnxhr)")
    parser.add_argument("-p", "--profile", choices=DNXHR_PROFILES.keys(), default="lb", help="Profil DNxHR (par défaut: lb)")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    videos = collect_videos(args.paths)
    if not videos:
        print("[!] Aucun fichier vidéo trouvé.")
        sys.exit(1)

    for video in videos:
        try:
            convert_file(video, output_dir, args.profile, args.codec)
        except subprocess.CalledProcessError:
            print(f"[!] Erreur lors de la conversion: {video}")

if __name__ == "__main__":
    main()

