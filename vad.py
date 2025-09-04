import torch

torch.set_num_threads(1)
model, utils = torch.hub.load(repo_or_dir="snakers4/silero-vad", model="silero_vad")


def vad(filepath):

    (get_speech_timestamps, _, read_audio, _, _) = utils

    wav = read_audio(filepath)  # backend (sox, soundfile, or ffmpeg) required!
    speech_timestamps = get_speech_timestamps(wav, model)
    return wav, speech_timestamps


if __name__ == "__main__":
    print(vad("audio.wav"))
