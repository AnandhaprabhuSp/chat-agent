# AIAgent

A small LangChain research agent that runs a **local Ollama model**, looks up a topic, and can save the result to a text file.

Ask a question at the prompt. The agent may search the web, query Wikipedia, then write a structured summary (topic, summary, sources, tools used).

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) installed and running
- The local model used in `main.py` (default: `qwen3.5:9b`)

```bash
ollama pull qwen3.5:9b
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On macOS/Linux run `python3 main.py` (not `python3 \main.py` or `python3 .\main.py`).

## Usage

```bash
python3 main.py
```

Example:

```text
Enter your query: research about Kangeyam bulls and save to file
```

The agent prints a structured response when it can parse one. If you asked it to save, it writes a file such as `output.txt` (or a name it chooses, like `kangeyam_bulls.txt`).

## Project layout

| File | Role |
|------|------|
| `main.py` | Agent loop, prompt, and Pydantic output parsing |
| `tools.py` | Search, Wikipedia, and save-to-file tools |
| `requirements.txt` | Python dependencies |

## Tools

- **Search_Web** — web search (Bing/Brave/Yahoo/Wikipedia backends)
- **wikipedia** — Wikipedia lookup
- **Save_to_File** — writes topic, summary, sources, and tools used to a text file

The model is `ChatOllama` in `main.py`. Change `model="qwen3.5:9b"` there to use a different local model.

## Notes

- No OpenAI key is required for the default local setup. `.env` is optional.
- Python 3.9 on macOS with LibreSSL can fail DuckDuckGo’s TLS 1.3 client. Search already avoids that engine and falls back to Wikipedia if needed. Python 3.11+ with OpenSSL is more reliable for web search.
