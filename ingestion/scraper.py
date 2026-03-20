from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from llm.llm import extract_car_markdown
from storage.markdown import save_markdown


"""
ONLY FOR EXTRACTING WEBPAGES AND CREATING MARKDOWN FILES. NOT FOR PROD
"""

def get_page_content(url:str) -> str:
    """
        Fetches the content of a given HTTPS URL and returns cleaned plain text.

        The function removes all HTML tags as well as script and style elements,
        returning only the visible text content of the page.

        Args:
            url (str): The HTTPS URL to retrieve content from.

        Returns:
            str | None: The cleaned plain text if the request is successful (status code 200),
            otherwise None.

        Raises:
            requests.RequestException: If the HTTP request fails.
    """
    
    if not url.startswith("https://"):
        raise ValueError("Link is not valid.")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled"
        ]
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 768},
            locale="de-DE"
        )
        page = context.new_page()

        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        content = page.content()
        browser.close()


    if len(content) > 0:
        # Remove tags
        soup = BeautifulSoup(content, "html.parser")

        for tag in soup(["script", "style"]):
             tag.decompose()

        return soup.get_text() + f"\n\n\n URL={url}"
    else:
        raise Exception("Scraped Content is empty")
        
    


    
def extract_information_from_page(url:str):
    """ Extract information from the given url and save it as a Markdown file

    Args:
        url (str): URL link to the Page
    """
    content = get_page_content(url)
    markdown_content, title = extract_car_markdown(content)
    save_markdown(markdown_content, title)

