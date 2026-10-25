from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wikipedia_tool, save_to_file_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatOllama(model="qwen3.5:9b", temperature=0)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can answer questions and provide summaries of information. Wrap the output in this format and provide no other text: {format_instructions}"),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wikipedia_tool, save_to_file_tool]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_tool_error=True,
)
query = input("Enter your query: ")
raw_response = agent_executor.invoke({"input": query})
# print("raw_response:",raw_response)

try:
    structured_response = parser.parse(raw_response["output"])
    print("structured_response:",structured_response)
except Exception as e:
    print(f"Error parsing response: {e}")

# parsed_response = parser.parse(raw_response["output"])
# print(parsed_response)

