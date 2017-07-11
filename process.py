#!/usr/bin/env python2
# ~/vcs/OEB-USFM-Tools $ python transform.py --target=csv --name=ulb --usfmDir=../tw_consistency/ --builtDir=../tw_consistency/


import os
import sys
import csv
import shutil
import urllib2
import argparse
from glob import glob
from ruamel import yaml


usfm_dir = 'sources/usfm'
usfm_dir_manifest = os.path.join(usfm_dir, 'manifest.yaml')
tw_dir = 'sources/tw'
tw_bible_dir = os.path.join(tw_dir, 'bible')
tw_config = os.path.join(tw_bible_dir, 'config.yaml')
tw_review = 'tw_review.csv'
books = {
          #u'GEN': [ u'Genesis', '01' ],
          #u'EXO': [ u'Exodus', '02' ],
          #u'LEV': [ u'Leviticus', '03' ],
          #u'NUM': [ u'Numbers', '04' ],
          #u'DEU': [ u'Deuteronomy', '05' ],
          #u'JOS': [ u'Joshua', '06' ],
          #u'JDG': [ u'Judges', '07' ],
          #u'RUT': [ u'Ruth', '08' ],
          #u'1SA': [ u'1 Samuel', '09' ],
          #u'2SA': [ u'2 Samuel', '10' ],
          #u'1KI': [ u'1 Kings', '11' ],
          #u'2KI': [ u'2 Kings', '12' ],
          #u'1CH': [ u'1 Chronicles', '13' ],
          #u'2CH': [ u'2 Chronicles', '14' ],
          #u'EZR': [ u'Ezra', '15' ],
          #u'NEH': [ u'Nehemiah', '16' ],
          #u'EST': [ u'Esther', '17' ],
          #u'JOB': [ u'Job', '18' ],
          #u'PSA': [ u'Psalms', '19' ],
          #u'PRO': [ u'Proverbs', '20' ],
          #u'ECC': [ u'Ecclesiastes', '21' ],
          #u'SNG': [ u'Song of Solomon', '22' ],
          #u'ISA': [ u'Isaiah', '23' ],
          #u'JER': [ u'Jeremiah', '24' ],
          #u'LAM': [ u'Lamentations', '25' ],
          #u'EZK': [ u'Ezekiel', '26' ],
          #u'DAN': [ u'Daniel', '27' ],
          #u'HOS': [ u'Hosea', '28' ],
          #u'JOL': [ u'Joel', '29' ],
          #u'AMO': [ u'Amos', '30' ],
          #u'OBA': [ u'Obadiah', '31' ],
          #u'JON': [ u'Jonah', '32' ],
          #u'MIC': [ u'Micah', '33' ],
          #u'NAM': [ u'Nahum', '34' ],
          #u'HAB': [ u'Habakkuk', '35' ],
          #u'ZEP': [ u'Zephaniah', '36' ],
          #u'HAG': [ u'Haggai', '37' ],
          #u'ZEC': [ u'Zechariah', '38' ],
          #u'MAL': [ u'Malachi', '39' ],
          u'MAT': [ u'Matthew', '41' ],
          u'MRK': [ u'Mark', '42' ],
          u'LUK': [ u'Luke', '43' ],
          u'JHN': [ u'John', '44' ],
          u'ACT': [ u'Acts', '45' ],
          u'ROM': [ u'Romans', '46' ],
          u'1CO': [ u'1 Corinthians', '47' ],
          u'2CO': [ u'2 Corinthians', '48' ],
          u'GAL': [ u'Galatians', '49' ],
          u'EPH': [ u'Ephesians', '50' ],
          u'PHP': [ u'Philippians', '51' ],
          u'COL': [ u'Colossians', '52' ],
          u'1TH': [ u'1 Thessalonians', '53' ],
          u'2TH': [ u'2 Thessalonians', '54' ],
          u'1TI': [ u'1 Timothy', '55' ],
          u'2TI': [ u'2 Timothy', '56' ],
          u'TIT': [ u'Titus', '57' ],
          u'PHM': [ u'Philemon', '58' ],
          u'HEB': [ u'Hebrews', '59' ],
          u'JAS': [ u'James', '60' ],
          u'1PE': [ u'1 Peter', '61' ],
          u'2PE': [ u'2 Peter', '62' ],
          u'1JN': [ u'1 John', '63' ],
          u'2JN': [ u'2 John', '64' ],
          u'3JN': [ u'3 John', '65' ],
          u'JUD': [ u'Jude', '66' ],
          u'REV': [ u'Revelation', '67' ],
}



