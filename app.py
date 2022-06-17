from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import redis
from rq import Queue
import logging

app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)

# logs will be stored at logfile.log from debug level to critical level
logging.basicConfig(filename='logfile.log', level=logging.DEBUG)


def background_task(tickerInput):

    resp = requests.get(f"https://api.nasdaq.com/api/news/topic/articlebysymbol?q={tickerInput}|stocks&offset=0&limit=8&fallback=false", headers={
        "User-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'})

    if resp.status_code == 200:

        data = resp.json()

        articles = []

        for i in data['data']['rows']:
            articles.append(i['title'])

        r.sadd(tickerInput, *articles)

    else:
        app.logger.error("nasdaq server issue, api isnt giving any response")


@app.route("/fetchNews")
def add_task():
    if request.args.get("tickerInput"):
        job = q.enqueue(background_task, request.args.get("tickerInput"))
        q_len = len(q)
        return f"Task {job.id} added to queue at {job.enqueued_at}. {q_len} tasks in the queue"
    else:
        return "No value for tickerInput"


if __name__ == "__main__":
    app.run()
