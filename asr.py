from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import soundfile as sf
import torch
import streamlit as st
import numpy as np
import streamlit as st
import time
from multiprocessing import get_context


def asr(batch, processor, model, decoder):
    # Simulate work being done
    speech_batch = [i[0] for i in batch]
    start_batch = [i[1] for i in batch]
    inputs = processor(
        speech_batch, return_tensors="pt", padding="longest"
    )  # Batch size 1
    inputs = {k: v.to("cuda") for k, v in inputs.items()}
    # retrieve logits
    with torch.no_grad():
        logits = model(**inputs).logits.cpu().numpy()
    with get_context("fork").Pool(processes=4) as pool:
        res = decoder.decode_beams_batch(logits_list=logits, pool=pool, beam_width=50)
    transcript_lst = [i[0][0] for i in res]
    # take argmax and decode
    # predicted_ids = torch.argmax(logits, dim=-1)
    # transcript_lst = processor.batch_decode(predicted_ids)
    return transcript_lst, start_batch


if __name__ == "__main__":
    filepath = "/home4/khanhnd/VLSP/dev/wav/348-00000015-00000549.wav"
    speech = map_to_array(filepath)
    print(asr(speech))
