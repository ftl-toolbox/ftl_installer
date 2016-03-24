# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 11:56:17 2016

@author: Mina Naghshnejad
"""

class Variant():
   openshift-enterpise = 0
   atomic-enterprise = 1
   origin = 2
   def __init__(self, Type):
        self.value = Type
   def __str__(self):
      if self.value == Variant.openshift-enterpise:
            return 'openshift-enterpise'
      if self.value == Variant.atomic-enterprise:
            return 'atomic-enterprise'
      if self.value == Variant.origin:
            return 'origin'
   def __eq__(self,y):
        return self.value==y.value