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

### Running a Comparison Export

If you want to check the current list of tWs against the current USFM, you can run:

    python process.py -e

This will generate a file named `tw_review.csv` in the current working directory.  By default, every entry is marked TRUE to make reviewing for false-positives easier.

### Importing a Reviewed File

After the `tw_review.csv` has been reviewed for correctness, you can import the resulting data into the `config.yaml` file by running:

    python process.py -i
    
## Future

This is a short term solution that will aid consistency for the June/July 2017 release of our English source content.  Longer term this consistency feature will be based off Strongs numbers.
