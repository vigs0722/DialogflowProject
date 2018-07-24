@@ -1,86 +1,92 @@
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
     req = request.get_json(silent=True, force=True)

     print("Request:")
     print(json.dumps(req, indent=4))

     # res = makeWebhookResult(req)
     res = get_currency_rate(req)

     res = json.dumps(res, indent=4)
     print(res)
-    r = make_response(res)
-    r.headers['Content-Type'] = 'application/json'
-    return r
+    # r = make_response(res)
+    # res.headers['Content-Type'] = 'application/json'
+    return res

-def get_currency_rate():
+def get_currency_rate(req):
 #
-  base_url = 'http://api.fixer.io/latest'
-
-  if req.get("result").get("action") != "shipping.cost":
+  base_url = 'http://data.fixer.io/api/latest'
+  # print (base_url)
+  if req.get("result").get("action") != "currency.convert":
       return {}
   result = req.get("result")
   parameters = result.get("parameters")
-  currency = parameters.get("currency")
-  rate_in = parameters.get("rate_in")
+  # print (parameters)
+  base_currency = parameters.get("currency-from")
+  to_currency = parameters.get("currency-to")
+  amount = parameters.get("amount")
+  # print (base_currency)
+  api_key = "?access_key=8c378b6c285d976080cc2ff8f0418035"
+
+  query = base_url + api_key + '&symbols=%s' % (to_currency)
+  print (query)

-  query = base_url + '?base=%s&symbols=%s' % (currency, rate_in)
   try:
     response = requests.get(query)
-    print("[%s] %s" % (response.status_code, response.url))
+    # print ("This is the response:")
+    # print (response)
+
+    # print("[%s] %s" % (response.status_code, response.url))
     if response.status_code != 200:
       response = 'N/A'
       return response
     else:
       rates = response.json()
-      rate_in_currency = rates["rates"][rate_in]
-      return rate_in_currency
+      print ("Rates:")
+      print(json.dumps(rates, indent=4))
+
+      rates_field = rates.get ("rates")
+      just_rate = rates_field.get (to_currency)
+      converted_amount = amount * just_rate
+
+      speech = "You will get" + ' %s %s' % (converted_amount, to_currency)
+      print("Speech:")
+      print(speech)
+      return {
+            "speech": speech,
+            "displayText": speech,
+            #"data": {},
+            #"contextOut": [],
+            "source": "CurrencyConvertor"
+        }
+
   except requests.ConnectionError as error:
     print error
     sys.exit(1)

-def makeWebhookResult(req):
-    if req.get("result").get("action") != "shipping.cost":
-        return {}
-    result = req.get("result")
-    parameters = result.get("parameters")
-    zone = parameters.get("bank-name")
-
-    cost = {'Andhra Bank':'6.85%', 'Allahabad Bank':'6.75%', 'Axis Bank':'6.5%', 'Bandhan bank':'7.15%', 'Bank of Maharashtra':'6.50%', 'Bank of Baroda':'6.90%', 'Bank of India':'6.60%', 'Bharatiya Mahila Bank':'7.00%', 'Canara Bank':'6.50%', 'Central Bank of India':'6.60%', 'City Union Bank':'7.10%', 'Corporation Bank':'6.75%', 'Citi Bank':'5.25%', 'DBS Bank':'6.30%', 'Dena Bank':'6.80%', 'Deutsche Bank':'6.00%', 'Dhanalakshmi Bank':'6.60%', 'DHFL Bank':'7.75%', 'Federal Bank':'6.70%', 'HDFC Bank':'5.75% to 6.75%', 'Post Office':'7.10%', 'Indian Overseas Bank':'6.75%', 'ICICI Bank':'6.25% to 6.9%', 'IDBI Bank':'6.65%', 'Indian Bank':'4.75%', 'Indusind Bank':'6.85%', 'J&K Bank':'6.75%', 'Karnataka Bank':'6.50 to 6.90%', 'Karur Vysya Bank':'6.75%', 'Kotak Mahindra Bank':'6.6%', 'Lakshmi Vilas Bank':'7.00%', 'Nainital Bank':'7.90%', 'Oriental Bank of Commerce':'6.85%', 'Punjab National Bank':'6.75%', 'Punjab and Sind Bank':'6.4% to 6.80%', 'Saraswat bank':'6.8%', 'South Indian Bank':'6% to 6.75%', 'State Bank of India':'6.75%', 'Syndicate Bank':'6.50%', 'Tamilnad Mercantile Bank Ltd':'6.90%', 'UCO bank':'6.75%', 'United Bank Of India':'6%', 'Vijaya Bank':'6.50%', 'Yes Bank':'7.10%'}
-
-    speech = "The interest rate of " + zone + " is " + str(cost[zone])
-    print("Response:")
-    print(speech)
-    return {
-        "speech": speech,
-        "displayText": speech,
-        #"data": {},
-        #"contextOut": [],
-        "source": "BankRates"
-    }

 if __name__ == '__main__':
     port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
