#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Gabriel Zapodeanu TME, ENB"
__email__ = "gzapodea@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import json

import requests
import urllib3
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings


# Cisco DNA Center info

username = 'Admin'
password = 'Clive.06'
DNAC_URL = 'https://10.93.141.35'


DNAC_AUTH = HTTPBasicAuth(username, password)


def get_dnac_jwt_token(dnac_auth):
    """
    Create the authorization token required to access DNA C
    Call to Cisco DNA Center - /api/system/v1/auth/login
    :param dnac_auth - Cisco DNA Center Basic Auth string
    :return: Cisco DNA Center JWT token
    """
    url = DNAC_URL + '/dna/system/api/v1/auth/token'
    header = {'content-type': 'application/json'}
    response = requests.post(url, auth=dnac_auth, headers=header, verify=False)
    dnac_jwt_token = response.json()['Token']
    return dnac_jwt_token


def get_physical_topology(dnac_jwt_token):
    """
    This function will retrieve the physical topology for all the devices
    :param dnac_jwt_token: Cisco DNA C token
    :return: topology info
    """
    url = DNAC_URL + '/dna/intent/api/v1/topology/physical-topology'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    topology_json = response.json()['response']
    return topology_json


def get_sites_topology(dnac_jwt_token):
    """
    This function will retrieve the physical topology for all the devices
    :param dnac_jwt_token: Cisco DNA C token
    :return: topology info
    """
    url = DNAC_URL + '/dna/intent/api/v1/topology/site-topology'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    sites_topology_json = response.json()['response']
    return sites_topology_json


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """
    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


# noinspection PyUnboundLocalVariable
def main():
    """
    This script will ask the user for input a name for a device or a site.
    It will collect the sites and devices inventory and search for:
     - exact match for the device name
     If found it will return the site name and address for the device
     - partial match for the site name
     If found it will return the site name, address and the device inventory for the site
    """

    # get the Cisco DNA Center Auth
    dnac_auth = get_dnac_jwt_token(DNAC_AUTH)

    # get the physical topology
    topology_info = get_physical_topology(dnac_auth)
    topology_nodes_list = topology_info['nodes']

    # get the site list
    site_info = get_sites_topology(dnac_auth)
    site_info_list = site_info['sites']

    # select all the nodes from the topology_nodes_list that are assigned to sites
    # using the site_id, select the site name and address for each device from the site_info_list

    devices_info_dict = {}  # create the dict with all the devices info
    sites_address_dict = {}  # create the dict with the site name to site address mapping

    for node in topology_nodes_list:
        device_name = node['label']
        # select only the nodes that are assigned to a site, by checking if we have the key 'siteid' in the
        # 'additionalInfo' array
        if 'additionalInfo' in node and 'siteid' in node['additionalInfo']:
            site_id = node['additionalInfo']['siteid']
            for site in site_info_list:
                if site_id == site['id']:
                    site_name = site['groupNameHierarchy']
                    site_address = site['locationAddress']
                    break
            devices_info_dict.update({device_name: site_name})
            # noinspection PyUnboundLocalVariable
            sites_address_dict.update({site_name: site_address})

    # ask the user to enter the name of a network device or a site
    search_value = input('\nPlease enter the name of a network device or partial name of a site '
                         '(using the format "site name/floor #" with "floor #" optional): ')

    # use the search_value to search for device names matches using the device_info_dict keys
    found = False
    dict_keys = dict.keys(devices_info_dict)

    if search_value in dict_keys:
        # match found, collect the site name and address for the device
        device_site_name = devices_info_dict[search_value]
        device_site_address = sites_address_dict[device_site_name]
        print('\nThe device with the name "' + search_value + '" location is: "'
              + device_site_name + '", address: "' + device_site_address + '"')
        found = True

    # use the search_value to search for location names matches, using the device_info_dict values
    device_list = []
    for device, location in dict.items(devices_info_dict):
        if search_value in location:
            device_list.append(device)
            location_address = sites_address_dict[location]
            location_name = location
    if device_list:
        print('\nThe location with the name "' + location_name + '", address: "' + location_address +
              '",\nhas these devices:', (', '.join(device_list)))
        found = True

    if not found:
        print('\nThe input "' + search_value + '", is not a match for any network devices or sites names')


if __name__ == '__main__':
    main()

