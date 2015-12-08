#! /bin/env python
from ROOT import *
from array import array
from sys import argv, stderr
from commands import getoutput
if len(argv)>1:
    path=argv[1]
    if path[-1]!='/':
        path+='/'
    basetime=int(getoutput('date -d {0} +%s'.format(path.split('/')[-2])))
else:
    path='./'
    basetime=1438763742
files=getoutput('ls {0}*.log'.format(path)).split('\n')
times=array('d')
bdrts=array('d')
gROOT.SetBatch()
c=TCanvas('c','c',800,800)
for fl in files:
    ctt=open(fl)
    reg=[i for i in ctt if '->' in i]
    badrate=len([i for i in reg if 'ERROR!!' in i])/float(len(reg))*100
    timest=fl.split('/')[-1].split('.log')[0].replace('_',' ')
    hm=getoutput('date -d "{0}" +%s'.format(timest[:-2]))
    time=float(hm)+float(timest[-2:])-basetime
    times.append(time/3600)
    bdrts.append(badrate)
g=TGraph(len(times),times,bdrts)
g.SetTitle('Register ERROR rate vs time;t/h;register error rate/%')
g.SetMarkerColor(2)
#g.SetMarkerStyle(7)
g.SetMaximum(109)
g.SetMinimum(0)
g.Draw('ap')
c.Print('badrate.png')
