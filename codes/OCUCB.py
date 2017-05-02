'''
Created on Dec 21, 2016

@author: Subhojyoti
'''


import math
import random
import numpy

class ucb1_2(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    
    def upperBound(self, step, numPlays):
        self.alpha=2.0
        self.psi=2.0
        return math.sqrt((self.alpha * math.log((self.psi*self.numRounds) / (step))) / numPlays)
    
     
    def rewards(self,choice):
        #return random.gauss(self.means[choice],1)
        #print sum(numpy.random.binomial(1,self.means[choice],200))/200.0
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
        
        #bestAction=arms/2
        self.bestAction=self.numActions-2
        
        #biases = [1.0 / k for k in range(5,5+numActions)]
        #means = [0.5 + b for b in biases]
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
        t=1
        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]
        
        for i in range(self.numActions):
            theReward = self.rewards(i)
            #self.numPlays[i]=self.numPlays[i]+1
            
            action=i
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            
            #f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            #f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))
            
            #yield action, theReward, ucbs
            
            
            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            t = t + 1
            
        #t = numActions
        
        
            
        
        #t=1
        while True:
            ucbs = [(self.payoffSums[i] / self.numPlays[i]) + self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #upbs = [self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #print "upbs"
            #print upbs
            #print ucbs
            #getting the maximum of the ucbs
            action = max(range(self.numActions), key=lambda i: ucbs[i])
            theReward = self.rewards(action)
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            
            #f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            #f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))
            
            #yield action, theReward, ucbs
            
            
            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            if t>=self.numRounds:
                break
            
            t = t + 1
            
            #print t
            '''
            if t%100000==0:
                print t
            '''
            
    
        action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        #print self.arm_reward
        
        
        f = open('expt/testRegretOCUCB01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()
        
        return cumulativeReward,bestActionCumulativeReward,regret,action,t
        

if __name__ == "__main__":
    
    wrong=0
    i=20
    while i<=20:
        turn=0
        for j in range(0,100):
            
            random.seed(i+j)
            
            obj=ucb1_2()
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep=obj.ucb1(i)
            if arm!=i-2:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn+1)+"\twrong: "+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('expt/testOCUCB1.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        i=i+1
        