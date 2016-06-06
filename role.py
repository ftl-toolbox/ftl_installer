# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:16:52 2016

@author: mina
"""

class Role():
   master = 0
   node = 1
   etcd = 2
   lb= 3
   storage= 4
   def __init__(self, Type):
        self.value = Type
   def __str__(self):
      if self.value == Role.master:
            return 'master'
      if self.value == Role.node:
            return 'node'
      if self.value == Role.etcd:
            return 'etcd'
      if self.value == Role.lb:
            return 'lb'
      if self.value==Role.storage:
            return 'storage'
    
   def __eq__(self,y):
        return self.value==y.value