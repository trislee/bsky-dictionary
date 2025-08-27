import time
import os

import requests

from atproto import Client
from atproto.exceptions import RequestException, ModelError


WORDLIST_URL = "https://raw.githubusercontent.com/words/an-array-of-english-words/refs/heads/master/index.json"
OUTPUT_FILE = "word_results.txt"


def get_word_list():
    r = requests.get(url = WORDLIST_URL)
    all_words = r.json()
    with open(OUTPUT_FILE, "r") as f:
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
            with open(OUTPUT_FILE, "a") as f:
                f.write(f"{word},{results}\n")
        except:
            print(f"Encountered error when searching {word}, sleeping for 60 seconds")
            return 60
        with open(OUTPUT_FILE, "a") as f:
            f.write(f"{word},{results}\n")

if __name__ == "__main__":

    client = Client()
    client.login(os.environ["BLUESKY_USERNAME"], os.environ["BLUESKY_PASSWORD"])

    if not os.path.isfile(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w") as f:
            f.write("")

    time_to_wait = 0
    while True:
        time.sleep(time_to_wait)
        time_to_wait = run_until_ratelimit(client = client)