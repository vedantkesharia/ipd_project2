import openai 
import os
import requests
import wikipediaapi
import wikipedia
import urllib
import bs4 as bs
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# page = wiki_wiki.page(page_title)



# if page.exists():
#     print("Title:", page.title)
#     print("Summary:", page.summary) 
# else:
#     print("Page does not exist.")


# llm = OpenAI(openai_api_key="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",temperature=0.3)

# prompt = PromptTemplate.from_template("Summarise the following {text}")

# chain = LLMChain(llm=llm,prompt=prompt)
# output = chain.run(text)