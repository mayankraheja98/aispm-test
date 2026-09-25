"""LangChain ReAct agent for fashion recommendations."""
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

def search_catalogue(query: str) -> str:
    return f"Found products for: {query}"

def get_size_guide(brand: str) -> str:
    return f"Size guide for {brand}"

tools = [
    Tool(name="SearchCatalogue", func=search_catalogue,
         description="Search the fashion catalogue"),
    Tool(name="GetSizeGuide", func=get_size_guide,
         description="Get brand size guide"),
]

llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_react_agent(llm, tools, prompt=None)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    result = agent_executor.invoke({"input": "Find me a blue kurta in size M"})
    print(result)
