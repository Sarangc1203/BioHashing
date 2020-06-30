import json
from pearhash import PearsonHasher
hasher = PearsonHasher(1)
import numpy

def generate_triplets(inp):
    res = [
        inp[0:1]+inp[1:2]+inp[2:3],
        inp[0:1]+inp[1:2]+inp[3:4],
        inp[0:1]+inp[1:2]+inp[4:5],
        inp[0:1]+inp[2:3]+inp[3:4],
        inp[0:1]+inp[2:3]+inp[4:5],
        inp[0:1]+inp[3:4]+inp[4:5]
    ]
    return res

def get_hamming_distance(inp1, inp2):
    c=0
    for (i,j) in zip(inp1,inp2):
        if i != j:
            c = c + 1
    return c

def main():
    f = open('./myjson.json')
    templates = json.load(f)
    allhashed = {}
    allraw = {}
    alltemplates = []

    for sample in templates:
        template = templates[sample]
        alltemplates.append((sample, template))
    
    alltemplates = sorted(alltemplates)

    for (name,template) in alltemplates:
        print(name)
        template = "".join(str(e) for e in template)
        allraw[name] = template

        b = bytearray()
        i = int(template,2)
        while i:
            b.append(i & 0xff)
            i >>= 8
        b = bytes(b[::-1])

        accm = [0 for i in range(256)]

        for i in range(1200):
            if i+5 <= 1200:
                s = b[i:i+5]
            else:
                s = b[i:1200] + b[0:i+5-1200]
            triplets = generate_triplets(s)
            for tri in triplets:
                val = int(hasher.hash(tri).hexdigest(),16)
                accm[val] = accm[val] + 1

        # print(accm)
        q1 = numpy.quantile(accm, 0.25)
        q2 = numpy.quantile(accm, 0.50)
        q3 = numpy.quantile(accm, 0.75)
        ans = ''
        for i in accm:
            if i <= q1:
                ans = ans + '00'
            elif i <= q2:
                ans = ans + '01'
            elif i <= q3:
                ans = ans + '10'
            else:
                ans = ans + '11'
        # print(ans)
        allhashed[name] = ans
    
    allhds1 = []
    allhds2 = []

    for sample1 in allhashed:
        hds1 = []
        hds2 = []
        for sample2 in allhashed:
            hd1 = get_hamming_distance(allhashed[sample1], allhashed[sample2])
            hd2 = get_hamming_distance(allraw[sample1], allraw[sample2])
            hds1.append(hd1)
            hds2.append(hd2)

        allhds1.append(hds1)
        allhds2.append(hds2)
    
    for hds in allhds1:
        print(hds)

    for hds in (numpy.array(allhds2)>2250):
        print(1*hds)

if __name__=="__main__":
    main()