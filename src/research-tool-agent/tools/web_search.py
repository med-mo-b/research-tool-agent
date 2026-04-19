from ddgs import DDGS
from langchain_core.tools import tool

@tool
def web_search_ddg(query: str, max_results: int = 3) -> str:
    """
    Useful for searching the web for current information, news, or facts using DuckDuckGo.
    The input should be a search query string.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            
            if not results:
                return "No results found."
            
            formatted_results = []
            for r in results:
                formatted_results.append(
                    f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}"
                )
            
            return "\n\n---\n\n".join(formatted_results)
            
    except Exception as e:
        return f"Error during web search: {str(e)}"