'''
Created on Oct 6, 2015

@author: Subhojyoti
'''

import math
import random
import numpy

class ucb1(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    #UpperBound Definition
    def upperBound(self, step, numPlays):
        return math.sqrt(2 * math.log(step + 1) / numPlays)
    
     
    #Calculate rewards
    def rewards(self,choice):
        #Gaussain Reward
        #return random.gauss(self.means[choice],1)
        #Bernoulli Reward(1 sample from Binomial Distribution)
        return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        
    def ucb1(self,numActions):
    
        #Set the environment
        self.numActions=numActions
        
        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [0] * self.numActions
        self.upbs = [0] * self.numActions
        #self.numRounds = 3000000
        self.numRounds = 60000
        #numRounds = 250000
        
        self.arm_reward = [0]*numActions

        self.bestAction=self.numActions-2

        self.means =[0.06 for i in range(self.numActions)]
        

        for i in range(self.numActions/3):
            self.means[i]=0.01

        '''
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.03
            i=i+1
        '''
        self.means[self.bestAction]=0.1
        
        
        # initialize empirical sums pull each arm once
        t=1
        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]
        
        for i in range(self.numActions):
            theReward = self.rewards(i)

            
            action=i
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward

            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            t = t + 1
            

        while True:
            ucbs = [(self.payoffSums[i] / self.numPlays[i]) + self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]

            #getting the maximum of the ucbs
            action = max(range(self.numActions), key=lambda i: ucbs[i])
            theReward = self.rewards(action)
            #print theReward,action

            #pulling the arm
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward

            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            if t>=self.numRounds:
                break
            
            t = t + 1

            if t%10000==0:
                print t

            
    
        action=max(range(self.numActions), key=lambda i: self.arm_reward[i])

        #Print output file for regret for each timestep
        f = open('expt/testRegretUCB101.txt', 'a')
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
            
            obj=ucb1()
            cumulativeReward,bestActionCumulativeReward,regret,bestArm,timestep=obj.ucb1(arms)
            if bestArm!=arms-2:
                wrong=wrong+1
            print "turn: "+str(turn)+"\twrong: "+str(wrong)+"\tarms: "+str(arms)+"\tbarm: "+str(bestArm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)

            #Print final output file for cumulative regret
            f = open('expt/testUCB101.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (arms, bestArm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        arms=arms+1
        