from langchain_community.document_loaders import WebBaseLoader
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent, Tool
from langchain import hub
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.output_parsers.rail_parser import GuardrailsOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents.agent import BaseMultiActionAgent
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.callbacks.streaming_aiter_final_only import AsyncFinalIteratorCallbackHandler

import os
import requests
import json
import time
from typing import Annotated
from issues_tool import *
from meeting_tool import *
from pulls_tool import *
from common_tool import *
from repo_tool import get_repos_info
from email_tool import reminder_reveiw_code
from datastat_tool import *
from datetime import datetime
import config_util


# TavilySearchResults(max_results=1), 
inner_tools = [web_loader, get_meetinfo_by_group, search_tool, python_repl, math_tool, now_time_tool,
        get_all_meeting_group, create_a_meeting, get_issues_labels, get_issues_detail_info,
        reminder_reveiw_code, get_pulls_labels, get_pulls_detail_info, get_pulls_repos, get_pulls_assignees,
        get_pulls_authors, get_pulls_refs, get_pulls_sigs, get_repos_info, query_community_detail_info,
        query_community_all_sigs, query_community_usercontribute
        ]

llm_callback = AsyncFinalIteratorCallbackHandler()

def init_tool_agent(model_name, is_async) -> BaseMultiActionAgent:
    llm = None
    if is_async:
        # global llm_callback
        # llm_callback = AsyncIteratorCallbackHandler()
        llm = ChatOpenAI(model=model_name, max_tokens=4096, streaming=True,
                         verbose=True, callbacks=[llm_callback])
    else:
        llm = ChatOpenAI(model=model_name, max_tokens=4096)

    llm_with_tools = llm.bind_tools(inner_tools)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                - Role: 开源社区专家
                - Background: 用户需要一个智能助手来帮助解答有关openEuler和openGauss社区的领域问题，如PR（Pull Request）、issue、会议和开源流程等。
                - Profile: 你是一个专注于开源社区管理的专家，拥有丰富的知识储备和经验，能够准确回答社区成员的问题。
                - Skills: 熟悉openEuler和openGauss社区的运作方式、开源流程、项目管理工具和社区文化。
                - Goals: 提供准确、专业且及时的领域内问题解答，帮助社区成员更好地参与和贡献。
                - Constrains: 回答内容必须限定在openEuler和openGauss社区的领域问题，避免涉及不相关的娱乐、政治或文化内容。
                - OutputFormat: 清晰、简洁的文本回答，必要时提供链接或进一步的资源推荐。
                - Workflow:
                1. 确认用户的问题属于openEuler或openGauss社区的领域问题。
                2. 提供准确且专业的解答，包括相关的开源流程、工具使用和最佳实践。
                3. 如果需要，提供进一步的资源链接或推荐。
                - Examples:
                问题：如何在openEuler社区提交一个PR？
                回答：要提交一个Pull Request（PR）到openEuler社区，首先需要在社区的代码仓库中找到你想要贡献的项目，然后按照以下步骤操作：
                - Fork项目到你的个人账户。
                - Clone你的Fork到本地。
                - 创建一个新的分支并进行你的更改。
                - 提交更改并推送到你的Fork。
                - 通过你的Fork向原仓库提交PR。

                - Initialization: 欢迎使用社区智能助手，我是你的开源社区专家。如果你有任何关于openEuler或openGauss社区的问题，请随时提问，我会尽力为你提供帮助。
                """,
            ),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_tool_calling_agent(llm_with_tools, inner_tools, prompt)
    return agent

def create_agent_executor(is_async: bool = False):
    tool_agent = init_tool_agent("gpt-4o", is_async)
    agent_executor = AgentExecutor(agent=tool_agent, tools=inner_tools, verbose=True, Callbacks=[llm_callback])
    return agent_executor
