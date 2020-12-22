#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import requests
import json
from prettytable import PrettyTable
import urllib3
import csv
from getpass import getpass
urllib3.disable_warnings()

# Enter TACACS credentials via Prompt
username = input("Username: ")
password = getpass("Password: ")

headers ={
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}

yang_interfaces = "/ietf-interfaces:interfaces"

### Reading routers parameters from CSV file and managing data like a dictionary
with open('/Users/amanueli/Documents/DevNet/Scripts/DevNet/routers.csv', mode='r') as csv_file:
    #Reading CSV file 
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        #Setting up variables
        router_ipaddr = row["ipaddr"]
        router_port= row["port"]

        #Making RESTCONF request
        url_router = f"https://{router_ipaddr}:{router_port}/restconf/data"
        interfaces = requests.get(url=f"{url_router}{yang_interfaces}", headers= headers, auth=(username, password), verify= False).json()["ietf-interfaces:interfaces"]["interface"]

        #Preparing PrettyTable header
        interfaces_table = PrettyTable(['Interface name', 'Description','Enabled', 'IPAddress'])
        #Setting up CSV header
        fieldnames = ['host_ipaddr','if_name', 'description', 'enabled', 'if_ipaddr']

        with open('/Users/amanueli/Documents/DevNet/Scripts/DevNet/output_interfaces.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for interface in interfaces:
                if "ietf-ip:ipv4" in interface:
                    if "address" in interface["ietf-ip:ipv4"]: ipaddr = interface["ietf-ip:ipv4"]["address"][0]["ip"]
                    else: ipaddr = "NA"
                if "description" in interface: description = interface["description"]
                else: description = "NA"

                #Writing to CSV file
                writer.writerow({'host_ipaddr': router_ipaddr, 'if_name': interface["name"], 'description': description, 'enabled': interface["enabled"], 'if_ipaddr':ipaddr})
                #Writing to PrettyTable
                interfaces_table.add_row([interface["name"], description, interface["enabled"],ipaddr])

        
        print(interfaces_table)

