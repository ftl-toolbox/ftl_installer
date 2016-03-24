# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:30:17 2016

@author: mina
"""

import yaml

class Workflow:
    def __init__(adress,self):      
      with open(adress, 'r') as f:
          doc = yaml.load(f)
          self.variant = doc ["workflow"]["Variant"]
          self.role = doc ["workflow"]["Role"]
    def setVariant(v,self):
        self.variant=v
    def setRole(r,self):
        self.role=r
    def yamlPrinter(self):
        data = dict(
            Variant = self.variant,
            Role = self.role
            )
        with open('data.yml', 'w') as outfile:
            outfile.write( yaml.dump(data, default_flow_style=True) )
        

    
