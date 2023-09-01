from pytube import YouTube, StreamQuery, Stream
import os
import re
from pytube import Channel


def get_latest_video(channel_url) -> str:
    channel = Channel(channel_url)
    return channel.video_urls[0]


def remove_special_characters(s):
    return re.sub(r'[^a-zA-Z0-9]', '', s)


def get_max_res(video_streams: StreamQuery, audio_streams: StreamQuery = None, file_name="temp"):
    # Create path if dones't exist
    if not os.path.exists(f"../videos/temp"):
        os.makedirs(f"../videos/temp")
    os.chdir(f"../videos/temp")
    pos_file_name = remove_special_characters(file_name)

    first_stream: Stream = video_streams.first()
    print("Downloading video file...")
    # Change name of download to video-{video-name} if not progressive
    first_stream.download(
        filename_prefix="video-" if not first_stream.is_progressive else "")
    # Download audio if not progressive
    if not first_stream.is_progressive:
        print("Audio file not found!\nDonwloading audio file...")
        audio_streams.first().download(filename_prefix="audio-")
        files = [f for f in os.listdir(
            ".") if os.path.isfile(os.path.join(".", f))]
        if len(files) < 2:
            raise IndexError("No audio source was found. Aborting!")
        # Joins audio and video with ffmpeg
        os.system(
            'ffmpeg -i "{}" -i "{}" -c:v copy -c:a aac -strict experimental "{}".mp4'.format(*files, pos_file_name))

    for file in files:
        os.remove(file)


def get_video_streams(yt: YouTube) -> StreamQuery:
    video_streams = yt.streams.order_by(
        "resolution").filter(type="video").desc()
    return {"video_streams": video_streams, "title": yt.title}


def get_audio_streams(yt: YouTube) -> StreamQuery:
    audio_streams = yt.streams.order_by("abr").filter(type="audio").desc()
    return audio_streams


def create_yt(url: str) -> YouTube:
    return YouTube(url)
