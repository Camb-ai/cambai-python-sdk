import typing
import shutil
import subprocess


def stream(audio_stream: typing.Iterator[bytes]) -> bytes:
    if shutil.which("gst-play-1.0") is None:
        message = (
            "Audio streaming requires `gst-play-1.0`, but it was not found on your system."
            "On macOS, type `brew install gstreamer` to install it."
            "On Ubuntu, type `sudo apt install gstreamer1.0-plugins-base-apps` to install it."
        )
        raise ValueError(message)

    gst_play_command = ["gst-play-1.0", "--no-interactive", "fd://0"]
    gst_play_process = subprocess.Popen(
        gst_play_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    audio = b""
    for chunk in audio_stream:
        if chunk is not None:
            gst_play_process.stdin.write(chunk)
            gst_play_process.stdin.flush()
            audio += chunk
    if gst_play_process.stdin:
        gst_play_process.stdin.close()
    gst_play_process.wait()
    return audio


def capture() -> typing.Iterator[bytes]:
    if shutil.which("gst-launch-1.0") is None:
        message = (
            "Audio capture requires `gst-launch-1.0`, but it was not found on your system."
            "On macOS, type `brew install gstreamer` to install it."
            "On Ubuntu, type `sudo apt install gstreamer1.0-tools` to install it."
        )
        raise ValueError(message)

    gst_launch_command = [
        "gst-launch-1.0",
        "autoaudiosrc", "!",
        "audioconvert", "!", "audioresample", "!",
        "audio/x-raw,format=S16LE,rate=16000", "!",
        "fdsink", "fd=1"
    ]
    
    process = subprocess.Popen(
        gst_launch_command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        universal_newlines=False  # Read bytes, not text
    )
    
    try:
        while True:
            chunk = process.stdout.read(16384) # Read approx. half a second at a time
            if not chunk:
                break  # EOS
            yield chunk  # Yield the chunk of audio data
    finally:
        process.stdout.close()
        process.wait()