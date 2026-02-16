from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_jobs():
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for job in soup.find_all("div", class_="card-content"):
        title = job.find("h2", class_="title").text.strip()
        company = job.find("h3", class_="company").text.strip()
        location = job.find("p", class_="location").text.strip()

        if "engineer" in title.lower() or "developer" in title.lower():
            link = job.find("a")["href"]

            jobs.append({
                "company": company,
                "title": title,
                "location": location,
                "link": link
            })

    return jobs


@app.route("/")
def home():
    search_query = request.args.get("search", "").lower()
    jobs = scrape_jobs()

    if search_query:
        jobs = [
            job for job in jobs
            if search_query in job["title"].lower()
            or search_query in job["company"].lower()
        ]

    return render_template("index.html", jobs=jobs)


if __name__ == "__main__":
    app.run(debug=True)
