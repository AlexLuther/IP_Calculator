
n1 = ""
n2 = ""
n3 = ""
n4 = ""
mask_orig = ""
result = []
ip_numbers = []
#ip_numbers = input("Input the IP:").split()

ip_numbers = "10.0.0.0/18 20.0.0.0/20 30.0.0.0/21 40.0.0.0/21"
ip_numbers = ip_numbers.split()

all_netmasks = []

for i in ip_numbers:
    netmask = []
    netmask = i.split("/")

    netmask = netmask[1::]
    netmask = int(netmask[0])
    all_netmasks.append(2 ** (32 - netmask))

#intro[intro.find('I'):]

over_twenty = []
under_twenty = []
x = 0
sum_of_netmask = []
for i in all_netmasks:
    if i >= 4096:
        over_twenty.append(ip_numbers[x])
    else:
        sum_of_netmask.append(i)

        under_twenty.append(ip_numbers[x])

    x = x + 1

print(sum_of_netmask)
for i in under_twenty:
    result.append(i)


for i in over_twenty:

    splitted_net = []
    splitted_individual_ip = []


    splitted_net = i.split("/")



    mask_orig = splitted_net[1]
    splitted_individual_ip = splitted_net[0].split(".")

    n1 = splitted_individual_ip[0]
    n2 = splitted_individual_ip[1]
    n3 = splitted_individual_ip[2]
    n4 = splitted_individual_ip[3]

    n1 = int(n1)
    n2 = int(n2)
    n3 = int(n3)
    n4 = int(n4)
    mask_orig = int(mask_orig)

    mask = 2 ** (32 - mask_orig)



    while mask > 0:
        result.append(str(n1) + '.' + str(n2) + '.' + str(n3) + '.' + str(n4) + '/20')
        mask1 = 2 ** 12
        while mask1 > 0:
            n4 = n4 + 256
            if n4 >= 256:
                n4 = n4 - 256
                n3 = n3 + 1
                if n3 >= 256:
                    n3 = n3 - 256
                    n2 = n2 + 1
                    if n2 >= 256:
                        n2 = n2 - 256
                        n1 = n1 + 1
            mask1 = mask1 - 256
        mask = mask - 2 ** 12

for i, item in enumerate(result):
    print("Part", i, item)

#print(', '.join(result))
