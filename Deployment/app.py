from fastapi import FastAPI, Requests
from pydantic import BaseModel
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import re
from fastapi.templates import Jinja2Templates  #UI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles