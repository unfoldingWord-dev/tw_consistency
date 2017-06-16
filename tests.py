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
    f = open('57-TIT.usfm', 'r').read()
    names = ['Artemas', 'Tychicus', 'Zenas', 'Apollos', 'Paul']
    for x in names:
      self.assertTrue(x in f)

  def testNoUpdate(self):
    getUSFM(False)
    f = open('57-TIT.usfm', 'r').read()
    names = ['Artemas', 'Tychicus', 'Zenas', 'Apollos', 'Paul']
    for x in names:
      self.assertTrue(x in f)

class TestCompare(unittest.TestCase):

  def testgetULBText(self):
    ulb_book = open('test-41-MAT.usfm', 'r').readlines()
    self.assertEqual(getULBText(ulb_book, '1', '4'), 'Ram was the father of Amminadab, Amminadab the father of Nahshon, and Nahshon the father of Salmon.')
    self.assertEqual(getULBText(ulb_book, '13', '58'), 'And he did not do many miracles there because of their unbelief.')
    self.assertEqual(getULBText(ulb_book, '13', '35'), 'This was in order that what had been said through the prophet might come true, when he said, "I will open my mouth in parables. I will say things that were hidden from the foundation of the world."')
    self.assertEqual(getULBText(ulb_book, '1', '6'), 'Jesse was the father of David the king. David was the father of Solomon by the wife of Uriah.')
    self.assertEqual(getULBText(ulb_book, '2', '5'), 'They said to him, "In Bethlehem of Judea, for this is what was written by the prophet,')
    self.assertEqual(getULBText(ulb_book, '2', '6'), ''''And you, Bethlehem, in the land of Judah, are not the least among the leaders of Judah, for from you will come a ruler who will shepherd my people Israel.'"''')
    self.assertEqual(getULBText(ulb_book, '4', '16'), 'The people who sat in darkness have seen a great light, and to those who sat in the region and shadow of death, upon them has a light arisen."')
    self.assertEqual(getULBText(ulb_book, '5', '9'), 'Blessed are the peacemakers, for they will be called sons of God.')

  def testCompareString(self):
    compare('test-tW-MAT.csv', 'test-41-MAT.usfm')
    f = open('test-41-MAT.usfm.diffs', 'r').read()
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
    os.remove('test-41-MAT.usfm.diffs')


if __name__ == '__main__':
  unittest.main()
