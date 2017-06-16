#!/usr/bin/env python

# ~/vcs/OEB-USFM-Tools $ python transform.py --target=csv --name=ulb --usfmDir=../tw_consistency/ --builtDir=../tw_consistency/


import os
import sys
import csv
import shutil
import urllib2
from glob import glob
from ruamel import yaml


ULB_source_pattern = 'https://git.door43.org/Door43-Catalog/en_ulb/raw/master/{0}-{1}.usfm'
diff_file = 'diffs/differences.csv'
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


def main(args):
  getUSFM(False)
  # Get JAMES
  config = loadConfig('config.yaml')
  if os.path.exists(diff_file):
    os.remove(diff_file)
  tw_list = loadtWs('../en_tw/bible')
  for usfm_file in glob('sources/[0-6]*.usfm'):
    tw_file = usfm_file.replace('usfm', 'tw.csv')
    if not os.path.exists(tw_file): continue
    compare(tw_file, usfm_file, config)
    config = export(tw_file, config, tw_list)

    # After editors review the diffs, run this:
    #config = export(diff_file, config, tw_list)
  saveConfig('config.yaml', config)

def compare(res1, res2, config):
  ulb_book = open(res2, 'r').readlines()
  diff = csv.writer(open(diff_file, 'a'))
  with open(res1, 'rb') as twcsv:
    for row in csv.reader(twcsv):
      book, chp, vs = row[1:4]
      if book == 'Book':
        continue
      tw_ulb_text = row[7].strip()
      if tw_ulb_text == '': continue
      ulb_text = getULBText(ulb_book, chp, vs)
      if tw_ulb_text != ulb_text:
        tw = row[5].rsplit('.txt', 1)[0].lower()
        # Check to see if this combo is alread in config.yaml,
        # if it is, continue as no need to require a recheck
        if configCheck(tw, getBook(book), chp, vs, config):
          continue
        row[7] = ulb_text
        diff.writerow(row)

def configCheck(tw, bk, chp, vs, config):
  if tw in config:
    if 'rc://en/ulb/book/{0}/{1}/{2}'.format(bk, chp.zfill(2), vs.zfill(2)) in config[tw]['occurrences']:
      return True
  return False

def export(f, config, tw_list):
  with open(f, 'rb') as fcsv:
    for row in csv.reader(fcsv):
      book, chp, vs = row[1:4]
      if ( book == 'Book' or book == '' ): continue
      if row[0] == 'FALSE': continue
      bk = getBook(book)
      tw = row[5].rsplit('.txt', 1)[0].lower()
      if tw == '': continue
      if tw not in tw_list:
        #######print row
        continue
      if tw not in config:
        config[tw] = {'false_positives': [], 'occurrences': []}
      entry = 'rc://en/ulb/book/{0}/{1}/{2}'.format(bk, chp.zfill(2), vs.zfill(2))
      if entry not in config[tw]['occurrences']:
        config[tw]['occurrences'].append(entry)
  return config

def getBook(book):
  bk = [x for x in books.iterkeys() if books[x][0] == book.strip()]
  return bk[0].lower()

def loadtWs(path):
  tws = []
  for x in glob('{0}/*/*.md'.format(path)):
    tws.append(x.rsplit('/', 1)[1].rsplit('.', 1)[0])
  return tws

def saveConfig(config_path, config):
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
  

def getUSFM(update=True):
  for entry in books.iterkeys():
    source_url = ULB_source_pattern.format(books[entry][1], entry)
    output_path = os.path.join(os.getcwd(), 'sources', source_url.rsplit('/', 1)[1])
    if not update:
      if os.path.exists(output_path): continue
    getURL(source_url, output_path)

def getURL(url, outfile):
  try:
    request = urllib2.urlopen(url)
  except:
    print "  => ERROR retrieving %s\nCheck the URL" % url
    sys.exit(1)
  with open(outfile, 'wb') as fp:
    shutil.copyfileobj(request, fp)

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
