from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from direct_chat import direct_send_message
from init_tool_agent import create_agent_executor, llm_callback
from typing import Optional, AsyncGenerator
from sse_starlette import EventSourceResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.pydantic_v1 import BaseModel, Field
from langserve import add_routes
import asyncio
import logging
import os
import time

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# agent_executor = create_agent_executor(False)
agent_executor = create_agent_executor(True)

@app.on_event("startup")
async def startup_event():
    print('on start up ....')
    # agent_executor = create_agent_executor(True)
    print(f'init agent success')

class Message(BaseModel):
    content: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/stream_chat/")
async def stream_chat(message: Message):
    generator = direct_send_message(message.content)
    return StreamingResponse(generator, media_type="text/event-stream")

class AgentRequest(BaseModel):
    content: str
    role: Optional[str] = "user"
    model: Optional[str] = "gpt-4o"

chat_history = []

async def sync_agent_call(params: AgentRequest):
    global agent_executor
    start_time = time.perf_counter()
    response = agent_executor.invoke({
        'input': params.content,
        'chat_history': chat_history,
    })

    end_time = time.perf_counter()

    execution_time = end_time - start_time
    print(f"response execution time: {execution_time:.6f} seconds")
    chat_history.extend([
        HumanMessage(content=params.content),
        AIMessage(content=response["output"]),
    ])
    if len(chat_history) > 3:
        chat_history.pop(0)
    return response['output']

async def agent_response(params: AgentRequest) -> AsyncGenerator[str, None]:
    global agent_executor
    global llm_callback
    if params.content:
        # if llm_callback:
            run = asyncio.create_task(agent_executor.ainvoke(
            {"input": params.content, "chat_history": chat_history}))
            try:
                async for token in llm_callback.aiter():
                    yield token
            except Exception as e:
                print(f"Caught exception: {e}")
            finally:
                llm_callback.done.set()
            await run
        # else:
        #     run = asyncio.create_task(sync_agent_call(params))
        #     await run

# @app.post("/api/chat/")
# async def sse_http(params: AgentRequest):
#     # return EventSourceResponse(agent_response(params))
#     return {"message": sync_agent_call(params)}

class ChatInputWithHistory(BaseModel):
    """Input for the chat endpoint."""
    input: str
    chat_history: list[HumanMessage | AIMessage | SystemMessage] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )

playground_compatible_agent_executor = (
    agent_executor | (lambda x: x["output"])
).with_types(input_type=ChatInputWithHistory, output_type=str)


add_routes(
        app,
        playground_compatible_agent_executor,
        path="/chat",
        playground_type="chat",
)
