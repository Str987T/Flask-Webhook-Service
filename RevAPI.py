#!/usr/bin/python3

from flask import Flask, json, request, abort
from waitress import serve
import datetime
import requests
import mysql.connector
app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():

            #Sorting out the relevant info from the dump into variables
             customer_name = request.json['transaction']['Customer Name']
             customer_id = request.json['transaction']['Customer ID']
             cashier_name = request.json['transaction']['Cashier Name']
             payment_id = request.json['transaction']['Payment ID']
             counter_number = request.json['transaction']['Counter Number']
             total = request.json['transaction']['Total']
             date = request.json['transaction']['Date']

             connection = mysql.connector.connect(
               user="database-user",
               password="database-pass",
               host="127.0.0.1", #Localhost/IPv4 for remote Database
               database="database-name",
               port="database-port"

             )

             cursor = connection.cursor()
             add_user = """INSERT INTO database.table_name
             (customer_name, customer_id, cashier_name, payment_id, counter_number, total, date)
             VALUES (%s,%s,%s,%s,%s,%s,%s)"""
             data_user = (customer_name, customer_id, cashier_name, payment_id, counter_number, total, date)
             cursor.execute(add_user, data_user)
             connection.commit()
             cursor.close()
             connection.close()

             #Format
             _message = "============================\n"
             _message += "\nCustomer Name: *{}*"
             _message += "\nCustomer ID: *{}*"
             _message += "\nCashier Name: *{}*"
             _message += "\nPayment ID: *{}*"
             _message += "\nCounter No: ***** *{}* *****"
             _message += "\nTotal: *{}*"
             _message += "\nDate: *{}*"
             _message += "\n============================"

             #The Slack Webhook URL on which all our data is to be sent
             #Test webhook
             webhook_url = 'Slack-WEBHOOK-URL'

             #Preparing for sending data. Headers and body components initialized
             headers = {'Content-type': 'application/json'}
             message = _message.format(
                        customer_name,
                        customer_id,
                        cashier_name,
                        payment_id,
                        counter_number,
                        total,
                        date
                    )

             #The message will be jsonified here
             body = {
                        'username': 'Transaction Details',
                        'text': message
                    }

             #Sending data on Slack now
             response = requests.post(webhook_url, data=json.dumps(body), headers=headers)

             return 'success', 200

@app.route("/perform-test", methods=['GET'])
def test():
    return 'Service Active!', 200

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
