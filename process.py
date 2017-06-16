#!/usr/bin/env python

# ~/vcs/OEB-USFM-Tools $ python transform.py --target=csv --name=ulb --usfmDir=../tw_consistency/ --builtDir=../tw_consistency/


import os
import sys
import csv
import shutil
import urllib2


ULB_source_pattern = 'https://git.door43.org/Door43-Catalog/en_ulb/raw/master/{0}-{1}.usfm'
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
  #getCSVs()
  compare('test-tW-MAT.csv', 'test-41-MAT.usfm')

def compare(res1, res2):
  ulb_book = open(res2, 'r').readlines()
  diff_file = '{0}.diffs'.format(res2)
  diff = csv.writer(open(diff_file, 'w'))
  with open(res1, 'rb') as twcsv:
    for row in csv.reader(twcsv):
      bk, chp, vs = row[1:4]
      if bk == 'Book': continue
      tw_ulb_text = row[7].strip()
      ulb_text = getULBText(ulb_book, chp, vs)
      if tw_ulb_text != ulb_text:
        diff.writerow(row)

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
  print "Getting source USFM files..."
  for entry in books.iterkeys():
    source_url = ULB_source_pattern.format(books[entry][1], entry)
    output_path = os.path.join(os.getcwd(), source_url.rsplit('/', 1)[1])
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
