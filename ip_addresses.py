import ipaddress
import binpacking
from tkinter import *

#input -  then split into a list
#TODO 20.0.0.6/22
# ip_numbers = "10.0.0.0/21 20.0.0.0/20"

root = Tk()

e = Entry(root, width=50)
e.pack()
e.insert(0, "Input Assets to INCLUDE separated by space/s" )
e1 = Entry(root, width=50)
e1.pack()
e1.insert(0, "Input Assets to EXCLUDE separated by space/s" )

def submit():

    ip_numbers = e.insert()
    exclude = e1.insert()



myButton = Button(root, text="Submit", command = submit)
myButton.pack()

root.mainloop()

# ip_numbers = input("Input Assets to Include separated by space/s:")

try:
    ip_numbers = ip_numbers.split()
except ValueError:
        print("You didn't use SPACE/s to separate the addresses, please try again")


# exclude = input("Input Assets to exclude separated by space/s:")

try:
    exclude = exclude.split()
except ValueError:
        print("You didn't use SPACE/s to separate the addresses, please try again")

#converted IP addresses
ip_converted = []


ex_ip_converted = []

#prefix length
prefix_length = []

#declare j out of both loops to start at 0
j = 0

# Loop excluded addresses to place them in IP format
for i in exclude:
    i = ipaddress.ip_interface(i)
    ex_ip_converted.append(str(i))

#loop over each item in input
for i in ip_numbers:

    #convert element into IP
    i = ipaddress.IPv4Network(i)

    #get IP prefix and add to list
    prefix_length.append(i.num_addresses)

    #if subnet is above or equal to /20 convert to /20
    if prefix_length[j] >= 4096:

        # When prefix over 4096 remove it and replace with smaller prefixes
        del prefix_length[j]
        j -= 1

        # Make new prefix max /20
        for sn in i.subnets(new_prefix=20):

            # Add new subnets instead of the large one
            ip_converted.append(str(sn))

            # Add new prefix length to match with new IP subnet added
            prefix_length.append(sn.num_addresses)
            j += 1

    else:

        # Helps not put
        if "/32" in str(i):
            ip_converted.append(str(i).replace("/32", ""))
        else:
            ip_converted.append(str(i))

    j += 1

ip_set = {}
num = 0
for i in prefix_length:
    ip_set[ip_converted[num]] = int(i)

    num += 1


groups = binpacking.to_constant_volume(ip_set, 4096)



resourcesPerGroups = [list(group.keys()) for group in groups]

# Numerate part starting from 1
b = 1

for i in resourcesPerGroups:
    excluded_ips = []

    ips_ex = ', '.join(i)

    ips_ex = ips_ex.split(", ")

    print("Part", b, ', '.join(i))

    for z in ips_ex:

        for zz in ex_ip_converted:
            if ipaddress.ip_interface(zz) in ipaddress.IPv4Network(z):
                excluded_ips.append(zz)
    if excluded_ips:
        print("Exlude IP/s: ", ', '.join(excluded_ips))


    print('') # new line between parts



    b += 1


