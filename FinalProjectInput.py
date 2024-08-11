''' Joseph Neveu
    ID: 1161167 '''

import csv 
from datetime import datetime

class inventoryManager:
    def __init__(self):
        self.items = {} #starts self.items dictionary 

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
                    'damaged': 'damaged' if damaged and damaged[0].strip().lower() == 'damaged' else ''
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
                    self.items[itemId]['serviceDate'] = datetime.strptime(serviceDate.strip(), '%m/%d/%Y') # adds service date to dictionary 

    def generateReports(self): # calls 4 methods to generate inventory reports that will be defined following this
        self.generateFullInventory()
        self.generateItemTypeInventory()
        self.generatePastServiceDateInventory()
        self.generateDamagedInventory()

    def generateFullInventory(self): #creates report with all inventory items sorted by manufaturer
        items = sorted(self.items.items(), key=lambda x: x[1]['manufacturer']) #sorts items by manufacturer
        with open('FullInventory.csv', 'w', newline = '') as f:
            writer = csv.writer(f)
            for itemId, item in items: # iterates over each item and writes to csv file
                writer.writerow([itemId, item['manufacturer'], item['itemType'], item['price'], item['serviceDate'].strftime('%m/%d/%Y'), item['damaged']]) 

    def generateItemTypeInventory(self): # creates report for inventory by item type
        types = {} # starts empty dictionary to store items by type
        for itemId, item in self.items.items(): #checks if item is key in types dictionary
            if item['itemType'] not in types: # if not then adds to new list for item type 
                types[item['itemType']] = []
            types[item['itemType']].append((itemId, item))

        for itemType, items in types.items():
            items = sorted(items, key=lambda x: x[0]) #sorts items of each type by ID
            with open(f'{itemType}Inventory.csv', 'w', newline = '') as f: 
                writer = csv.writer(f)
                for itemId, item in items: #iterates over each item and writes to csv file
                    writer.writerow([itemId, item['manufacturer'], item['price'], item['serviceDate'].strftime('%m/%d/%Y'), item['damaged']]) 

    def generatePastServiceDateInventory(self): # creates report for items past service date
        today = datetime.today() # gets current date and time 
        items = [(itemId, item) for itemId, item in self.items.items() if item['serviceDate'] < today] #lists items past service date
        items = sorted(items, key = lambda x: x[1]['serviceDate']) # sorts by service date
        with open('PastServiceDateInventory.csv', 'w', newline = '') as f:
            writer = csv.writer(f)
            for itemId, item in items: #iterates over items and writes to csv file
                writer.writerow([itemId, item['manufacturer'], item['itemType'], item['price'], item['serviceDate'].strftime('%m/%d/%Y'), item['damaged']])

    def generateDamagedInventory(self): # creates report of damaged items
        items = [(itemId, item) for itemId, item in self.items.items() if item['damaged']] #creates list of damaged items
        items = sorted(items, key = lambda x: x[1]['price'], reverse = True) # sorts by price 
        with open('DamagedInventory.csv', 'w', newline = '') as f:
            writer = csv.writer(f)
            for itemId, item in items: #iterates over items and writes to csv file
                writer.writerow([itemId, item['manufacturer'], item['itemType'], item['price'], item['serviceDate'].strftime('%m/%d/%Y')])

#main execution 
if __name__ == "__main__": #check to see if being run directly
    manager = inventoryManager() #creates  inctance in inventoryManager class
    manager.loadData('ManufacturerList.csv', 'PriceList.csv', 'ServiceDatesList.csv') # calls load data method to load data from csv files
    manager.generateReports() # calls generate reports method
 
