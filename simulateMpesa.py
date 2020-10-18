import argparse # argument parser
import requests
import json
from templates import acceptedResponse, cancelledResponse


headers = {             
  'Content-Type': 'application/json',             
  'User-Agent': 'python-requests/2.4.3 CPython/3.4.0'
}
 

def accept(response):
  response = requests.post(
    url, 
    data=json.dumps(response), 
    headers=headers
  )
  
  return response.json()

# find currency in csv file
def reject(s):
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
    parser = argparse.ArgumentParser(description='Simulate Mpesas.')
    parser.add_argument("accept", help="accept payment.")
    args = parser.parse_args()
    return args


# run code
if __name__ == '__main__':  

  #  mpesa callback url
  url ="https://api.yourmedicare.online/mpesa-callback"
 
  args = parseArgs()

  if args.accept:
    s = acceptedResponse.safe_substitute(CheckoutRequestID='idjfhdhfjdf')
    print(s)
    # result = accept(s)
    # print(result)
  
  # if args.cancell:
  #   print(s)
  #   s = cancelledResponse.safe_substitute(CheckoutRequestID='idjfhdhfjdf')
  #   # result = reject(s)
  #   # print(result)
      
  else: 
      print('expecting arguments. use -h flag for help')
  
