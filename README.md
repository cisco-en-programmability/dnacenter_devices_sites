# Cisco DNA Center Devices and Sites

This script will ask the user for input a name for a device or a site.
It will collect the sites and devices inventory and search for:
 - exact match for the device name
   If found it will return the site name and address for the device
 - partial match for the site name
   If found it will return the site name, address and the device inventory for the site

**Cisco Products & Services:**

- Cisco DNA Center
- Cisco Network Devices Managed by Cisco DNA Center

**Tools & Frameworks:**

- Python environment

**Usage**

Here are some samples for the the script run for few different user provided values:

----------

Please enter the name of a network device or partial name of a site (using the format "site name/floor #" with "floor #" optional): NYC

The location with the name "Global/NYC", address: "111 8th Ave, Manhattan, New York, New York 10011, United States",
has these devices: NYC-ACCESS, NYC-RO

----------

----------
Please enter the name of a network device or partial name of a site (using the format "site name/floor #" with "floor #" optional): SJC

The input "SJC", is not a match for any network devices or sites names

----------

----------

Please enter the name of a network device or partial name of a site (using the format "site name/floor #" with "floor #" optional): PDX-RO

The device with the name "PDX-RO" location is: "Global/PDX/Floor 3", address: "5400 Meadows Road, Lake Oswego, Oregon 97035, United States"

----------

This script may be useful as part of integrations with other workflows for device inventory or network troubleshooting.


**License**

This project is licensed to you under the terms of the [Cisco Sample Code License](./LICENSE).
