

n1 = 10
n2 = 0
n3 = 0
n4 = 0
mask_orig = 18
mask = 2**(32-mask_orig)
result = []

while mask > 0:
    result.append(str(n1) + '.' + str(n2) + '.' + str(n3) + '.' + str(n4) + '/20')
    mask1 = 2**12
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
    mask = mask - 2**12
print(' '.join(result))