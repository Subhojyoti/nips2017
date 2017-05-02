'''
Created on May 12, 2016

@author: Subhojyoti

code taken from: http://mloss.org/software/view/415/
'''


import math
import random
import numpy

class DMED(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    #Calculate Divergence Function
    def kl(self,p,q,eps = 1e-15):
        p = max(p, eps); 
        p = min(p, 1-eps);  
        q = max(q, eps); 
        q = min(q, 1-eps);
        y = p*math.log(p/q) + (1-p)*math.log((1-p)/(1-q));
        return y
   
    #Calculate rewards
    def rewards(self,choice):
        #Gaussain Reward
        #return random.gauss(self.means[choice],1)
        #Bernoulli Reward(1 sample from Binomial Distribution)
        return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        
    def DMED(self,numActions):

        #genuine = true -> DMED,
        #genuine = false -> DMED+(less aggressive)

        self.genuine=True

        #Set the environment
        self.numActions=numActions
        
        self.N = [0] * self.numActions
        self.S = [0] * self.numActions
        self.L = [i for i in range(self.numActions)]
        
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
        
        t=1.0
        self.means[self.bestAction]=0.1
        

        
        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]
        
        for i in range(self.numActions):
            theReward = self.rewards(i)
            self.numPlays[i]=self.numPlays[i]+1
            
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
            
            
            
            if len(self.L) > 0:
                # Play action on the list and update the list
                action = self.L[0]
                #lastAction=action
                self.L1=[]
                for i in range(1,len(self.L)):
                    self.L1.append(self.L[i])
                self.L=[]
                for i in range(0,len(self.L1)):
                    self.L.append(self.L1[i])
            else:
                # Make new list an play first action
                ucbs = [(self.payoffSums[i] / self.numPlays[i])  for i in range(self.numActions)]
                c = max(range(self.numActions), key=lambda i: ucbs[i]) # Current best empirical mean
                #print c
                if (self.genuine):
                    
                    for i in range(self.numActions):
                        take=self.numPlays[i]*self.kl((self.payoffSums[i] / self.numPlays[i]), self.payoffSums[c]/self.numPlays[c])
                        if take< math.log(t/self.numPlays[i]):
                            self.L.append(i) 
                else:
                    
                    for i in range(self.numActions):
                        take=self.numPlays[i]*self.kl((self.payoffSums[i] / self.numPlays[i]),self.payoffSums[c] / self.numPlays[c])
                        if take< math.log(t):
                            self.L.append(i)
                    #self.L = self.find(self.numPlays[i]*self.kl(self.payoffSums[c] / self.numPlays[c]) < math.log(t));
                
                #print self.L,self.L1
                if len(self.L)>-1:
                    #print "L: "+str(self.L)
                    action = self.L[0]
                    #lastAction=action
                    self.L1=[]
                    for i in range(1,len(self.L)):
                        self.L1.append(self.L[i])
                    self.L=[]
                    
                    for i in range(0,len(self.L1)):
                        self.L.append(self.L1[i])
                    #print "L: "+str(self.L)    

            theReward = self.rewards(action)
            #print theReward,action
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
        f = open('expt/testRegretDMED01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()

        return cumulativeReward,bestActionCumulativeReward,regret,action,t
        

if __name__ == "__main__":
    
    wrong=0
    arms=20
    while arms<=20:

        for turn in range(0,100):

            #set the random seed, same for all environment
            random.seed(arms+turn)
            
            obj=DMED()
            cumulativeReward,bestActionCumulativeReward,regret,bestArm,timestep=obj.DMED(arms)
            if arms!=arms-2:
                wrong=wrong+1
            print "turn: "+str(turn)+"\twrong: "+str(wrong)+"\tarms: "+str(arms)+"\tbarm: "+str(bestArm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)


            #Print final output file for cumulative regret
            f = open('expt/testDMED01.txt', 'a')
            f.writelines("arms: %d\tbArm: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (arms, bestArm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        arms=arms+1
        