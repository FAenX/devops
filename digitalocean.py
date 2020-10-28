#!/usr/bin/env python3

import os
import argparse # argument parser
import requests
import json
# import ast
# settings.py
from dotenv import load_dotenv
from string import Template
import pprint 

# increased verbosity
load_dotenv(verbose=True)

DO_TOKEN = os.getenv('DO_TOKEN')

class DigitalOceanWrapper:
    def __init__(self):       
        self.pre_headers = {             
            'Content-Type': 'application/json',             
            'User-Agent': 'python-requests/2.4.3 CPython/3.4.0',
            'Authorization': 'Bearer {}'.format(DO_TOKEN)
        }
        self.droplets_endpoint = "https://api.digitalocean.com/v2/droplets"
        self.domains_endpoint = "https://api.digitalocean.com/v2/domains"
        self.domain_records_endpoint = Template("https://api.digitalocean.com/v2/domains/$domain_name/records")

    # list droplets
    def list_droplets(self):        
        # Copy csv to a local file
        response = requests.get(
            self.droplets_endpoint, 
            headers=self.pre_headers,
        )

        return response.json()

     # list domains
    def list_domains(self):        
        # Copy csv to a local file
        response = requests.get(
            self.domains_endpoint, 
            headers=self.pre_headers,
        )

        return response.json()

    # domain records
    def domains_records(self, domain_name):        
        response = requests.get(
            self.domain_records_endpoint.safe_substitute(domain_name=domain_name), 
            headers=self.pre_headers,
        )

        return response.json()

    def add_domain_record(self, domain_name, name, ip, **args):
      response = requests.post(
        self.domain_records_endpoint.safe_substitute(domain_name=domain_name),
        headers=self.pre_headers,        
        data=json.dumps({
            "type": "A",
            "name": "{}".format(name),
            "data": '{}'.format(ip),
            "priority": "null",
            "port": "null",
            "ttl": 1800,
            "weight": "null",
            "flags": "null",
            "tag": "null"
          })
        )
      return response.json()
    
            

# terminal argument parser
def parseArgs():
    # create a parser
    parser = argparse.ArgumentParser(description='Digital ocean Droplets.')
    parser.add_argument("--droplets", action='store_true', help="List droplets.")
    parser.add_argument("--domains", action='store_true', help="List domains.")
    parser.add_argument("--domain-records", metavar=('domain.com'), help="domain to show records for")
    parser.add_argument("--add-domain-record", nargs=3, metavar=('domain.com', 'name', '127.0.0.1'), help="domain to add records for")
    args = parser.parse_args()
    return args


# run code
if __name__ == '__main__':  
 
  args = parseArgs()
  print(args)
  pp = pprint.PrettyPrinter(width=41, compact=True)

  if args.domains:
    domains = DigitalOceanWrapper().list_domains()['domains']
    domain_names = [i['name'] for i in domains]
    pp.pprint(domain_names)

  if args.droplets:
    droplets = DigitalOceanWrapper().list_droplets()['droplets']
    droplet_names = [i['name'] for i in droplets]
    pp.pprint(droplet_names)

  if args.domain_records:
    records = DigitalOceanWrapper().domains_records(args.domain_records)['domain_records']
    domain_records = [i['data'] for i in records]
    pp.pprint(domain_records)
  
  if args.add_domain_record:
    records = DigitalOceanWrapper().add_domain_record(
      args.add_domain_record[0], 
      args.add_domain_record[1],
      args.add_domain_record[2]
      )
    # domain_records = [i['data'] for i in records]
    pp.pprint(records)
    # print