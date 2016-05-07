from unittest import TestCase

import crdtpy

class sampleTest(TestCase):
  def isDummy():
    s = crdtpy.dummy()
    self.assertEqual(s,'dummy')
