'''
Created on Jul 28, 2015

@author: Subhojyoti
'''

import math
import random
import numpy
#import statistics

class medianElim(object):
    '''
    classdocs
    '''
    
    min1=-9999999
    
    def __init__(self):
        '''
        Constructor
        '''
        #print self.numRounds
        #print self.means
        
    
    #Calculate rewards
    def rewards(self,choice):
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
        
    def medianElimimation(self,arms,epsilon,delta,wrong,turn):

        #Set the environment
        self.numActions = arms
        self.horizon=2000000
        
        self.bestAction=self.numActions-2
        self.means =[0.06 for i in range(self.numActions)]

        for i in range(self.numActions/3):
            self.means[i]=0.01
        '''
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.4
            i=i+1
        '''

        self.means[self.bestAction]=0.1
        

        print "Means: "+str(self.means)

        self.arm_reward = [0]*self.numActions
        
        self.timestep=0
        self.B=[0 for i in range(self.numActions)]
        
        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.avgPayOffSums = [0] * self.numActions
        
        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0
        self.regret = 0
        
        self.arm_reward = [0]*self.numActions

        self.actionRegret=[]

        l=1
        epsilon_l=epsilon*0.25
        delta_l=delta*0.5
        
        while True:
            
            print "\n\nRound: "+str(l)
            self.numRounds = int(math.ceil((1/(epsilon_l*0.5))*math.log(3/delta_l)))
            print "nm: "+str(self.numRounds)

            #Pull all arms equally in the round
            for i in range(self.numActions):
                for j in range(self.numRounds):
                    
                    if self.B[i]!=-1:
                        theReward = self.rewards(i)
                            
                        self.arm_reward[i]=self.arm_reward[i]+theReward
                        self.numPlays[i] += 1
                        self.payoffSums[i] += theReward
                        self.avgPayOffSums[i] = self.payoffSums[i] / self.numPlays[i]
                            
                        self.cumulativeReward += theReward
                        self.bestActionCumulativeReward += theReward if i == self.bestAction else self.rewards(self.bestAction)
                        self.regret = self.bestActionCumulativeReward - self.cumulativeReward

                        self.actionRegret.append(self.regret)

                        self.timestep=self.timestep+1

            #Calculate the median of the remaining arms
            self.avgPayOffSums1=[]
            for i in range(self.numActions):
                if self.B[i]!=-1:
                    self.avgPayOffSums1.append(self.avgPayOffSums[i])
            median_val=numpy.median(sorted(self.avgPayOffSums1))
            
            
            print "AvgPayoff: "+str(self.avgPayOffSums)
            print "Median: "+str(median_val)

            #Eliminate arms below median
            for i in range(self.numActions):
                if self.B[i]!=-1:
                    if self.avgPayOffSums[i]<median_val:
                        self.B[i]=-1
            
            print "B: "+str(self.B)
            print "Rem arms: "+str(self.remArms())
            
            #update parameters
            epsilon_l=0.75*epsilon_l
            delta_l=0.5*delta_l
            l=l+1
                 
            count=self.remArms()
            if count<=1 or self.timestep>=self.horizon:
                break
            
        for i in range(self.numActions):
            if self.B[i]!=-1:
                bestArm=i

        arm=bestArm

        print "last arm:"+str(arm) + " turn:"+str(turn) + " wrong:"+str(wrong)

        #if horizon not reached dpull the best Arm outputed till horizon
        while self.timestep<self.horizon:

            theReward = self.rewards(arm)
            self.arm_reward[arm]=self.arm_reward[arm]+theReward
            self.numPlays[arm] += 1
            self.payoffSums[arm] += theReward

            self.avgPayOffSums[arm] = self.payoffSums[arm] / self.numPlays[arm]

            self.cumulativeReward += theReward
            self.bestActionCumulativeReward += theReward if arm == self.bestAction else self.rewards(self.bestAction)
            self.regret = self.bestActionCumulativeReward - self.cumulativeReward
            self.actionRegret.append(self.regret)

            self.timestep=self.timestep+1


        #Print output file for regret for each timestep
        f = open('expt/testRegretMedElim.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()

        return self.cumulativeReward,self.bestActionCumulativeReward,self.regret,bestArm,self.timestep
        
        
if __name__ == "__main__":
    

    
    wrong=0
    arms=100
    while arms<=100:
        
        for turn in range(0,100):

            #set the random seed, same for all environment
            numpy.random.seed(arms+turn)

            me= medianElim()
            eps=0.03
            delta=0.1
            cumulativeReward,bestActionCumulativeReward,regret,bestArm,timestep=me.medianElimimation(arms,eps,delta,wrong,turn)
            if bestArm!=arms-2:
                wrong=wrong+1

            print "turn: "+str(turn)+"\twrong: "+str(wrong)+"\tarms: "+str(arms)+"\tbarm: "+str(bestArm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)

            #Print final output file for cumulative regret
            f = open('expt/testMedElim.txt', 'a')
            f.writelines("arms: %d\tbArm: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (arms, bestArm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
        arms=arms+1
    
    

    
