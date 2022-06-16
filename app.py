from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import redis
from rq import Queue

import time

app = Flask(__name__)
app.app_context().push()

r = redis.Redis()
q = Queue(connection=r)


def background_task(tickerInput):

    print("Task running")

    resp = requests.get('https://api.nasdaq.com/api/news/topic/articlebysymbol?q={tickerInput}|stocks&offset=0&limit=8&fallback=false', headers={
        "User-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'})
    data = resp.json()
    articles = []
    for i in data['data']['rows']:
        print(i['title'])
        articles.append(i['title'])

    print("Task complete")

    r.sadd(tickerInput, *articles)


@app.route("/fetchNews")
def add_task():

    if request.args.get("tickerInput"):

        job = q.enqueue(background_task, request.args.get("tickerInput"))
        print(type(job))
        return f"{job}"

    return "No value for tickerInput"


if __name__ == "__main__":
    app.run()
