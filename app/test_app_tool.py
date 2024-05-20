from langchain_community.document_loaders import WebBaseLoader
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent, Tool
from langchain import hub
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.output_parsers.rail_parser import GuardrailsOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults

import os
import requests
import json
import time
from typing import Annotated
from issues_tool import *
from meeting_tool import *
from pulls_tool import *
from common_tool import *
from init_tool_agent import create_agent_executor
from config_util import *

agent_executor = create_agent_executor()

chat_history = []

input_text = input('>>> ')
while input_text.lower() != 'bye':
    if input_text:
        start_time = time.perf_counter()
        try:
            response = agent_executor.invoke({
                'input': input_text,
                'chat_history': chat_history,
            })

            end_time = time.perf_counter()

            execution_time = end_time - start_time
            print(f"response execution time: {execution_time:.6f} seconds")

            chat_history.extend([
                HumanMessage(content=input_text),
                AIMessage(content=response["output"]),
            ])
            if len(chat_history) > 3:
                chat_history.pop(0)
            print(response['output'])
        except Exception as e:
            print(e)
    input_text = input('>>> ')
