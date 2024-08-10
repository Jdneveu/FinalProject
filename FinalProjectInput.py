''' Joseph Neveu
    ID: 1161167 '''

import csv 
from datetime import datetime

class inventoryManager:
    def __init__(self):
        self.item = {} #starts self.items dictionary 

    def loadData(self, manufacturerFile, priceFile, serviceDateFile): # defines load data method
        self.loadManufacturers(manufacturerFile) # first parameter 
        self.loadPrices(priceFile) # second parameter
        self.loadServiceDates(serviceDateFile) # third parameter

    def loadManufacturers(self, file):
        with open(file, 'r') as f: 
            reader = csv.reader(f)
            for row in reader: 
                itemID, manufacturer, itemType, *damaged = row # seperates each row by identifier 
                self.items[itemID] = { # adds entry to self.itme dictionary 
                    'manufacturer': manufacturer.strip(),
                    'itemType': itemType.strip(),
                    'damaged': 'damaged' if damaged and damaged[0].strip().lower() == 'damaged'
            else ''
                }

    def loadPrices(self, file): 
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                itemId, price = row # unpacks row into itemId and price 
                if itemId in self.items: 
                    self.items[itemId]['price'] = float(price) # adds price to item in dictionary and converts to float

    def loadServiceDates(self, file):
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                itemId, serviceDate = row # unpacks row into item Id and service date 
                if itemId in self.items:
                    self.item[itemId]['serviceDate'] = datetime.strptime(serviceDate.strip(), '%m/%d/%Y') # adds service date to dictionary 

    def generateReports(self): # calls 4 methods to generate inventory reports that will be defined following this
        self.generateFullInventory()
        self.generateItemTypeInventory()
        self.generatePastServiceDateInventory()
        self.generateDamagedInventory()

    def generateFullInventory(self): #creates report with all inventory items sorted by manufaturer
        items = sorted(self.items.items(), key=lambda x: x[]['manufacturer']) #sorts items by manufacturer
        with open('FullInventory.csv', 'w', newline = '') as f:
            writer = csv.writer(f)
            for itemId, item in items: # iterates over each item and writes to csv file
                writer.writerow([itemId, item['manufacturer'], item['itemType'], item['price'], item['serviceDate'].strftime('%m/%d/%Y'), item['damaged']]) 

    def generateItemTypeInventory(self):
        types = {} # starts empty dictionary to store items by type
        for itemId, item in self.items.items(): #checks if item is key in types dictionary
            if item['itemType'] not in types: # if not then adds to new list for item type 
                types[item['itemType']].append((itemId, item))

        for itemType, items in types.items():
            items = sorted(items, key=lambda x: x[]) #sorts items of each type by ID
            with open(f'{itemType}Inventory.csv', 'w', newline = '') as f: 
                writer = csv.writer(f)
                for itemId, item in items: #iterates over each item and writes to csv file
                    writer.writerow([itemId, item['manufacturer'], item['price'], item['serviceDate'].strftime('%m/%d/%Y'), item['damaged']]) 
