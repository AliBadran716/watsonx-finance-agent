from typing import Any
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
import yfinance as yf
from langchain_core.tools import Tool
from langchain.tools import tool

@tool
def ddg_search(query: str, max_results: int = 3) -> str:
    """
    Perform a DuckDuckGo web search and return formatted top search results.

    Args:
        query (str): The search query string.
        max_results (int): Maximum number of search results to return (default 3).

    Returns:
        str: Formatted string containing titles, snippets, and links of top search results,
             or an explanatory message if no query or results are found.
    """
    if not query:
        return "No query provided."
    
    search = DuckDuckGoSearchAPIWrapper()
    results = search.results(query, max_results=max_results) or []
    
    out = []
    for i, r in enumerate(results[:max_results]):
        # Extract title, snippet, and link from result dict, with fallbacks
        title = r.get("title", "No title")
        snippet = r.get("snippet", "No snippet")
        link = r.get("link", "No link")
        out.append(f"{i+1}. {title}\n{snippet}\n{link}")
    
    # Join all results into a single string separated by blank lines
    return "\n\n".join(out) if out else "No results."


@tool
def get_stock_info(ticker: str, period: str = "5d") -> str:
    """
    Retrieve recent stock price and basic company information for a given ticker symbol.

    Args:
        ticker (str): Stock ticker symbol, e.g. "AAPL".
        period (str): Historical data period to fetch (default is last 5 days).

    Returns:
        str: Formatted string including ticker, company name, sector, 
             last closing price, and a preview of recent analyst recommendations,
             or an error message if data retrieval fails.
    """
    if not ticker:
        return "No ticker provided."
    try:
        t = yf.Ticker(ticker)

        # Fetch historical price data for given period
        hist = t.history(period=period)
        last_close = float(hist['Close'].iloc[-1]) if not hist.empty else None

        # Safely extract company info dictionary from yfinance object
        info = {}
        try:
            if hasattr(t, "info"):
                info = t.info or {}
            elif hasattr(t, "get_info"):
                info = t.get_info() or {}
        except Exception:
            info = {}

        # Extract name and sector with fallbacks
        name = info.get("shortName") or info.get("longName") or ticker
        sector = info.get("sector") or info.get("industry") or "N/A"

        # Attempt to get the last 5 analyst recommendations string
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
        # Return error message if any exception occurs during data fetch
        return f"Error fetching ticker {ticker}: {e}"


# Create LangChain Tool wrappers for the defined functions for agent use
SEARCH_TOOL = Tool.from_function(
    ddg_search,
    name="duckduckgo_search",
    description="Search the web using DuckDuckGo"
)

STOCK_TOOL = Tool.from_function(
    get_stock_info,
    name="get_stock_info",
    description="Get stock price and short company info for a ticker symbol"
)

NEWS_TOOL = YahooFinanceNewsTool()  # Prebuilt tool for fetching finance news


def main():
    """
    simple test main function to demonstrate usage of the search, stock info, and news tools.
    """
    print("DuckDuckGo Search Tool:")
    print(ddg_search("what is the GDP of Egypt 2024"))  # Example web search query

    print("\nStock Info Tool:")
    print(get_stock_info("AAPL"))  # Example stock info for Apple

    print("\nFinance News Tool:")
    print(NEWS_TOOL.run("AAPL"))  # Example finance news for Apple ticker


if __name__ == "__main__":
    main()