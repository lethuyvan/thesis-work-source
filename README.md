# Thesis Course Works

Source code and various data that I used during my Master Thesis work

Most of the programs are written in Python and I used a docker image to run my
program, this makes it more portable

## Docker image

You can build the image using Dockerfile from `docker_image` directory

## Tagger

The tagger program is `tagger.py` and use the Stanford core NLP package

This is run by docker image `konradstrack/corenlp`. You can run this in
a dedicated docker network, then run the `targger.py` script using another
container in the same network to connect to the `corenlp` server and send over
the requests

## LIWC results

Within the 2 datasets, I use LIWC as features for neural network.

There **should** be a `van_liwc_result.txt` file in `facebook/aggregated_result`
and another `van_liwc_result.txt` in `reddit/crawled_result`
