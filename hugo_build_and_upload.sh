#!/bin/sh
#
# Build a hugo site and upload to my website

hugo  -s site/covid

# uses ssh keys
scp -P 7822 -r site/covid/public/* wastedye@wastedyears.rocks:jason.wastedyears.rocks/obroin.net/
