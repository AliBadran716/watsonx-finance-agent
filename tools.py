from typing import Any
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
import yfinance as yf
from langchain_core.tools import Tool
from langchain.tools import tool

@tool
def ddg_search(query: str, max_results: int = 3) -> str:
    """Return top DuckDuckGo search snippets (title, snippet, link)."""
    if not query:
        return "No query provided."
    
    search = DuckDuckGoSearchAPIWrapper()
    results = search.results(query, max_results=max_results) or []
    
    out = []
    for i, r in enumerate(results[:max_results]):
        title = r.get("title", "No title")
        snippet = r.get("snippet", "No snippet")
        link = r.get("link", "No link")
        out.append(f"{i+1}. {title}\n{snippet}\n{link}")
    
    return "\n\n".join(out) if out else "No results."


@tool
def get_stock_info(ticker: str, period: str = "5d") -> str:
    """Return stock price and short company info for a ticker like AAPL."""
    if not ticker:
        return "No ticker provided."
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period)
        last_close = float(hist['Close'].iloc[-1]) if not hist.empty else None

        # safer info extraction
        info = {}
        try:
            if hasattr(t, "info"):
                info = t.info or {}
            elif hasattr(t, "get_info"):
                info = t.get_info() or {}
        except Exception:
            info = {}

        name = info.get("shortName") or info.get("longName") or ticker
        sector = info.get("sector") or info.get("industry") or "N/A"

        # recommendations preview
        try:
            recs = t.recommendations
            if recs is not None and not recs.empty:
                recs_preview = recs.tail(5).to_string()
            else:
                recs_preview = "No recommendations available."
        except Exception:
            recs_preview = "No recommendations available."

        return (
            f"Ticker: {ticker}\n"
            f"Name: {name}\n"
            f"Sector: {sector}\n"
            f"Last close: {last_close}\n"
            f"Recommendations (last 5):\n{recs_preview}"
        )
    except Exception as e:
        return f"Error fetching ticker {ticker}: {e}"


# Wrap as LangChain tools
SEARCH_TOOL = Tool.from_function(ddg_search, name="duckduckgo_search", description="Search the web using DuckDuckGo")
STOCK_TOOL = Tool.from_function(get_stock_info, name="get_stock_info", description="Get stock price and short company info for a ticker symbol")
NEWS_TOOL = YahooFinanceNewsTool()

def main():
    print("DuckDuckGo Search Tool:")
    print(ddg_search("what is the GDP of Egypt 2024"))
    print("\nStock Info Tool:")
    print(get_stock_info("AAPL"))
    print("\nFinance News Tool:")
    print(NEWS_TOOL.run("AAPL"))

if __name__ == "__main__":
    main()
