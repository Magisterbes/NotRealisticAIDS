import numpy as np
import IOPart as io
import Helper as hp

class Soc:

    def __init__(self,size):
        self.Soc = {}
        self.Pairs = {}
        self.Dead = []
        self.now = 0
        self.size = size
        self.Infected ={}

        MCount = np.round(hp.InitAgeDistMan*size,0)
        WCount = np.round(hp.InitAgeDistWoman*size,0)

        for (sex,ar) in enumerate([MCount,WCount]):
            for (age,num) in enumerate(ar):
                for i in range(int(num)):
                    p = Person(sex,-age*52, 0)
                    while p.Position in self.Soc.keys():
                        p.Position = tuple(np.random.random(size=2))
                    self.Soc[p.Position] = p

        pp = list(self.Soc.values())
        np.random.shuffle(pp)

        for p in pp[:10]:
            if p.BirthWeek >- 1000:
                p.BirthWeek = -1000
                p.Death = p.Death-1000

            p.Infect(self.now)
            self.Infected[p.Position] = p


    def IterSoc(self):
        self.now +=1

        pp = list(self.Soc.values())
        for p in pp:  
            self.Diagnose(p)
            self.RemoveDead(p)

        self.RemovePairs()
        self.Pairing()
        self.Birth()
        self.Sex()

    def Sex(self):
        for pair in self.Pairs.values():
            
            if (pair.p1.IsInfected == 0 and pair.p2.IsInfected == 0) \
                or (pair.p1.IsSincere ==0 and pair.p2.IsSincere == 0) \
                or (pair.p1.IsInfected == 1 and pair.p2.IsInfected == 1):
                continue

            freq =round(np.abs(np.random.normal(hp.SexPerWeek,2)))

            pr = hp.ProbPerSexM
            notinf =  pair.p1
            if pair.p1.Sex == 1 and pair.p1.IsInfected ==0:
                pr = hp.ProbPerSexW

            if pair.p2.Sex == 1 and pair.p2.IsInfected ==0:
                pr = hp.ProbPerSexW
                notinf =  pair.p2


            for i in range(int(freq)):
                if np.random.rand()<= pr:
                    notinf.Infect(self.now)
                    self.Infected[notinf.Position] = notinf
    
    def Birth(self):
        for i in range(int(hp.BirthRate*self.size)):

            p = Person(np.random.randint(0,1), self.now, self.now)
            while p.Position in self.Soc.keys():
                p.Position = tuple(np.random.random(size=2))
            self.Soc[p.Position] = p

    def Diagnose(self,p):
        if p.IsInfected ==1 and p.IsDiagnosed == 0 and self.now - p.BirthWeek >= p.DiagnoseAge:
            p.IsDiagnosed = 1
            

    def RemoveDead(self,p):
        if self.now - p.BirthWeek >= p.Death or self.now - p.BirthWeek >= p.NewDeath:
            if p.IsInPair == 1:
                key = tuple(p.PairKey)
                self.ClearPair(self.Pairs[p.PairKey])
                del self.Pairs[key]

            p.IsDead = 1
           # self.Dead.append(p)
            del self.Soc[p.Position]
            if p.IsInfected ==1:
                del self.Infected[p.Position]


    def RemovePairs(self,):
        temp = {}
        for k in self.Pairs.keys():
            if self.Pairs[k].End >=self.now:
                self.ClearPair(self.Pairs[k])
            else:
                temp[k] = self.Pairs[k]
    
    def ClearPair(self,pair):
            
            pair.p1.IsInPair= 0
            pair.p2.IsInPair= 0
            pair.p1.PairKey= ()
            pair.p2.PairKey= ()
            

    def Pairing(self):
        pp = list(self.Soc.values())
        np.random.shuffle(pp)
        ct=0
        for (j,p) in enumerate(pp[:int(len(pp)/4)]):
            if p.GetAge(self.now)<15*52 or p.GetAge(self.now)>60*52 or p.IsDead == 1 or p.IsInPair == 1 or p.IsDiagnosed ==1:
                continue
            ct+=1
            c = self.PairOne(p,pp)
            if c == []:
                continue

            p.IsInPair = 1
            c.IsInPair = 1
            p.PairKey = (c.Position,p.Position)
            c.PairKey = (c.Position,p.Position)
            pair = Pair(p,c,self.now+hp.RelLength(min([p.GetAge(self.now),c.GetAge(self.now)])))
            self.Pairs[(c.Position,p.Position)] = pair
             
            

    def PairOne(self, Person,plist):

        pp = np.random.randint(0, len(self.Soc.values()),size = 200)
        
        for (j,ind) in enumerate(pp):
            p = plist[ind]
            if p.GetAge(self.now)<15*52 or p.GetAge(self.now)>60*52 or p.IsDead == 1 or p.IsInPair == 1 or p.Position == Person.Position or p.IsDiagnosed ==1:
                continue

            if p.Sex == Person.Sex:
                if np.random.rand() >0.07:
                    continue
            pr = (1/(np.linalg.norm(np.array(p.Position)- np.array(Person.Position))*40))*(1/(np.log(np.abs(p.GetAge(self.now)/52-Person.GetAge(self.now)/52)+1)+1))

            if pr > np.random.rand():
                return p
            
        return []

class Pair:

    def __init__(self,p1,p2,End):
        self.p1 = p1
        self.p2 = p2
        self.End = End


class Person:
    def __init__(self,Sex,Birth,Now):

        self.Sex = Sex
        self.BirthWeek = Birth
        self.Position  = tuple(np.random.random(size=2))
        self.Death  = self.InitDeathAge(int(self.GetAge(Now)/52),Sex)*52 +  int(np.random.rand()*52)
        self.NewDeath = 110*52
        self.DiagnoseAge = -1
        self.IsDead = 0
        self.IsInPair = 0
        self.IsInfected = 0
        self.IsDiagnosed = 0
        self.PairKey = ()
        if np.random.rand()< hp.Sincerity:
            self.IsSincere = 1
        else:
            self.IsSincere = 0

    def GetAge(self,now):
        return now - self.BirthWeek

    def InitDeathAge(self, CurrentAge, Sex):
        ag = []
        if Sex == 0:
            ag = hp.MenAging
        else:
            ag = hp.WomenAging

        ag = ag[CurrentAge:]

        for (i,haz) in enumerate(ag):
            if np.random.randint(0,100000)<=haz:
                return CurrentAge + i
        return 0

    def Infect(self, now):
        self.IsInfected =1
        survweek = np.random.normal(hp.LifeTillDeath,5*52)
        self.NewDeath = int(self.GetAge(now) + survweek)
        sojourntime  = np.random.normal(hp.SojournMean,1*52)
        self.DiagnoseAge = int(self.GetAge(now) + sojourntime)