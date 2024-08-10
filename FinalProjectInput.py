''' Joseph Neveu
    ID: 1161167 '''

import csv 
from datetime import datetime

class inventoryManager:
    def __init__(self):
        self.item = {}

    def loadData(self, manufactuerFile, priceFile, serviceDate file): # defines load data method
        self.loadManufactuers(manufactuerFile) # first parameter 
        self.loadPrices(priceFile) # second parameter
        self.loadServiceDate(serviceDateFile) # third parameter

    