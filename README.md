# resolve-transcoder-davinci_resolve

Simple Python wrapper around `ffmpeg` to transcode videos into DNxHR or ProRes,  
so they can be imported and edited smoothly in DaVinci Resolve on Linux.

Resolve under Linux has poor support for some common codecs (H.264, HEVC, MKV).  
This script batch-converts them to intermediate formats used in professional workflows.

## Features
- Batch process files or folders
- Supports DNxHR (LB, SQ, HQ, 444) and ProRes
- Creates `.mov` files ready for Resolve
- Cross-platform (Linux/macOS/Windows if ffmpeg is available)

## Requirements
- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html) installed and in `$PATH`

## Usage

```bash
# DNxHR LB (proxy) by default
python resolve_transcoder.py video.mp4

# ProRes HQ
python resolve_transcoder.py myclip.mov -c prores

# DNxHR HQ for all files in a folder
python resolve_transcoder.py ./rushes -p hq
