'''
Created on Dec 21, 2016

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
        #return random.gauss(self.means[choice],1)
        #Bernoulli Reward(1 sample from Binomial Distribution)
        return sum(numpy.random.binomial(1,self.means[choice],1))/1.0

    #Count the number of remaining arms
    def remArms(self):
        count=0
        arm=-1
        for i in range(self.numActions):
            if self.B[i]!=-1:
                count=count+1
                arm=i
        return count

    def ArmElimination(self):

        max1=self.min1
        for i in range(self.numActions):
            
            if max1<self.avgPayOffSums[i]:
                max1=self.avgPayOffSums[i]
                take=i
            
        
        c=math.sqrt(( math.log(self.horizon*self.rangetake*self.rangetake))/(2*self.nm))

        for i in range(self.numActions):

            if (self.avgPayOffSums[i] + c < self.avgPayOffSums[take] - c) and i!=take:
            #if self.avgPayOffSums[b] + c*math.sqrt(self.weight*1.0/self.rangetake) < self.avgPayOffSums[take1] - c*math.sqrt(self.weight*1.0/self.rangetake):
                        
                self.B[i]=-1
                #print "Remove Arm:"+ str(i)


                
    #Calculate number of pulls each round
    def calculate_pulls(self):


        #self.func=math.log(self.horizon)
        #self.func=self.horizon / math.log(self.horizon*self.numActions)
        self.nm=int(math.ceil((2*math.log(self.horizon*self.rangetake*self.rangetake))/(self.rangetake*self.rangetake)))
        self.T=self.timestep + self.nm*self.remArms()
                
        print "nm:"+str(self.nm)
        return self.nm


    '''
    Running the Clustered UCB
    '''

    def clusUCB(self,arms,p,turn,wrong):

        '''
        Set Environment
        '''
        self.numActions = arms

        self.horizon=60000
        #self.horizon=100000 + self.numActions*self.numActions*1000



        self.rangetake=1.0
        self.bestAction=self.numActions-2



        self.numRounds = math.floor(0.5*math.log10(self.horizon/math.e)/math.log10(2))
        #self.numRounds = math.floor(0.5*math.log10(self.horizon)/math.log10(2))

        print "\n\nnumrounds:"+str(self.numRounds)

        self.means =[0.07 for i in range(self.numActions)]


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
        self.ucbs=[0.0 for i in range(self.numActions)]

        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.avgPayOffSums = [0] * self.numActions
        self.variance = [0] * self.numActions

        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0
        self.regret = 0
        self.regretBounds = 0

        self.arm_reward = [0]*self.numActions
        
        #self.func=math.log(self.horizon)
        #self.func=1.0
        #self.func=self.numRounds / math.log(self.horizon*self.numActions)

        self.actionRegret=[]
        
        
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
        
        while True:

            for i in range(self.numActions):
                self.func=math.sqrt(self.horizon)/self.numPlays[i]
                c=math.sqrt((math.log(self.horizon*self.rangetake*self.rangetake) * self.func)/(2*(self.nm)))
                self.ucbs[i]=self.avgPayOffSums[i] + c
                
            #arm = max(range(self.numActions), key=lambda j: self.ucbs[j])
            take=self.min1
            arm=-1
            for i in range(self.numActions):
                if take < self.ucbs[i]:
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
            
            self.ArmElimination()
            
            if self.timestep>=self.horizon:
                break   
             
            if self.timestep >= self.T and self.m <= self.numRounds:
                   
                print "\n\nRound: "+str(self.m)
                print "AvgPayOffsums: " + str(self.avgPayOffSums)
                
                print "B: "+str(self.B)
                print "numPlays: " +str(self.numPlays)
                
                #update parameters
                
                self.rangetake=self.rangetake/2
                self.m = self.m + 1

                self.calculate_pulls()
                
        
        #Print output file for regret for each timestep
        f = open('expt/testRegretCCB01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()
        
        return self.cumulativeReward,self.bestActionCumulativeReward,self.regret,arm,self.timestep


if __name__ == "__main__":


    wrong=0

    arms=20
    while arms<=20:

        for turn in range(1,100):

            #set the random seed, same for all environment
            numpy.random.seed(arms+turn)

            
            

            ucb= ClusUCB()
            cumulativeReward,bestActionCumulativeReward,regret,bestArm,timestep=ucb.clusUCB(arms,5,turn,wrong)
            if bestArm!=arms-2:
                wrong=wrong+1

            print "turn: "+str(turn+1)+"\twrong: "+str(wrong)+"\tarms: "+str(arms)+"\tbarm: "+str(bestArm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)


            #Print final output file for cumulative regret
            f = open('expt/CCB01.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (arms, bestArm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()

        arms=arms+1

        print "total wrong: "+str(wrong)

