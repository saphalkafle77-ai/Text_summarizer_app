from fastapi import FastAPI, Requests
from pydantic import BaseModel
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import re
from fastapi.templates import Jinja2Templates  #UI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

#Initalize our fastapi app
app = FastAPI(title="Text Summarizeer App", description="Here you can summarize any long conversation or dialogue",version="1.0")

#model and tokenizer import 
model = T5ForConditionalGeneration.from_pretrained("./saved_summary_model")
tokenizer = T5Tokenizer.from_pretrained("./saved_summary_model")

#device 

if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else: 
    device = torch.device("cpu")
model.to(device)


#templating
templates = Jinja2Templates(directory=".")

#Input schema for dialogue ==> string
class DialogueInput(BaseModel):
    dialogue: str

def clean_data(text):
    text = re.sub(r"\r\n"," ",text) #lines
    text = re.sub(r"\s+"," ",text) #spaces
    text = re.sub(r"<.*?>"," ",text) #tags
    text = text.strip().lower()
    return text



#summarize dialogue
def summarize_dialogue(dialogue : str):
    dialogue = clean_data(dialogue) #clean dialogue

    #tokenize
    inputs = tokenizer(
        dialogue,
        padding = "max_length",
        max_length = 512,
        truncation = True,
        return_tensors = "pt"
    )

    #generate summary ( token ids)
    model.to(device)
    targets = model.generate(
        input_ids = inputs["input_ids"],
        attention_mask = inputs["attention_mask"],
        max_length = 150,
        num_beams=4 ,# transformer compare 4 output to give best summary
        early_stopping = True

    )

    #token ids to summary ==> decoding
    summary = tokenizer.decode(targets[0],skip_special_tokens=True) #EOS, SEP
    return summary
