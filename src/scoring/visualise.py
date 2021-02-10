import json

res = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/SVM_res.json', 'r'))
true = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/Y_test.json', 'r'))
points = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/pos.json', 'r'))

green = []
white= []
red = []
yellow = []

for i in range(len(points)):
    if true[i] == res[i]:
        if true[i] == 1:
            green.append(points[i])
        else:
            white.append(points[i])
    elif true[i] != res[i]:
        if true[i] == 0:
            red.append(points[i])


g = open('green.xyz', 'w')
for c in green:
    g.write(f'Mg {c[0]} {c[1]} {c[2]}\n')

g = open('red.xyz', 'w')
for c in red:
    g.write(f'Mg {c[0]} {c[1]} {c[2]}\n')

g = open('yellow.xyz', 'w')
for c in yellow:
    g.write(f'Mg {c[0]} {c[1]} {c[2]}\n')
