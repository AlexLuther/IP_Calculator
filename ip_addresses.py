import ipaddress
import binpacking
import tkinter as tk

root = tk.Tk()

# Creates a canvas specific size and title
root.geometry("405x175")
root.title("IP Calculator")

# Creates the first line of text
label1 = tk.Label(root, text="Input assets to INCLUDE separated by space/s:")
label1.config(font=('helvetica', 14))
label1.place(height=40, width=400, x=0, y=0)

# Creates the first input box for included addresses
e = tk.Entry(root, width=100)
e.place(height=20, width=400, x=0, y=41)

# Creates the second line of text under the first input box
label1 = tk.Label(root, text="Input assets to EXCLUDE separated by space/s:")
label1.config(font=('helvetica', 14))
label1.place(height=40, width=400, x=0, y=62)

# Creates the second input box for excluded addresses
e1 = tk.Entry(root, width=100)
e1.place(height=20, width=400, x=0, y=105)

ip_numbers = []  # List for included assets
exclude = []  # List for excluded assets


# Submit button takes the inputs and closes the program
def submit():
    global ip_numbers
    global exclude

    # If no input and Submitted exit the program
    if not e.get() and not e1.get():
        exit()
    # Else if no assets to include are inputted exit the program
    elif not e.get():
        exit()

    ip_numbers = e.get()
    exclude = e1.get()

    root.destroy()


# The submit button
myButton = tk.Button(root, text="Submit", command=submit)
myButton.place(height=30, width=70, x=170, y=130)

root.mainloop()

# Close program
try:
    ip_numbers = ip_numbers.split()
except AttributeError:
    exit()

exclude = exclude.split()  # Split excluded IPs into a list
ip_converted = []  # Converted included IPs
ex_ip_converted = []  # Convert excluded IPs
prefix_length = []  # Prefix length

# Declare j out of both loops to start at 0
j = 0

# Loop excluded addresses to place them in IP format
for i in exclude:

    try:
        i = ipaddress.ip_network(i, False)  # Converts IP address to string

    # Pop-up explaining the error encountered
    except ValueError:
        root = tk.Tk()
        root.title("Error")
        root.geometry("405x35")
        label1 = tk.Label(root, text="Incorrect value inputted in assets to EXCLUDE")
        label1.config(font=('helvetica', 14))
        label1.pack()
        root.mainloop()
        exit()

    if "/32" in str(i):  # Replaces "/32" with blank
        ex_ip_converted.append(str(i).replace("/32", ""))
    else:  # Adds IPs to excluded list
        ex_ip_converted.append(str(i))

# Loop over each item in input
for i in ip_numbers:

    # Convert element into IP, if incorrect i.e. 10.0.0.1/20 converts to 10.0.0.0/20
    try:
        i = ipaddress.ip_network(i, False)

    # Pop-up explaining the error encountered
    except ValueError:
        root = tk.Tk()
        root.title("Error")
        root.geometry("405x35")
        label1 = tk.Label(root, text="Incorrect value inputted in assets to INCLUDE")
        label1.config(font=('helvetica', 14))
        label1.pack()
        root.mainloop()
        exit()

    # Gets number of IPs and add to list
    prefix_length.append(i.num_addresses)

    # If mask bits are above or equal to /20 convert to /20
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

    elif "/32" in str(i):  # Replaces "/32" with blank
        ip_converted.append(str(i).replace("/32", ""))
    else:
        ip_converted.append(str(i))


    j += 1

ip_set = {}  # Dictionary for binpacking
num = 0
# Creating the dictionary
for i in prefix_length:
    ip_set[ip_converted[num]] = int(i)
    num += 1

groups = binpacking.to_constant_volume(ip_set, 4096)

resourcesPerGroups = [list(group.keys()) for group in groups]

# Numerate part starting from 1
b = 1

# Open the text file to write to
file1 = open("ips.txt", "w")

for i in resourcesPerGroups:
    excluded_ips = []

    # Join IPs to exclude separated by comma
    ips_ex = ', '.join(i)
    ips_ex = ips_ex.split(", ")

    L = "Part " + str(b) + ": " + ', '.join(i) + "\n"  # Convert to string

    # Loops over all included IPs to check if they match excluded IPs
    for z in ips_ex:
        for zz in ex_ip_converted:
            if ipaddress.ip_interface(zz) in ipaddress.IPv4Network(z):
                excluded_ips.append(zz)

    file1.writelines(L)  # Write to file Part # and assets in it

    # Write to file assets to exclude
    if excluded_ips:
        L = "Exclude IP/s: " + ', '.join(excluded_ips) + '\n' + '\n'
        file1.writelines(L)

    b += 1
file1.close()
