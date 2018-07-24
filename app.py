#!/usr/bin/env python

import urllib
import json
import os

# copied from FixerIo.py
# Fixer.io is a free JSON API for current and historical foreign exchange rates.
# It relies on daily feeds published by the European Central Bank.

import sys
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])


def webhook():
    print("START OF PROGRAM")
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))


    # res = makeWebhookResult(req)

    res = send_request_to_vizru(req)

    res = json.dumps(res, indent=4)
    print(res)
    # r = make_response(res)
    # res.headers['Content-Type'] = 'application/json'
    return res

def send_request_to_vizru(req):
    if req.get("result").get("action") == "cust.logbug":
        request = "bug"
        result = req.get("result")
        parameters = result.get("parameters")

        email = parameters.get("email")
        screen = parameters.get("screen")
        description = parameters.get("description")

        base_url = 'https://viz-demo.vizru.com/workflow.trigger/'
        api_key = "5b52a7ca55ebc96c55922992?"

        query = base_url+api_key+"email=" + email + "&screen=" + screen + "&description=" + description+"&request=" + request
        print(query)

    elif req.get("result").get("action") == "cust.logfeature":
        request = "feature"
        result = req.get("result")
        parameters = result.get("parameters")

        email = parameters.get("email")
        description = parameters.get("description")
        date = parameters.get("date")

        base_url = 'https://viz-demo.vizru.com/workflow.trigger/'
        api_key = "5b52a7ca55ebc96c55922992?"

        query = base_url+api_key+"email=" + email + "&description=" + description + "&date=" + date + "&request=" + request
        print(query)

    elif req.get("result").get("action") == "cust.check_status":
        request = "check_status"
        result = req.get("result")
        parameters = result.get("parameters")

        email = parameters.get("email")
        case_number = parameters.get("casenumber")
        date = parameters.get("date")

        base_url = 'https://viz-demo.vizru.com/workflow.trigger/'
        api_key = "5b52a7ca55ebc96c55922992?"

        query = base_url+api_key+"email=" + email + "&case_number=" + str(case_number) + "&date=" + date + "&request=" + request
        print(query)

    else:
        return{}


    try:
      response = requests.get(query)
      print ("This is the response:")
      print (response)

      # print("[%s] %s" % (response.status_code, response.url))
      if response.status_code != 200:
        response = 'N/A'
        return response
      else:
        vizru_response = response.json()
        vizru_response = vizru_response [0]
        print ("Vizru Response")
        print(json.dumps(vizru_response, indent=4))

        #rates_field = rates.get ("rates")
        #just_rate = rates_field.get (to_currency)
        #converted_amount = amount * just_rate


        speech = "I submitted your request to Vizru. Here is Vizru's response: " + (json.dumps(vizru_response, indent=4))
        print("Speech:")
        print(speech)
        return {
              "speech": speech,
              "displayText": speech,
              #"data": {},
              #"contextOut": [],
              "source": "CustomerService"
          }

    except requests.ConnectionError as error:
      print error
      sys.exit(1)






def get_currency_rate(req):
#
  base_url = 'http://data.fixer.io/api/latest'
  # print (base_url)
  if req.get("result").get("action") != "currency.convert":
      return {}
  result = req.get("result")
  parameters = result.get("parameters")
  # print (parameters)
  base_currency = parameters.get("currency-from")
  to_currency = parameters.get("currency-to")
  amount = parameters.get("amount")
  # print (base_currency)
  api_key = "?access_key=8c378b6c285d976080cc2ff8f0418035"

  query = base_url + api_key + '&symbols=%s' % (to_currency)
  print (query)

  try:
    response = requests.get(query)
    # print ("This is the response:")
    # print (response)

    # print("[%s] %s" % (response.status_code, response.url))
    if response.status_code != 200:
      response = 'N/A'
      return response
    else:
      rates = response.json()
      print ("Rates:")
      print(json.dumps(rates, indent=4))

      rates_field = rates.get ("rates")
      just_rate = rates_field.get (to_currency)
      converted_amount = amount * just_rate

      speech = "You will get" + ' %s %s' % (converted_amount, to_currency)
      print("Speech:")
      print(speech)
      return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            "source": "CurrencyConvertor"
        }

  except requests.ConnectionError as error:
    print error
    sys.exit(1)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
