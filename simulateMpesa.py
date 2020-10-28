#!/usr/bin/env python3

import argparse # argument parser
import requests
import json
from templates import mpesa
import ast 


headers = {             
  'Content-Type': 'application/json',             
  'User-Agent': 'python-requests/2.4.3 CPython/3.4.0'
}
 

def accept(response, url):
  response = requests.post(
    url, 
    data=json.dumps(response), 
    headers=headers
  )
  
  return response.json()

# find currency in csv file
def reject(s, url):
    # Copy csv to a local file
  response = requests.post(
    url, 
    data=json.dumps(s), 
    headers=headers
    )
  return response.json()
    
            

# terminal argument parser
def parseArgs():
    # create a parser
    parser = argparse.ArgumentParser(description='Simulate Mpesa Response.')
    parser.add_argument("--success", action='store_true', help="successfull payment.")
    parser.add_argument("--failed", action='store_true', help="Failed payment.")
    parser.add_argument("checkout", help="Mpesa checkout request ID.")
    parser.add_argument("url", help="callback url.")
    args = parser.parse_args()
    return args


# run code
if __name__ == '__main__':  
 
  args = parseArgs()

  if args.success:
    s = mpesa.acceptedResponse.safe_substitute(CheckoutRequestID=args.checkout)
    s = ast.literal_eval(s)
    result = accept(s, args.url)
    print(result)
  
  elif args.failed:
    s = mpesa.cancelledResponse.safe_substitute(CheckoutRequestID=args.checkout)
    s = ast.literal_eval(s)
    result = reject(s, args.url)
    print(result)
      
  else: 
      print('expecting arguments. use -h flag for help')
  
