a = ['*', 'd', 'c', '*', 'e', '*', 'a', '*']*3
i = 0
j = len(a) - 1
print(j)
while i < j:
    if a[i] == '*':
        i += 1
    else:
        if a[j] == '*':
            print((a[i], a[j]))
            a[i], a[j] = a[j], a[i]
            i += 1
            j -= 1
        else:
            print((a[i], a[j]))
            a[i], a[j] = a[j], a[i]
            j -= 1
            print((a[i], a[j]))
            a[i], a[j] = a[j], a[i]
print(a)
j = len(a) - 1
while i < j:
    print((a[i], a[j]))
    a[i], a[j] = a[j], a[i]
    i += 1
    j -= 1

print(a)
