# Author : ysh
# 2025/11/17 Mon 17:46:03
from core.general import *
from lib.general import *
import lib.init

import langchain as lc
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
template = ChatPromptTemplate([
    ('system', '{system}'),
    ('user', '{input}')
])
_general_model = ChatOllama(
    model = 'gemma3:12b',
    base_url = lib.init.url
)

def get_message(text: str, system: str):
    return ChatPromptTemplate([
            ('system', f'{system}'),
            ('user', f'{text}')
        ])

def get_model(model: str, url: str | None = lib.init.url):
    return ChatOllama(
        model = model,
        base_url = url
    )

def ask_llm(text: str, system: str | None = None) -> str:
    return (template | _general_model | parser).invoke({
        'input': text,
        'system': system
    })