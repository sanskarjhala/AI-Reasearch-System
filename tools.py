from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """
        Search web for recent and reliable information on a topic
    Args:
        query (str): The search query string provided by the user

    Returns:
        A list of titles, URLs, and snippets from search results.
    """
    results = tavily.search(
        query=query, max_results=5, include_raw_content=False, search_depth="advanced"
    )
    output = []
    for r in results["results"]:
        output.append(
            f"Title : {r['title']}\nURL:{r['url']}\nSnippet: {r['content'][:300]}\nScore: {r['score']:.2f}\n"
        )

    return "\n-----\n".join(output)


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from the given URL for depper reading

    Args:
        url (str): URL of the website

    Returns:
        String which containe clean text content
    """

    try:
        response = requests.get(url, timeout=10, headers={"User-agent": "Mozilla/5.0"})
        # print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup)
        for tag in soup(["script", "style", "nav", "footer" ,"img"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)[:3500]

    except Exception as e:
        return f"Error while scarping the data {str(e)}"
