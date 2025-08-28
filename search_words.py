import time
import os

import requests

from atproto import Client
from atproto.exceptions import RequestException, ModelError


WORDLIST_URL = "https://raw.githubusercontent.com/words/an-array-of-english-words/refs/heads/master/index.json"
WORD_LIST = "word_results_fresh.txt"
SLEEP_TIME_SECONDS = 60


def get_word_list():
    r = requests.get(url = WORDLIST_URL)
    all_words = r.json()
    with open(WORD_LIST, "r") as f:
        already_done_words = set(filter(None, [line.split(",")[0] for line in f.read().split("\n")]))
    words = [word for word in all_words if word not in already_done_words]
    print(f"{len(words)} words left to search out of {len(all_words)} total")
    return words

def run_until_ratelimit(client):
    words = get_word_list()
    for i, word in enumerate(words):
        print(f"{i} / {len(words)}", word)
        params = {"q": word, "limit": 5}
        try:
            response = client.app.bsky.feed.search_posts(params)
            results = len(response["posts"])
        except ModelError:
            results = 1
        except:
            print(f"Encountered error when searching '{word}', sleeping for 60 seconds")
            return SLEEP_TIME_SECONDS
        with open(WORD_LIST, "a") as f:
            f.write(f"{word},{results}\n")
    return 0

if __name__ == "__main__":

    client = Client()
    client.login(os.environ["BLUESKY_USERNAME"], os.environ["BLUESKY_PASSWORD"])

    if not os.path.isfile(WORD_LIST):
        with open(WORD_LIST, "w") as f:
            f.write("")

    while True:
        time_to_wait = run_until_ratelimit(client = client)
        if time_to_wait == 0:
            break
        time.sleep(time_to_wait)
