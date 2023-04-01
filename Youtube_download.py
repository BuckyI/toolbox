from pytube import YouTube
import os
import re
import argparse


def modified_filename(stream):
    return re.sub(r"(.*?)\.", r"\g<1> - YouTube.", stream.default_filename)


def download_video(url):
    video = YouTube(url)
    stream = video.streams.get_highest_resolution()
    filename = modified_filename(stream)
    stream.download(filename=filename)
    return


def download_music(url):
    video = YouTube(url)
    stream = video.streams.filter(only_audio=True).last()  # 最后一个是音质最好的
    filename = modified_filename(stream)
    stream.download(filename=filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download YouTube video/music at the highest resolution.")
    parser.add_argument("--type",
                        help="choose: video / music",
                        default="video")
    parser.add_argument("urls", nargs='+', help="YouTube video's url")
    args = parser.parse_args()

    assert args.type in ['video', 'music'], 'invalid type!'

    for url in args.urls:
        video = YouTube(url)
        if args.type == "video":
            stream = video.streams.get_highest_resolution()
        elif args.type == "music":
            # 最后一个是音质最好的
            stream = video.streams.filter(only_audio=True).last()
        filename = modified_filename(stream)
        stream.download(filename=filename)
        print("download completed:", filename)
