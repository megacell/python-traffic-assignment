__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
This module processes the *_trips.txt from Bar-Gera 
that can be found here: http://www.bgu.ac.il/~bargera/tntp/
'''

import csv


def process_trips(input, output):
    origin = -1
    out = ['O,D,Ton\n']
    with open(input, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            #before, keyword, after = row.partition('Origin')
            if len(row)>0: 
                l = row[0].split()
                if l[0] == 'Origin':
                    origin = l[1]
                elif origin != -1:
                    for i,e in enumerate(l):
                        if i%3 == 0:
                            out.append('{},{},'.format(origin,e))
                        if i%3 == 2:
                            out.append('{}\n'.format(e[:-1]))
    with open(output, "w") as text_file:
        text_file.write(''.join(out))


def main():
    process_trips('data/SiouxFalls_trips.txt', 'data/SiouxFalls_od.csv')


if __name__ == '__main__':
    main()