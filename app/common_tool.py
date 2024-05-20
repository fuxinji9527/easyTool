import os
import requests
import json
from typing import Annotated
from langchain_core.tools import tool
from langchain_openai import OpenAI
from langchain.chains import LLMMathChain
from langchain_experimental.utilities import PythonREPL
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import Tool
from datetime import datetime
import config_util

@tool
def web_loader(url: str) -> str:
    """抓取url对应网页的内容"""
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs[0].page_content

# Warning: This executes code locally, which can be unsafe when not sandboxed
repl = PythonREPL()
@tool
def python_repl(
    code: Annotated[str, "The python code to execute to generate your chart."]
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    return f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"

search = SerpAPIWrapper()
@tool
def search_tool(
    input: Annotated[str, "The question need to search in the web."]
):
    """当您需要网上搜索并回答当前事件的问题时很有用
    """
    try:
        result = search.run(input)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    return f"Successfully executed, out: {result}"

@tool
def now_time_tool(
    input: Annotated[str, "可以不用参数"] = ''
):
    """当您需要获取当前时间非常有效
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

llmtool = OpenAI(temperature=0)
llm_math_chain = LLMMathChain(llm=llmtool, verbose=True)
math_tool = Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="当你需要回答数学问题时很有用"
    )
