# Bluesky Dictionary

My somewhat janky attempt at a faster version of [The Bluesky Dictionary](https://www.avibagla.com/blueskydictionary/)

## How to use
1. run `python search_words.py`: this loops over all words in a word list and searches them on Bluesky
2. run `python get_ngrams.py`: this uses the ngrams.dev API to find the most commonly used words in the English language that haven't been used by Bluesky yet

## TODO
- Handling the ratelimit error response from atproto is sloppy, I just sleep for a minute when that happens and it seems to work
- using an actual database instead of 2 text files might be good
- the ngrams.dev API is great and free, but it has a fairly high frequency threshold, so uncommon words have a frequency of 0. Using the Google ngrams data (which can be [downloaded](https://stressosaurus.github.io/raw-data-google-ngram/)) would probably be more comprehensive