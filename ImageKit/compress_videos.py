import subprocess
from pathlib import Path
import logging
from logs import add_file_handler
"""using ffmpeg compress all the video files in the given folder"""


def get_file_size(file: Path):
    size_in_bytes = file.stat().st_size
    # define units and thresholds
    units = ["B", "KB", "MB", "GB", "TB"]
    thresholds = [1024**i for i in range(len(units))]
    # find the appropriate unit
    for i in range(len(units) - 1):
        if size_in_bytes < thresholds[i + 1]:
            unit = units[i]
            threshold = thresholds[i]
            break
    else:
        unit = units[-1]
        threshold = thresholds[-1]
    # format the size
    return f"{size_in_bytes / threshold:.2f} {unit}"


def compress_video(source: Path, output: Path):
    args = [
        'ffmpeg', '-i', source, '-c:v', 'libx265', '-x265-params',
        'crf=18:preset=veryslow', '-c:a', 'copy', output
    ]
    args = [
        'ffmpeg', '-i', source, '-c:v', 'libx265', '-x265-params', 'crf=25',
        '-c:a', 'copy', output
    ]
    args = [
        'ffmpeg', '-i', source, '-c:v', 'libx265', '-x265-params', 'crf=28',
        '-c:a', 'copy', '-vf', 'scale=iw/1.3333:-1', output
    ]
    result = subprocess.run(args)

    if result.returncode == 0:
        logging.info('success %s: %s --> %s', source, get_file_size(source),
                     get_file_size(output))
    else:
        logging.error('failed processing: %s', source)


def batch_compress_videos(source: str, match="*.mp4"):
    source = Path(source)
    dest = source / 'output'
    if not source.exists():
        raise Exception(f"{source} doesn't exists")

    dest.mkdir(exist_ok=True)  # create output folder

    for video in source.rglob(match):
        compress_video(video, dest / video.name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s: %(message)s')
    add_file_handler('video_compression', 'video_compression.log')

    source = r'D:\Desktop\小米相册\屏幕录制\input'
    batch_compress_videos(source)
