from datetime import datetime
from typing import List, Optional

from langchain.tools import StructuredTool, Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from pydantic import BaseModel, Field


wikipedia = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=2000)
wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia)

# Python 3.9 + LibreSSL cannot use ddgs' DuckDuckGo engine (TLS 1.3).
# Skip that backend and fall back to Wikipedia if search still fails.
search_wrapper = DuckDuckGoSearchAPIWrapper(
    backend="bing,brave,yahoo,wikipedia",
    max_results=5,
)


def search_web(query: str) -> str:
    try:
        return search_wrapper.run(query)
    except ValueError as exc:
        if "Unsupported protocol version" not in str(exc):
            raise
        return wikipedia.run(query)


search_tool = Tool(
    name="Search_Web",
    description="Search the web for information",
    func=search_web,
)


class SaveToFileInput(BaseModel):
    topic: str = Field(description="Research topic")
    summary: str = Field(description="Research summary")
    sources: List[str] = Field(default_factory=list, description="Sources used")
    tools_used: List[str] = Field(default_factory=list, description="Tools used")
    filename: str = Field(default="output.txt", description="File to write")


def save_to_file(
    topic: str,
    summary: str,
    sources: Optional[List[str]] = None,
    tools_used: Optional[List[str]] = None,
    filename: str = "output.txt",
) -> str:
    sources = sources or []
    tools_used = tools_used or []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    formatted_text = (
        f"Research Results\n"
        f"Timestamp: {timestamp}\n"
        f"Topic: {topic}\n\n"
        f"{summary}\n\n"
        f"Sources: {', '.join(sources)}\n"
        f"Tools used: {', '.join(tools_used)}\n"
    )

    with open(filename, "w") as file:
        file.write(formatted_text)
    return f"Results saved to {filename}"


save_to_file_tool = StructuredTool.from_function(
    func=save_to_file,
    name="Save_to_File",
    description=(
        "Save research results to a file. "
        "Pass topic, summary, sources, and tools_used."
    ),
    args_schema=SaveToFileInput,
)
