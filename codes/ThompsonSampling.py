'''
Created on Oct 6, 2015

@author: Subhojyoti
'''

import math
import random
import numpy
#from random import betavariate
#from scipy.special import btdtri


class   TS(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
     
   #Calculate rewards
    def rewards(self,choice):

        #Bernoulli Reward(1 sample from Binomial Distribution)
        return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        
    def TS(self,numActions):
    
        #Set the environment
        self.numActions=numActions
        
        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [0] * self.numActions
        self.upbs = [0] * self.numActions
        #self.numRounds = 3000000
        self.numRounds = 20000
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
        
        
        # initialize empirical sums
        '''
        for i in range(self.numActions):
            self.payoffSums[i] = self.rewards(i)
            self.numPlays[i]=self.numPlays[i]+1
        '''
        
        theta=[0.0]*self.numActions
        success=[0.0]*self.numActions
        failure=[0.0]*self.numActions
        
        for i in range(self.numActions):
            theta[i]=random.betavariate(success[i]+1,failure[i]+1)
            

        cumulativeReward = 0
        bestActionCumulativeReward = 0
            
        self.actionRegret=[]
        t=1
        while True:

            
            for i in range(self.numActions):

                theta[i]=random.betavariate(success[i]+1,failure[i]+1)
            
            action=max(range(self.numActions), key=lambda i: theta[i])
            


            theReward = self.rewards(action)
            
            theReward1 = sum(numpy.random.binomial(1,theReward,1))/1.0
            
            if theReward1==1.0:
                success[action]=success[action]+1
            else:
                failure[action]=failure[action]+1
            
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
        f = open('expt/testRegretTS01.txt', 'a')
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


            obj=TS()
            cumulativeReward,bestActionCumulativeReward,regret,bestArm,timestep=obj.TS(arms)
            if bestArm!=arms-2:
                wrong=wrong+1

            print "turn: "+str(turn)+"\twrong: "+str(wrong)+"\tarms: "+str(arms)+"\tbarm: "+str(bestArm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)

            #Print final output file for cumulative regret
            f = open('expt/testTS1.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (arms, bestArm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        arms=arms+1
        
