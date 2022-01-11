# IP_Calculator

Calculator for OpenVAS
Takes input of addresses to include in the first box
Takes input of addresses to exclude in the second box
(Input must be separated by spaces one or multiple)

Features: 
Breaks up CIDR over 4096 i.e. "/20" into hosts under 4096
Converts incorrectly inputted IPs such as 10.0.0.0/32 to 10.0.0.0 and 10.0.0.20/20 into 10.0.0.0/20
Will not include a duplicate address

When you hit "Submit" button a text file will generate in the same location as the program with parts listed
Excluded parts will be under the part to include e.g.

      Part 1: 10.0.0.0/20
      Part 2: 10.0.16.0/20
      Exclude IP/s: IP/s: 10.0.25.0/28

Part 3: 10.0.32.0/20

Use pyinstaller to create into a standalone program.
