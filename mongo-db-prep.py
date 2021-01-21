#!/usr/bin/env python3
from string import Template
import argparse
import subprocess
import sys
from pymongo import MongoClient

def create_user(**kwargs):
    client = MongoClient("mongodb://{}:{}@{}:{}".format(
        kwargs['mongo_admin'], 
        kwargs['mongo_admin_password'], 
        kwargs['mongo_host'], 
        kwargs['mongo_port']
    ))

    db = client[kwargs['database']]

    user = db.command('createUser', kwargs['user'], pwd=kwargs['password'], roles=['readWrite'])
    print(user)


# argument parser
def parseArgs():
    # create a parser
    parser = argparse.ArgumentParser(description='App options.')
    parser.add_argument("-- database", help="optional database, if not provided it will create a test database")
    parser.add_argument("--password", help="optional password, if not provided it will autogenerate a password")
    parser.add_argument("--user", help="optional user, if not provided it will create a test")

    return parser.parse_args()

if __name__ == '__main__':
    args = parseArgs()
    # print(args)
    user = args.user
        
    database = 'test'
    if args.database:
        database = args.database

    user = 'test'
    if args.user:
        user = args.user

    password='T72askY8Am3Yt3Q2'
    if args.password:
        password = args.password 

    mongo_admin = input('mongo-admin: ')

    mongo_admin_password = input('mongo-admin password: ')

    mongo_host = input('host: ')

    mongo_port = input('port: ')

    create_user(
            mongo_admin_password=mongo_admin_password, 
            mongo_admin=mongo_admin, 
            mongo_host=mongo_host, 
            mongo_port=mongo_port,
            database=database,
            user=user,
            password=password
        )

    # create_user()

   
   


    
