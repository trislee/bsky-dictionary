from itertools import batched

import requests
import pandas as pd


BASE_URL = "https://api.ngrams.dev"
CORPUS = "eng"
WORD_LIST = "word_results.txt"
FREQ_LIST = "word_freq.txt"


def process_batch_response(r):
    word_freqs = []
    for d in r.json()["results"]:
        word = d["query"]
        ngrams = d["ngrams"]
        if len(ngrams) == 0:
            word_freqs.append({"word": word, "freq": 0})
        else:
            word_freqs.append({"word": d["query"], "freq": d["ngrams"][0]["relTotalMatchCount"]})
    return word_freqs


if __name__ == "__main__":

    with open(WORD_LIST, "r") as f:
        data = list(filter(None, f.read().split("\n")))
    word_count = {line.split(",")[0] : int(line.split(",")[1]) for line in data}
    unused_words = [word for word, count in word_count.items() if count == 0]

    old_freqs = pd.read_csv("word_freq.txt", names = ["word", "freq"])
    already_done_words = set(old_freqs["word"])
    words_to_do = set(unused_words) - already_done_words

    print(f"Fetching ngrams for {len(words_to_do)} words, {len(already_done_words)} words already have ngrams")

    word_freq = []

    for batch in batched(words_to_do, n=100):
        payload = {
            "queries": list(batch),
            "flags": "cr"
        }
        r = requests.post(f"{BASE_URL}/{CORPUS}/batch", json = payload)
        word_freq.extend(process_batch_response(r))

    new_freqs = pd.DataFrame(word_freq)

    freqs = pd.concat([old_freqs, new_freqs]).reset_index(drop = True).sort_values("word")
    freqs.to_csv(FREQ_LIST, index = False, header = False)

    print("Unused words with highest frequency\n")
    print(freqs.sort_values("freq", ascending = False).iloc[:5].to_string(index = False))