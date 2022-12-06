import os,sys
import argparse
import re
class args:
    pass
search=re.compile('\(([0-9\.]+)\)')
search2=re.compile('n\:([0-9]+)')
parser=argparse.ArgumentParser()
parser.add_argument('INPUT',nargs='+')
parser.parse_args(sys.argv[1:],args)
for i in args.INPUT:
    f = open(i,'r')
    dbmin = 999
    dbtot = 0
    frtot = 0
    minfr = 0
    for line in f:
        if '(inf)' in line:
            continue
        res=search.search(line)
        if res==None:
            continue
        db = float(res.group(1))
        #print(db)
        dbtot += db
        frtot += 1
        if db<dbmin:
            dbmin=db
            minfr=int(search2.search(line).group(1))
    print('%s\navg: %f\nsmallest: %f\nin frame: %d\n' % (i,dbtot/frtot,dbmin,minfr))
input('enter to exit')
