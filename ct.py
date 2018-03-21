from numpy import *
from matplotlib import pyplot as plt
from math import sqrt
import matplotlib
import time


def drawDat(Dat):
    fig=plt.figure(figsize=(20,10))
    ax=fig.add_subplot(111)
    ax.scatter(Dat[:,0].flatten().A[0],Dat[:,1].flatten().A[0],s=20,c='red')
    plt.xlim(0,len(Dat))
    plt.ylim(0,35)
    plt.show()

def Score(rV,Rh,predic,result):
    N=len(predic)
    sq1=sqrt(sum([(result[i]-predic[i])**2 for i in predic.iterkeys()])/N)
    sq2=sqrt(sum((predic[i])**2 for i in predic.iterkeys())/N)
    sq3=sqrt(sum((result[i])**2 for i in result.iterkeys())/N)
    return (1-sq1/(sq2+sq3))*(float(sum(rV))/float(sum(Rh)))*100

class f2d():
    def __init__(self,filepath):

        self.pool=[] # sampleI shape like datas
        self.sampleI=[0,
                      0,0,0,0,0, # Counts of flavor0 ~ flavor15
                      0,0,0,0,0,
                      0,0,0,0]
        self.legi={"flavor1":1,"flavor2":2,"flavor3":3,"flavor4":4,"flavor5":5,"flavor6":6,"flavor7":7,
                   "flavor8":8,"flavor9":9,"flavor10":10,"flavor11":11,"flavor12":12,"flavor13":13,
                   "flavor14":14,"flavor15":15}
        with open(filepath, 'r') as f:
            lines = f.readlines()

        self.stime=self.date2read(lines[0].strip().split('\t')[2])

        for line in lines:
            self.mkpool(line)

    def time2read(self,dt):
        dt = dt.split('\t')[0]
        return time.mktime(time.strptime(dt,'%Y-%m-%d %H:%M:%S'))

    def timeMh(self,d1,d2):
        #return int((d1-d2)/604800) #a week
        return int((d1-d2)/7200) #a hour
        #return int((d1-d2)/86400) #a day

    def mkpool(self,raw):
        flavor,tm=raw.strip().split("\t")[1:]
        TM=self.time2read(tm)
        if flavor in self.legi:
            hourTM=self.timeMh(TM,self.stime)
            #pint hourTM
            while hourTM - len(self.pool) >= 0:
                sample = self.sampleI[:]
                self.pool.append(sample)
            self.pool[hourTM][self.legi[flavor]]+=1

    def appendDat(self,filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()

        for line in lines:
            self.mkpool(line)


if __name__ == "__main__":
    trainSet=f2d("example/TrainData_2015.1.1_2015.2.19.txt")
    trainMat=mat(trainSet.pool)
    fig=plt.figure(figsize=(20,10))
    plt.plot(trainMat[:,1:])
    trainSet.appendDat("example/TestData_2015.2.20_2015.2.27.txt")
    testMat=mat(trainSet.pool)
    fig=plt.figure(figsize=(20,10))
    plt.plot(testMat[:,1:])
    plt.show()
    a = raw_input()
