# tW Consistency

This repository contains code to aid the content team(s) in achieving consistency between the tW and the ULB text.


## Running

The CSV files need to be downloaded manually from Google Sheets and placed into the `sources/` directory.

After that, you can run `python process.py` and this script will output CSV file into the `diffs/` directory that records everywhere that the ULB text has changed since the previous review.

In addition, the script will output a `config.yaml` file which is an exhaustive list of everywhere that the tW is listed in the ULB.  Currently this is only for the NT.

## Tests

You can run tests via `python tests.py`.


## Future

This is a short term solution that will aid consistency for the June/July 2017 release of our English source content.  Longer term this consistency feature will be based off Strongs numbers.
