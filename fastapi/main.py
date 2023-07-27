from fastapi import FastAPI
import uvicorn
import json
from typing import List, Union
from pydantic import BaseModel
from transformers import AutoTokenizer, LlamaForCausalLM
import torch
from huggingface_hub import login
import time


app = FastAPI()


# huggingface login
with open('../huggingface_login.json', 'r') as f:
    huggingface_token = json.load(f)
    login(token=huggingface_token["llama2"])


## model load
print(f"model loading")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf").to(device)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
print("model loading complite")


class Chat(BaseModel):
    prompt: str
    text: str


@app.post('/text-llama')
def chat(inputs: Chat):
    start_time = time.time()
    # gc.collect()
    torch.cuda.empty_cache()
    inputs = tokenizer(inputs.prompt+inputs.text, return_tensors="pt").to(device)
    generate_ids = model.generate(inputs.input_ids, max_length=1024)
    result = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    end_time = time.time()

    print(end_time-start_time)

    return result
    

# if __name__=="__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=40001) # 자신의 포트 번호
