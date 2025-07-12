# 1. reports_agent.py

from typing import Literal, List, Any
from langchain_core.tools import tool
from langgraph.types import Command
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from langchain_core.prompts.chat import ChatPromptTemplate
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from utils.llms import LLMModel
from langchain_community.tools.tavily_search import TavilySearchResults
from prompt_library.prompt import personal_assistant_prompt
from langgraph.checkpoint.redis import RedisSaver


class ReportAgentState(TypedDict):
    messages: Annotated[list[Any], add_messages]
    id_number: int
    name: str
    next: str

class PersonalReportAgent:
    def __init__(self):
        llm_model = LLMModel()
        self.llm_model = llm_model.get_model()
        self.search_tool = TavilySearchResults()  # ✅ Init search tool


    def tracker_node(self, state: ReportAgentState) -> Command[Literal['__end__']]:
        """
        Node that responds to the user with report-based or external help using Tavily if needed.
        """
        system_prompt = ChatPromptTemplate.from_messages([
            ("system", personal_assistant_prompt),
            ("placeholder", "{messages}"),
        ])

        agent = create_react_agent(
            model=self.llm_model,
            tools=[self.search_tool],
            prompt=system_prompt,
        )

        result = agent.invoke(state)

        return Command(
            update={
                "messages": state["messages"] + [
                    AIMessage(content=result["messages"][-1].content, name="report_tracker")
                ]
            },
            goto="__end__",
        )


    def workflow(self):
        self.graph = StateGraph(ReportAgentState)
        self.graph.add_node("tracker", self.tracker_node)
        self.graph.set_entry_point("tracker")

       
        REDIS_URI = "redis://localhost:6379"
        with RedisSaver.from_conn_string(REDIS_URI) as checkpointer:
              checkpointer.setup()
    
              with RedisStore.from_conn_string(REDIS_URI) as store:
                store.setup()

        self.app = self.graph.compile(checkpointer=checkpointer,store=store)
        return self.app
