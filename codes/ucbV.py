'''
Created on May 10, 2016

@author: Subhojyoti
'''

import math
import random
import numpy

class ucbV(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    #UpperBound Definition
    def upperBound(self, step, numPlays,payoffSums,sqpayoffSums):

        vj=1.0/numPlays*((payoffSums - (payoffSums/numPlays))*(payoffSums - (payoffSums/numPlays)))
        return (math.sqrt((2*vj*math.log(step+1))/numPlays)+math.log(step+1)/numPlays)
    
     
    #Calculate rewards
    def rewards(self,choice):
        #Gaussain Reward
        #return random.gauss(self.means[choice],1)
        #Bernoulli Reward(1 sample from Binomial Distribution)
        return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        
    def ucbV(self,numActions):
    
        #Set the environment
        self.numActions=numActions
        
        self.payoffSums = [0] * self.numActions
        self.sqpayoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [0] * self.numActions
        self.upbs = [0] * self.numActions
        #self.numRounds = 3000000
        self.numRounds = 60000
        #numRounds = 250000
        
        self.arm_reward = [0]*numActions

        self.bestAction=self.numActions-2
        

        self.means =[0.07 for i in range(self.numActions)]
        
        '''
        i=(1*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.05
            i=i+1
        
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.03
            i=i+1
        '''
        
        self.means[self.bestAction]=0.1
        
        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]

        # initialize empirical sums pull each arm once
        
        t=1
       
        for i in range(self.numActions):
            theReward = self.rewards(i)
            self.payoffSums[i] += theReward
            self.sqpayoffSums[i] += abs( theReward*theReward)
            self.numPlays[i]=self.numPlays[i]+1
                
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if i == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            t=t+1

        
        
            

        while True:

            ucbs = [ (self.payoffSums[i] / self.numPlays[i]) +self.upperBound(t, self.numPlays[i],self.payoffSums[i],self.sqpayoffSums[i]) for i in range(self.numActions)]

            #getting the maximum of the ucbs
            max1=-99999.0
            for p in range(self.numActions):
                if ucbs[p]>max1:
                    max1=ucbs[p]
                    action=p

            #pulling the arm
            theReward = self.rewards(action)
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            self.sqpayoffSums[i] += abs(theReward*theReward)

            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            if t%10000==0:
                print t
            
            if t>=self.numRounds:
                break
            
            
            
            t = t + 1
            
    
        action=max(range(self.numActions), key=lambda i: self.arm_reward[i])

        
        #Print output file for regret for each timestep
        f = open('expt/testRegretUCBV01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()

        return cumulativeReward,bestActionCumulativeReward,regret,action,t
        

if __name__ == "__main__":
    
    wrong=0
    arms=20
    while arms<=20:
        turn=0
        for turn in range(0,100):

            #set the random seed, same for all environment
            random.seed(arms+turn)

            obj=ucbV()
            cumulativeReward,bestActionCumulativeReward,regret,bestArm,timestep=obj.ucbV(arms)
            if bestArm!=arms-2:
                wrong=wrong+1
            print "turn: "+str(turn)+"\twrong: "+str(wrong)+"\tarms: "+str(arms)+"\tbarm: "+str(bestArm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)

            #Print final output file for cumulative regret
            f = open('expt/testUCBV01.txt', 'a')
            f.writelines("arms: %d\tbArm: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (arms, bestArm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        arms=arms+1
        