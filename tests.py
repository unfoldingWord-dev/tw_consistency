#!/usr/bin/env python

import unittest
from process import *

class TestBooks(unittest.TestCase):

  def testDictionary(self):
    self.assertEqual('Jude', books['JUD'][0])
    self.assertEqual(len(books), 27)

class TestgetURL(unittest.TestCase):

  def testDownload(self):
    getURL('https://git.door43.org/Door43-Catalog/en_ulb/raw/master/65-3JN.usfm', '/tmp/65-3JN.usfm')
    self.assertTrue(os.path.exists('/tmp/65-3JN.usfm'))
    os.remove('/tmp/65-3JN.usfm')

class TestgetUSFM(unittest.TestCase):

  def testUpdate(self):
    getUSFM()
    f = open('sources/57-TIT.usfm', 'r').read()
    names = ['Artemas', 'Tychicus', 'Zenas', 'Apollos', 'Paul']
    for x in names:
      self.assertTrue(x in f)

  def testNoUpdate(self):
    getUSFM(False)
    f = open('sources/57-TIT.usfm', 'r').read()
    names = ['Artemas', 'Tychicus', 'Zenas', 'Apollos', 'Paul']
    for x in names:
      self.assertTrue(x in f)

class TestCompare(unittest.TestCase):

  def testgetULBText(self):
    ulb_book = open('sources/test-41-MAT.usfm', 'r').readlines()
    self.assertEqual(getULBText(ulb_book, '1', '4'), 'Ram was the father of Amminadab, Amminadab the father of Nahshon, and Nahshon the father of Salmon.')
    self.assertEqual(getULBText(ulb_book, '13', '58'), 'And he did not do many miracles there because of their unbelief.')
    self.assertEqual(getULBText(ulb_book, '13', '35'), 'This was in order that what had been said through the prophet might come true, when he said, "I will open my mouth in parables. I will say things that were hidden from the foundation of the world."')
    self.assertEqual(getULBText(ulb_book, '1', '6'), 'Jesse was the father of David the king. David was the father of Solomon by the wife of Uriah.')
    self.assertEqual(getULBText(ulb_book, '2', '5'), 'They said to him, "In Bethlehem of Judea, for this is what was written by the prophet,')
    self.assertEqual(getULBText(ulb_book, '2', '6'), ''''And you, Bethlehem, in the land of Judah, are not the least among the leaders of Judah, for from you will come a ruler who will shepherd my people Israel.'"''')
    self.assertEqual(getULBText(ulb_book, '4', '16'), 'The people who sat in darkness have seen a great light, and to those who sat in the region and shadow of death, upon them has a light arisen."')
    self.assertEqual(getULBText(ulb_book, '5', '9'), 'Blessed are the peacemakers, for they will be called sons of God.')

  def testCompareString(self):
    if os.path.exists(diff_file): os.remove(diff_file)
    compare('sources/test-tW-MAT.csv', 'sources/test-41-MAT.usfm', {})
    f = open('diffs/differences.csv', 'r').read()
    self.assertTrue('Therefore every scribe' in f)
    self.assertTrue('Jesus came up immediately from the water' in f)
    self.assertFalse('appeared to him in a dream, saying' in f)
    self.assertFalse('Joseph woke up from' in f)
    self.assertFalse('After they had departed' in f)
    self.assertFalse('When Herod died, behold,' in f)
    self.assertFalse('Then a scribe came to ' in f)
    self.assertFalse('The birth of Jesus Christ happened' in f)
    self.assertFalse('As he thought about these things' in f)
    self.assertFalse('I baptize you with water' in f)
    self.assertFalse('But if I drive out demons ' in f)
    self.assertFalse('And whoever speaks any word' in f)
    self.assertFalse('Matthew,,' in f)
    self.assertTrue('dove and alighting on him.' in f)
    self.assertEqual(len(open('diffs/differences.csv', 'r').readlines()), 2)

class TestExport(unittest.TestCase):

  def testloadConfig(self):
    config = loadConfig('sources/test-config.yaml')
    self.assertEqual(type(config), dict)
    self.assertEqual(len(config['aaron']['occurrences']), 5)
    self.assertEqual(len(config['aaron']['false_positives']), 2)

  def testconfigCheck(self):
    config = loadConfig('sources/test-config.yaml')
    self.assertTrue(configCheck('aaron', '1ch', '07', '38', config))
    self.assertFalse(configCheck('aaron', '1ch', '25', '12', config))
    self.assertFalse(configCheck('god', '1ch', '07', '38', config))

  def testConfigExport(self):
    config = loadConfig('sources/test-config.yaml')
    tw_list, tw_dict = loadtWs('../en_tw/bible')
    config = export('sources/test-tW-MAT.csv', config, tw_list)
    config = export('diffs/differences.csv', config, tw_list)
    self.assertTrue('scribe' in config)
    self.assertTrue('rc://en/ulb/book/1ch/25/12' in config['aaron']['false_positives'])
    self.assertTrue('rc://en/ulb/book/mat/13/52' in config['scribe']['occurrences'])
    self.assertTrue('rc://en/ulb/book/mat/03/16' in config['holyspirit']['occurrences'])
    self.assertFalse('rc://en/ulb/book/mat/08/21' in config['godthefather']['occurrences'])
    self.assertTrue('rc://en/ulb/book/mat/08/21' in config['godthefather']['false_positives'])
    self.assertTrue('rc://en/ulb/book/mat/08/21' in config['godthefather']['false_positives'])
    self.assertTrue('rc://en/ulb/book/mat/01/02' in config['father']['occurrences'])
    saveConfig('test-config.yaml', config)
    f = open('test-config.yaml', 'r').read()
    self.assertTrue(f.startswith('---'))
    self.assertTrue('rc://en/ulb/book/1ch/28/01' in f)
    self.assertTrue('rc://en/ulb/book/1ch/25/12' in f)
    self.assertTrue('holyspirit' in f)
    self.assertTrue('rc://en/ulb/book/mat/13/52' in f)
    self.assertFalse("? ''" in f)
    new_config = loadConfig('test-config.yaml')
    self.assertEqual(type(new_config), dict)

class TestloadtWs(unittest.TestCase):

  def testloadtWs(self):
    tw_list, tw_dict = loadtWs('../en_tw/bible')
    self.assertEqual(type(tw_list), list)
    self.assertEqual(type(tw_dict), dict)
    self.assertTrue('reward' in tw_list)
    self.assertTrue('reward' in tw_dict)
    self.assertTrue('god' in tw_list)
    self.assertFalse('God' in tw_list)
    self.assertFalse('God' in tw_dict)
    self.assertFalse('afather' in tw_list)
    self.assertTrue('deceit' in tw_dict['deceive'])
    self.assertTrue('heavenly Father' in tw_dict['godthefather'])

class TestfindNew(unittest.TestCase):

  def testfindNew(self):
    if os.path.exists('test-new_file.csv'):
      os.remove('test-new_file.csv')
    tw_list, tw_dict = loadtWs('../en_tw/bible')
    config = loadConfig('sources/test-config.yaml')
    findNew(tw_dict, 'sources/test-41-MAT.usfm', config, 'test-new_file.csv')
    f = open('test-new_file.csv', 'r').read()
    self.assertTrue('mat,13,22' in f)
    self.assertFalse('mat,9,38,send.txt,send,' in f)
    self.assertFalse('mat,13,22,world' in f)
    self.assertFalse('iyahweh' in f)


if __name__ == '__main__':
  unittest.main()
