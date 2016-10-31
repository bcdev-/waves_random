import requests
start = 180025
found = False
for i in range(start, 186709):
    r = requests.get('http://127.0.0.1:6861/blocks/at/%d' % i)
    j = r.json()
#    print(i, found)
    if len(j['transactions']) > 0:
        for tx in j['transactions']:
#            if (tx['type'] == 3 or tx['type'] == 4) and tx['assetId'] == "F7LSFLL2q9hhfrUfJzZ7rGah5L6mZhHuteLPR49Ze5Lo":
            if (tx['type'] == 3):
                found=True
#                if len(tx['attachment']) > 0:
                print(tx)
#                exit(0)
