import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

def scrape_quotes(page=1):
    """
    Scrapes quotes from quotes.toscrape.com for the given page number.
    Returns a list of dictionaries: [{text, author, tags:[]}, ...].
    """
    url = f"http://quotes.toscrape.com/page/{page}/"
    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')
    quote_divs = soup.find_all("div", class_="quote")

    results = []
    for div in quote_divs:
        text_el = div.find("span", class_="text")
        author_el = div.find("small", class_="author")
        tag_els = div.find_all("a", class_="tag")

        text = text_el.get_text(strip=True) if text_el else ""
        author = author_el.get_text(strip=True) if author_el else ""
        tags = [t.get_text(strip=True) for t in tag_els]

        results.append({
            "text": text,
            "author": author,
            "tags": tags
        })
    return results

@app.route("/scrape_quotes", methods=["POST"])
def scrape_quotes_endpoint():
    """
    Expects JSON input: { "page": <int> }
    Returns JSON array of quotes:
    [
      {
        "text": "...",
        "author": "...",
        "tags": ["tag1", "tag2"]
      },
      ...
    ]
    """
    data = request.get_json()
    page = data.get("page", 1)
    quotes = scrape_quotes(page=page)
    return jsonify(quotes)

if __name__ == "__main__":
    # Render provides the PORT environment variable. Default to 5000 locally if not set.
    port = int(os.environ.get("PORT", 5000))
    # Listen on 0.0.0.0 to be accessible externally.
    app.run(host="0.0.0.0", port=port, debug=False)
