'''
Created on Jan 2, 2017

@author: Subhojyoti
'''

import math
import random
import numpy
from sets import Set

class ClusUCB(object):
    '''
    classdocs
    '''

    min1=-9999999

    def __init__(self):
        '''
        Constructor
        '''



    #Calculate rewards
    def rewards(self,choice, timesteps):
        #Gaussain Reward
        return random.gauss(self.means[choice],1)
        #Bernoulli Reward(1 sample from Binomial Distribution)
        #return sum(numpy.random.binomial(1,self.means[choice],1))/1.0

    #Count the number of remaining arms
    def remArms(self):
        count=0
        for i in range(self.numActions):
            if self.B[i]!=-1:
                count=count+1
        return count

    
    #Count the number of remaining Sets
    def remSets(self):
        count=0
        for i in range(len(self.sets)):
            if bool(self.sets[i])==True:
                count=count+1
                arm=i
        return count

    def exp_func(self):
        
        #self.func=1.0
        self.func=math.log(self.horizon)
        #self.func=self.numActions*self.numActions*self.horizon
        #self.func=self.horizon / math.log(self.horizon*self.numActions)
        return self.func

    #Initialize Clusters
    def setInit(self):
        self.sets=[]
        for i in range(self.numActions):
            #if self.B[i]!=-1:
                self.sets.append(Set())

        for i in range(self.numActions):
            if self.B[i]!=-1:
                #print i
                self.sets[i].add(i)
            else:
                if bool(self.sets[i]==True):
                    self.sets[i].remove(i)

        #print "Init:" +str(self.sets)


    #Create equal sized Clusters
    def setCreation(self):

        self.setInit()

        #print "rangeTake: "+ str(self.rangetake)
        
        '''
        uni=[]
        count=0
        while True:
            num=numpy.random.randint(0,self.numActions)
            if num not in uni:
                uni.append(num)
                count=count+1
                if count>=self.numActions:
                    break
        
        print "uni:"+str(uni)   
        for count in range(0,self.numActions):
                self.sets[count].remove(count)
                self.sets[count].add(uni[count])
        '''
        for i in range(self.numActions):
            for j in range(i+1,self.numActions):

                #if len(self.sets[j])!=0 and  len(self.sets[i])+len(self.sets[j]) <= self.setSizeLimit:
                if abs(self.avgPayOffSums[i]-self.avgPayOffSums[j]) <= self.rangetake and len(self.sets[j])!=0 and  len(self.sets[i])+len(self.sets[j]) <= self.setSizeLimit:
                    
                    self.sets[i]=self.sets[j]|self.sets[i]
                    #print self.sets[i],self.sets[j]
                    self.sets[j].clear()
                    
                #i=i+2
        #self.calculate_setMaxPay()
        #self.calculate_setMinPay()
        #print self.sets

    #Eliminate Clusters
    def SetElimination(self):
        

        if self.remSets()>1:
            take=-1
            max1=self.min1

            for i in range(self.numActions):
                
                if self.B[i]!=-1:
                    if self.avgPayOffSums[i] > max1:
                        max1=self.avgPayOffSums[i]
                        take=i


                        

            for k in range(len(self.sets)):

                if len(self.sets[k])>=1:
                    
                    max1=self.min1
                    maxSetArm=-1
                    
                    for d in self.sets[k]:
                        if self.B[d]!=-1:
                            if self.avgPayOffSums[d] > max1:
                                max1=self.avgPayOffSums[d]
                                maxSetArm=d


                    #self.func=1.0
                    #self.func=math.log(self.horizon)
                    #self.func=self.numActions*self.numActions*self.horizon
                    #self.func=self.horizon / math.log(self.horizon*self.numActions)
                    #c=math.sqrt((self.rho_s * math.log(self.exp_func() *self.horizon*self.rangetake*self.rangetake))/(2*(self.nm)))
                    
                    c1=math.sqrt((self.rho_s * math.log(self.exp_func() *self.horizon*self.rangetake*self.rangetake))/(2*(self.numPlays[maxSetArm])))
                    c_max=math.sqrt((self.rho_s * math.log(self.exp_func() *self.horizon*self.rangetake*self.rangetake))/(2*(self.numPlays[take])))
                    

                    if (self.avgPayOffSums[maxSetArm] + c1 < self.avgPayOffSums[take]-c_max and take!=maxSetArm):

                        print "Remove Set:"+ str(k), str(len(self.sets[k]))

                        for arms in self.sets[k]:
                            self.B[arms]=-1


                        self.sets[k].clear()

    #Arm Elimination within each cluster
    def ArmElimination(self):

            
        for i in range(len(self.sets)):

            if len(self.sets[i])>1:

                max1=self.min1
                take=-1

                for g in self.sets[i]:
                    if max1<self.avgPayOffSums[g] and self.B[g]!=-1:
                        max1=self.avgPayOffSums[g]
                        take=g

                #self.func=1.0
                #self.func=math.log(self.horizon)
                #self.func=self.numActions*self.numActions*self.horizon
                #self.func=self.horizon / math.log(self.horizon*self.numActions)
                
                #c=math.sqrt((self.rho_a * math.log(self.exp_func() *self.horizon*self.rangetake*self.rangetake))/(2*self.nm))
                
                c1=math.sqrt((self.rho_a * math.log(self.exp_func() *self.horizon*self.rangetake*self.rangetake))/(2*self.numPlays[i]))
                c_max=math.sqrt((self.rho_a * math.log(self.exp_func() *self.horizon*self.rangetake*self.rangetake))/(2*self.numPlays[take]))


                l_copy=Set(self.sets[i])
                    
                for b in self.sets[i]:

                    if (self.avgPayOffSums[b] + c1 < self.avgPayOffSums[take] - c_max) and b!=take:
                    #if self.avgPayOffSums[b] + c*math.sqrt(self.weight*1.0/self.rangetake) < self.avgPayOffSums[take1] - c*math.sqrt(self.weight*1.0/self.rangetake):
                        
                        self.B[b]=-1

                        l_copy.remove(b)
                            
                            


                        print "Remove Arm:"+ str(b)


                self.sets[i].clear()
                self.sets[i]=l_copy


    #Calculate number of pulls each round
    def calculate_pulls(self):


        #self.func=math.log(self.horizon)
        #self.func=self.horizon / math.log(self.horizon*self.numActions)
        self.nm= int(math.ceil((2*math.log(self.exp_func() *self.horizon*self.rangetake*self.rangetake))/(self.rangetake)))
        self.T = self.timestep + (self.remArms() * self.nm )
                
        print "nm: "+str(self.nm), "T: "+str(self.T)
        #return self.nm


    '''
    Running the Adaptive Clustered UCB
    '''

    def clusUCB(self,arms,p,turn,wrong):

        '''
        Set Environment
        '''
        self.numActions = arms

        self.horizon=1000000
        #self.horizon=100000 + self.numActions*self.numActions*1000



        self.rangetake=1.0
        self.bestAction=self.numActions-2



        self.numRounds = math.floor(0.5*math.log10(self.horizon/math.e)/math.log10(2))
        #self.numRounds = math.floor(0.5*math.log10(self.horizon)/math.log10(2))

        print "\n\nnumrounds:"+str(self.numRounds)

        self.means =[0.05 for i in range(self.numActions)]


        '''
        for i in range(0,1*self.numActions/3):
            self.means[i]=0.01
        '''
        '''
        for i in range(self.numActions/3):
            self.means[i]=0.47

        '''
        '''
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.46
            i=i+1
        '''
        '''
        for i in range(self.numActions/3):
            self.means[i]=0.01
        '''
        '''
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.05
            i=i+1
        '''

        self.means[self.bestAction]=0.1

        print self.means

        self.B=[0 for i in range(self.numActions)]
        self.timestep=0

        self.nm=1.0
        self.m=0.0
        self.rho_s=0.5
        self.rho_a=0.5
        self.alpha=self.numRounds
        self.p=p
        self.ucbs=[0.0 for i in range(self.numActions)]

        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.avgPayOffSums = [0] * self.numActions


        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0
        self.regret = 0
        self.regretBounds = 0

        self.arm_reward = [0]*self.numActions
        #self.setSizeLimit=math.ceil((self.numActions*1.0)/self.p)
        self.setSizeLimit = 2
        print "sizeLimit: "+str(self.setSizeLimit)
        #self.func=math.log(self.horizon)
        #self.func=1.0
        #self.func=self.numRounds / math.log(self.horizon*self.numActions)

        self.actionRegret=[]



        #Group Arms
        #self.setCreation()
        
        #Pull each arm once
        for i in range(self.numActions):
            theReward = self.rewards(i, self.timestep)

            self.arm_reward[i]=self.arm_reward[i]+theReward
            self.numPlays[i] += 1
            self.payoffSums[i] += theReward
            self.avgPayOffSums[i] = self.payoffSums[i] / self.numPlays[i]

            self.cumulativeReward += theReward
            self.bestActionCumulativeReward += theReward if i == self.bestAction else self.rewards(self.bestAction, self.timestep)
            self.regret = self.bestActionCumulativeReward - self.cumulativeReward
                                
            self.actionRegret.append(self.regret)

            self.timestep=self.timestep+1
            
            
        
        self.calculate_pulls()
        #self.setInit()
        
        while True:

            for i in range(self.numActions):
                if self.B[i]!=-1:
                    #c=math.sqrt((self.rho_s * math.log(self.exp_func() *self.horizon*self.rangetake*self.rangetake))/(2*(self.numPlays[i])))
                    #self.alpha=self.numRounds/self.numPlays[i]
                    c=math.sqrt((self.rho_s * math.log(self.exp_func() *self.horizon*self.rangetake*self.rangetake))/(2*(self.numPlays[i])))
                    self.ucbs[i]=self.avgPayOffSums[i] + c
                
            #arm = max(range(self.numActions), key=lambda j: self.ucbs[j])
            take=self.min1
            arm=-1
            for i in range(self.numActions):
                if take < self.ucbs[i] and self.B[i]!=-1:
                    take = self.ucbs[i]
                    arm=i
            
            
            theReward = self.rewards(arm, self.timestep)

            self.arm_reward[arm]=self.arm_reward[arm]+theReward
            self.numPlays[arm] += 1
            self.payoffSums[arm] += theReward
            self.avgPayOffSums[arm] = self.payoffSums[arm] / self.numPlays[arm]
    
            self.cumulativeReward += theReward
            self.bestActionCumulativeReward += theReward if arm == self.bestAction else self.rewards(self.bestAction, self.timestep)
            self.regret = self.bestActionCumulativeReward - self.cumulativeReward
                                    
            self.actionRegret.append(self.regret)
    
            self.timestep=self.timestep+1
            
            if self.timestep%100000==0:
                print self.timestep
            
            if self.remArms()>1:
                self.setCreation()
            self.ArmElimination()
            self.SetElimination()


            if self.timestep>=self.horizon:
                break   
             
            if self.timestep >= self.T and self.m <= self.numRounds:
                   
                print "\n\nRound: "+str(self.m)
                print "AvgPayOffsums: " + str(self.avgPayOffSums)
                print "Final sets: "+str(self.sets)
                
                print "B: "+str(self.B)
                print "numPlays: " +str(self.numPlays)
                print "epsilon: "+str(self.rangetake)



                #self.ArmElimination()
                #self.SetElimination()

                #update parameters
                
                self.rangetake=self.rangetake/2
                self.setSizeLimit = 2*self.setSizeLimit
                self.m = self.m + 1

                self.calculate_pulls()
                
        '''
        #Print output file for regret for each timestep
        f = open('expt2/testRegretaclUCB02.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()
        '''
                
        print "\n\nEnd Horizon: "+str(self.timestep)
        print "AvgPayOffsums: " + str(self.avgPayOffSums)
        print "Final sets: "+str(self.sets)
                
        print "B: "+str(self.B)
        print "numPlays: " +str(self.numPlays)        
        
        return self.cumulativeReward,self.bestActionCumulativeReward,self.regret,arm,self.timestep


if __name__ == "__main__":


    wrong=0

    arms=100
    while arms<=100:

        for turn in range(1,3):

            #set the random seed, same for all environment
            numpy.random.seed(arms+turn)

            #Make p=1 for ClusUCB-AE
            p=5

            ucb= ClusUCB()
            cumulativeReward,bestActionCumulativeReward,regret,bestArm,timestep=ucb.clusUCB(arms,p,turn,wrong)
            if bestArm!=arms-2:
                wrong=wrong+1

            print "turn: "+str(turn+1)+"\twrong: "+str(wrong)+"\tarms: "+str(arms)+"\tbarm: "+str(bestArm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)


            #Print final output file for cumulative regret
            f = open('expt2/aclUCB01.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (arms, bestArm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()

        arms=arms+1

        print "total wrong: "+str(wrong)

