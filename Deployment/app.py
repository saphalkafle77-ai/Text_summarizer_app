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