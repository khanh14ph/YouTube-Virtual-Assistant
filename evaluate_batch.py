from datasets import load_dataset
from evaluate import load

wer = load("wer")
# English
fleurs = load_dataset("google/fleurs", "en_us", split="test")

from transformers import Wav2Vec2ForCTC, AutoProcessor
import torch

model_id = "facebook/mms-1b-all"

processor = AutoProcessor.from_pretrained(model_id)
model = Wav2Vec2ForCTC.from_pretrained(model_id)
model.eval()
model.to("cuda")

processor.tokenizer.set_target_lang("eng")
model.load_adapter("eng")

def speech_file_to_array_fn(batch):
    

def evaluate(batch):
    inputs = processor(batch['audio']['array'], sampling_rate=16_000, return_tensors="pt").to("con_cu")
    with torch.no_grad():
        outputs = model(**inputs).logits

    ids = torch.argmax(outputs, dim=-1)
    transcription = processor.batch_decode(ids)
    batch["prediction"] = transcription
    return batch

result = fleurs.map(evaluate, batched=True, batch_size=32)
print("WER: {:2f}".format(100 * wer.compute(predictions=result["prediction"], references=result["transcription"])))


