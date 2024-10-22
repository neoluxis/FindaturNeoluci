from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 抓取 DuckDuckGo 搜索结果
def duckduckgo_search(query):
    search_url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for result in soup.find_all("a", class_="result__a", href=True):
        title = result.get_text()
        link = result["href"]
        results.append({"title": title, "link": link})
    
    return results

# 首页路由，显示搜索页面
@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            results = duckduckgo_search(query)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

