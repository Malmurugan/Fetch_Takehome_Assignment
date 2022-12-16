import json
from flask import Flask, request
import string
import random
import math
import logging
logging .basicConfig(level=logging.DEBUG)

app = Flask(__name__)

""" Global in-memory storage (dictionary) to store the receipts json  """
global dictionaryReceipts
dictionaryReceipts = {}
""" Global in-memory storage (dictionary) to store the spoints for each receipt """
global dictionaryPoints
dictionaryPoints = {}

counter = 1

def calculate_points(dict_org,id):
    """
    calculate_points function calculates the points for every new input and store the result in dictionaryPoints.

    :param dict_org: Input receipt dictionary.
    :param id: ID of that receipt.
    """ 
    points = 0 
    try:
        total = float(dict_org['total']) 
        items = dict_org['items']
        date_dt = int(dict_org['purchaseDate'][-1])
        hour = dict_org['purchaseTime'].split(':')[0]
        retailerAlphaNum = ''.join(ch for ch in str(dict_org['retailer']) if ch.isalnum())

    except:
        app.logger.info("Error:  Values missing in JSON receipt")
        exit()

    """ Rule 1: One point for every alphanumeric character in the retailer name."""
    points = points + len(retailerAlphaNum)

    """ Rule 2: 50 points if the total is a round dollar amount with no cents."""
    if float(total).is_integer():
        points = points + 50

    """ Rule 3: 25 points if the total is a multiple of 0.25"""
    if total%(0.25)==0:
        points = points + 25
    
    """ Rule 4: 5 points for every two items on the receipt."""
    itemLenFactor = int(len(items)/2)
    points = points + 5*itemLenFactor

    """ Rule 5: If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned."""
    for item in items:
        try:
            descriptionLen = len(item['shortDescription'])
        except:
            app.logger.info("Error:  Values missing in JSON receipt")
            exit()
        if descriptionLen%3 == 0:
            try:
                price = math.ceil((float(item['price'])) * 0.2)
            except:
                app.logger.info("Error:  Values missing in JSON receipt")
                exit()
            points = points + price

    """ Rule 6: 6 points if the day in the purchase date is odd."""
    if(date_dt%2 != 0):
        points = points + 6
    
    """ Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm."""
    if (hour == '14' or hour == '15'):
        points = points + 10
    
    dictionaryPoints[id] = points
    app.logger.info("Success:  Points Successfully calculated for the JSON receipt.")


@app.route('/')
def index():
    return '<p><b>Project</b>: Fetch Rewards Take Home Assessment <br> <b>Author</b>: Malmurugan Sukumar <br> <b> Email</b>: msuku002@ucr.edu</p>'

@app.route('/receipts/<id>/points', methods = ['GET'])
def get_points(id):
    """
    get_points function returns the points the input ID. 

    :param id: ID of that receipt.
    """ 
    try:
        points = dictionaryPoints[id]
    except:
                app.logger.info("Error:  Invalid receipt ID")
                exit()
    
    app.logger.info("Success:  Points Successfully returned for the receipt ID")
    return json.dumps({"points":points})

@app.route('/receipts/process', methods = ['POST'])
def add_receipt():
    """
    add_receipt accepts the JSON receipt, generates a random alphanumeric id and calls calculate_points.
    """ 
    id = ''.join(random.choices(string.ascii_uppercase +string.digits, k=7))
    """Global counter variable to make sure that very id is unique"""
    global counter
    id = id + str(counter)
    counter = counter + 1 
    try:
        dictionaryReceipts[id] = request.json
    except:
        app.logger.info("Error:  Invalid file format. Please upload a JSON file.")
        exit()
    app.logger.info("Log:  Receipt added successfully")
    calculate_points(request.json,id)
    return json.dumps({"id":id})

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = int("3000"), debug = True)
