from langchain.document_loaders import WikipediaLoader
 
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts.chat import (
                                PromptTemplate,
                                ChatPromptTemplate, 
                                SystemMessagePromptTemplate, 
                                HumanMessagePromptTemplate, 
                                AIMessagePromptTemplate )
import os
os.environ["OPENAI_API_KEY"] = "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"

# The number of max documents
n = 2
 
# The loader
loader = WikipediaLoader(query='Juancho Hernangomez', load_max_docs=n)
 
# Concatenate the text to variable called context_text
context_text = ''
for d in range(len(loader.load())):
    context_text = context_text + ' ' + loader.load()[d].page_content

model = ChatOpenAI()
 
template = "Answer this question:\n{question}\n Here is some extra context: \n{document}"
human_prompt = HumanMessagePromptTemplate.from_template(template)
 
chat_prompt = ChatPromptTemplate.from_messages([human_prompt])
 
question = 'Which is the current team of Juancho Hernangomez'
 
document = context_text
 
result = model(chat_prompt.format_prompt(question=question, document=context_text).to_messages())
 
result.content





# import openai 
# import os
# import requests
# import wikipediaapi
# import wikipedia
# import urllib
# import bs4 as bs
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from langchain.agents import AgentType,initialize_agent,load_tools

# os.environ["OPENAI_API_KEY"] = "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"

# llm = OpenAI(temperature=.7)
# tools = load_tools(["wikipedia", "llm-math"], llm=llm)
# agent = initialize_agent(tools, llm, agent= AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
# output = agent.run("How old is Ms Dhoni in 2029?")
# print(output)