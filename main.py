from vad import vad
from asr import asr
from download import download
from multiprocessing import get_context
import numpy as np

speech_segments = []
import time
from gpt import gpt


# with get_context("fork").Pool(processes=4) as pool:
#     result = test_dataset1.map(
#         map_to_pred, batched=True, batch_size=4, fn_kwargs={"pool": pool}
#     )
def main(youtube_url):
    # download_audio(youtube_url)
    speech, time_stamps = vad("audio.wav")
    for i in time_stamps:
        duration = i["end"] / 16000 - i["start"] / 16000
        speech_segments.append((np.array(speech[i["start"] : i["end"]]), duration))
    transcript_lst = asr(speech_segments)
    all_transcript = ". ".join(transcript_lst)
    # conversation_history=[]
    # while True:
    #     prompt=input("Input: ")
    #     response, conversation_history=gpt(prompt,all_transcript,conversation_history)
    #     print("GPT: ", response)
    return all_transcript


# main(youtube_url="https://www.youtube.com/watch?v=4QVaSE9v7RE&t=3s")