def findNew(tw_dict, usfm_file, config, tw_review):
  book = ''
  chp = '0'
  vs = '0'
  new_rows = {}
  changed_rows = []
  ulb_book = open(usfm_file, 'r').readlines()
  for tw in tw_dict.iterkeys():
    all_hits = []
    for word in tw_dict[tw]:
      for line in ulb_book:
        if line.startswith('\\toc1 '):
          continue
        # Make sure we know what book this is
        if line.startswith('\\id '):
          book = line.split()[1].strip().lower()
          if book.upper() not in books:
            print 'Could not find {0} from USFM in the books dictionary'.format(book)
            sys.exit(1)
        # Grab the chapter number as we iterate
        if line.startswith('\\c '):
          chp = line.split()[1].strip()
        # Grab the verse number as we iterate
        if line.startswith('\\v '):
          vs = line.split()[1].strip()
        # Search for the tW on this line, no word form magic, just punctuation
        if ( ' {0} '.format(word) in line or
             ' {0}.'.format(word) in line or
             ' {0},'.format(word) in line or
             ' {0}\'s'.format(word) in line or
             ' {0}\''.format(word) in line or
             '\'{0} '.format(word) in line or
             ' {0}"'.format(word) in line or
             '"{0} '.format(word) in line or
             ' {0}!'.format(word) in line or
             ' {0})'.format(word) in line or
             '({0}'.format(word) in line or
             '-{0}'.format(word) in line or
             ' {0}-'.format(word) in line or
             ' {0}?'.format(word) in line or
             line.endswith(' {0}'.format(word)) ):
          all_hits.append('rc://en/ulb/book/{0}/{1}/{2}'.format(book,
                                                   chp.zfill(2), vs.zfill(2)))
          if not configCheck(tw, book, chp, vs, config):
            if not configCheck(tw, book, chp, vs, config, 'false_positives'):
              key = [book, chp, vs, '{0}.md'.format(tw)]
              new_rows[str(key)] = ['TRUE', book, chp, vs, '{0}.md'.format(tw),
                                                                    word, line]

    # Now check to see if any occurrences have been removed from ULB
    if tw not in config: continue
    for entry in config[tw]['occurrences']:
      b, c, v = entry.rsplit('/', 3)[1:]
      if b != book: continue
      if entry not in all_hits:
        changed_rows.append(['FALSE', b, c, v, '{0}.md'.format(tw), '', ''])
  new = csv.writer(open(tw_review, 'a'))
  for k in new_rows.iterkeys():
    new.writerow(new_rows[k])
  for x in changed_rows:
    new.writerow(x)

def configCheck(tw, bk, chp, vs, config, section='occurrences'):
  '''
  Returns True if tW is found in `occurrences` list in config.yaml.
  '''
  if tw in config:
    if 'rc://en/ulb/book/{0}/{1}/{2}'.format(bk.lower(), chp.zfill(2),
                                          vs.zfill(2)) in config[tw][section]:
      return True
  return False

def export(f, config, tw_list):
  with open(f, 'rb') as fcsv:
    for row in csv.reader(fcsv):
      book, chp, vs = row[1:4]
      if ( book == 'Book' or book == '' ): continue
      bk = getBook(book)
      tw = row[4].rsplit('.md', 1)[0].lower()
      if tw == '': continue
      if tw not in tw_list:
        print row
        continue
      if tw not in config:
        config[tw] = {'false_positives': [], 'occurrences': []}
      entry = 'rc://en/ulb/book/{0}/{1}/{2}'.format(bk, chp.zfill(2), vs.zfill(2))
      if row[0] == 'FALSE':
        if entry not in config[tw]['false_positives']:
          config[tw]['false_positives'].append(entry)
        if entry in config[tw]['occurrences']:
          config[tw]['occurrences'].remove(entry)
      else:
        if entry not in config[tw]['occurrences']:
          config[tw]['occurrences'].append(entry)
        if entry in config[tw]['false_positives']:
          config[tw]['false_positives'].remove(entry)
  return config

