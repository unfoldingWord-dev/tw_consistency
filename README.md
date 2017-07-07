# tW Consistency

This repository contains code to aid the content team(s) in achieving consistency between the tW and the ULB text.


## Setup

The USFM and translationWords need to be downloaded into the sources directory.  Do the following to get setup:

    git clone https://github.com/unfoldingWord-dev/tw_consistency.git
    cd tw_consistency/sources
    git clone https://git.door43.org/Door43/en_tw.git tw
    git clone https://git.door43.org/Door43/en_ulb.git usfm

## Tests

You can run tests via `python tests.py`.

## Running

After that, you can run `python process.py` and this script will output CSV file into the `diffs/` directory that records everywhere that the ULB text has changed since the previous review.

In addition, the script will output a `config.yaml` file which is an exhaustive list of everywhere that the tW is listed in the ULB.  Currently this is only for the NT.


## Future

This is a short term solution that will aid consistency for the June/July 2017 release of our English source content.  Longer term this consistency feature will be based off Strongs numbers.
