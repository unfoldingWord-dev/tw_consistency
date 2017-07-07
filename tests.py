#!/usr/bin/env python

import unittest
from process import *

class TestBooks(unittest.TestCase):

  def testDictionary(self):
    self.assertEqual('Jude', books['JUD'][0])
    self.assertEqual(len(books), 27)

class TestCompare(unittest.TestCase):

  def testgetULBText(self):
    ulb_book = open('test_data/test-41-MAT.usfm', 'r').readlines()
    self.assertEqual(getULBText(ulb_book, '1', '4'), 'Ram was the father of Amminadab, Amminadab the father of Nahshon, and Nahshon the father of Salmon.')
    self.assertEqual(getULBText(ulb_book, '13', '58'), 'And he did not do many miracles there because of their unbelief.')
    self.assertEqual(getULBText(ulb_book, '13', '35'), 'This was in order that what had been said through the prophet might come true, when he said, "I will open my mouth in parables. I will say things that were hidden from the foundation of the world."')
    self.assertEqual(getULBText(ulb_book, '1', '6'), 'Jesse was the father of David the king. David was the father of Solomon by the wife of Uriah.')
    self.assertEqual(getULBText(ulb_book, '2', '5'), 'They said to him, "In Bethlehem of Judea, for this is what was written by the prophet,')
    self.assertEqual(getULBText(ulb_book, '2', '6'), ''''And you, Bethlehem, in the land of Judah, are not the least among the leaders of Judah, for from you will come a ruler who will shepherd my people Israel.'"''')
    self.assertEqual(getULBText(ulb_book, '4', '16'), 'The people who sat in darkness have seen a great light, and to those who sat in the region and shadow of death, upon them has a light arisen."')
    self.assertEqual(getULBText(ulb_book, '5', '9'), 'Blessed are the peacemakers, for they will be called sons of God.')

class TestExport(unittest.TestCase):

  def testloadConfig(self):
    config = loadConfig('test_data/test-config.yaml')
    self.assertEqual(type(config), dict)
    self.assertEqual(len(config['aaron']['occurrences']), 5)
    self.assertEqual(len(config['aaron']['false_positives']), 2)

  def testconfigCheck(self):
    config = loadConfig('test_data/test-config.yaml')
    self.assertTrue(configCheck('aaron', '1ch', '07', '38', config))
    self.assertTrue(configCheck('aaron', '1ch', '07', '38', config))
    self.assertFalse(configCheck('aaron', '1ch', '25', '12', config))
    self.assertFalse(configCheck('aaron', '1ch', '25', '12', config))
    self.assertFalse(configCheck('god', '1ch', '07', '38', config))

  def testConfigExport(self):
    config = loadConfig('test_data/test-config.yaml')
    tw_list, tw_dict = loadtWs('../en_tw/bible')
    config = export('test_data/test-differences.csv', config, tw_list)
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
    os.remove('test-config.yaml')

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
    config = loadConfig('test_data/test-config.yaml')
    tw_list, tw_dict = loadtWs(os.path.join(tw_dir, 'bible'))
    findNew(tw_dict, 'test_data/test-41-MAT.usfm', config, 'test-tw_review.csv')
    f = open('test-tw_review.csv', 'r').read()
    self.assertTrue('mat,13,22' in f)
    self.assertTrue('TRUE,mat,1,20,messenger.md' in f)
    self.assertFalse('mat,9,38,send.txt,send,' in f)
    self.assertFalse('mat,13,22,world' in f)
    self.assertFalse('iyahweh' in f)
    self.assertFalse('toc1' in f)
    os.remove('test-tw_review.csv')

  def testfindRemoved(self):
    config = loadConfig('test_data/test-config.yaml')
    tw_list, tw_dict = loadtWs(os.path.join(tw_dir, 'bible'))
    findNew(tw_dict, 'test_data/test-41-MAT.usfm', config, 'test-tw_review.csv')
    f = open('test-tw_review.csv', 'r').read()
    self.assertTrue('FALSE,mat,01,20,angel.md' in f)
    self.assertFalse('FALSE,1ch,01,05,aaron.md' in f)
    os.remove('test-tw_review.csv')

if __name__ == '__main__':
  unittest.main()