def getBook(book):
  if book.upper() in books:
    return book.lower()
  bk = [x for x in books.iterkeys() if books[x][0] == book.strip()]
  return bk[0].lower()

def loadtWs(path):
  tw_list = []
  tw_dict = {}
  for x in glob('{0}/*/*.md'.format(path)):
    tw_slug = x.rsplit('/', 1)[1].rsplit('.', 1)[0]
    tw_list.append(tw_slug)
    tw_dict[tw_slug] = []
    tw_text = open(x, 'r').readline()
    for word in tw_text.split(','):
      tw_dict[tw_slug].append(word.strip().strip('# '))
  return tw_list, tw_dict

def saveConfig(config_path, config):
  for x in config.iterkeys():
    config[x]['false_positives'].sort()
    config[x]['occurrences'].sort()
  config_f = open(config_path, 'w')
  yaml.safe_dump(config, config_f, default_flow_style=False, explicit_start=True)

def loadConfig(config_path):
  config = {}
  if os.path.exists(config_path):
    config_f = open(config_path, 'r').read()
    config = yaml.safe_load(config_f)
  return config

def getULBText(ulb_book, chp, vs):
  inchp = False
  clean_line = False
  for line in ulb_book:
    if inchp:
      if clean_line:
        if ( line.startswith('\\v ') or line.startswith('\\s') or
             line.startswith('\n') or line.startswith('\\m') ):
          return clean_line.strip()
        clean_line += ' '
        clean_line += line.lstrip('\\q12p'.format(vs)).strip()
        continue
      if '\\v {0}'.format(vs) in line:
        clean_line = line.lstrip('\\v {0}'.format(vs)).strip()
        continue
    if '\\c {0}'.format(chp) in line:
      inchp = True
  return clean_line


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-e', '--export', dest="tw_export", default=False,
      action='store_true', help='Export {0} to be reviewed.'.format(tw_review))
  parser.add_argument('-i', '--import', dest="tw_import", default=False,
      action='store_true', help='Import reviewed file, {0}.'.format(tw_review))

  # Parse args, exit if neither -e or -i was provided
  if len(sys.argv[1:]) < 1:
    parser.print_help()
    sys.exit(1)
  args = parser.parse_args(sys.argv[1:])

  # Ensure tW is cloned locally
  if not os.path.exists(tw_config):
    print 'Could not find {0}, make sure to clone tW into {1}'.format(
                                                            tw_config, tw_dir)
    sys.exit(1)

  # Ensure USFM is cloned locally
  if not os.path.exists(usfm_dir_manifest):
    print 'Could not find {0}, make sure to clone USFM into {1}'.format(
                                                  usfm_dir_manifest, usfm_dir)
    sys.exit(1)

  # Load tW config and tW terms
  config = loadConfig(tw_config)
  tw_list, tw_dict = loadtWs(os.path.join(tw_dir, 'bible'))

  # For exporting, run the comparison and output tw_review file
  if args.tw_export:
    if os.path.exists(tw_review):
      os.remove(tw_review)
    for usfm_file in glob('{0}/[0-6]*.usfm'.format(usfm_dir)):
      # Only process the books enabled in the books dictionary
      if not usfm_file.rstrip('.usfm').split('-')[1] in books: continue
      findNew(tw_dict, usfm_file, config, tw_review)
    print 'Please review {0}.'.format(tw_review)
    sys.exit(0)

  # For importing, verify file exists then run the update of config.yaml
  if args.tw_import:
    if not os.path.exists(tw_review):
      print 'Could not find {0} in current directory'.format(tw_review)
      sys.exit(1)
    config = export(tw_review, config, tw_list)
    saveConfig(tw_config, config)
    sys.exit(0)

