'''
Created on Jul 28, 2015

@author: Subhojyoti
'''

import math
import random
import numpy

class UCBRevisted(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''

    
    #Calculate rewards
    def rewards(self,choice, timestep):
        #Gaussain Reward
        #return random.gauss(self.means[choice],1)
        #Bernoulli Reward(1 sample from Binomial Distribution)
        return sum(numpy.random.binomial(1,self.means[choice],1))/1.0

    #UpperBound Definition
    def upperBound(self, step, numPlays,horizon,delta_tilda):
    
        #return math.sqrt( math.log10(horizon*delta_tilda*delta_tilda) / ((2*numPlays)*math.log10(math.e)) ) 
        
        return math.sqrt( math.log(horizon*delta_tilda*delta_tilda) / ((2*self.nm)) )
        #return math.sqrt( math.log(horizon*delta_tilda*delta_tilda) / ((2*numPlays)) ) 
        #return math.sqrt( math.log10(horizon*delta_tilda*delta_tilda) / ((2*self.nm)*math.log10(math.e)) )
    
    def ucbRevisited(self,arms,turn,wrong):

        #Set the environment
        self.numActions = arms
        self.horizon=400000
        self.bestAction=self.numActions-2

        self.numRounds = 0.5*math.floor(math.log10(self.horizon/math.e)/math.log10(2))

        self.means =[0.06 for i in range(self.numActions)]
        

        for i in range(self.numActions/3):
            self.means[i]=0.01

        '''
        for i in range(self.numActions/3):
            self.means[i]=0.47
        
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.46
            i=i+1
        '''
        self.means[self.bestAction]=0.1
        self.arm_reward = [0]*self.numActions

        self.actionRegret=[]
        
        

        
        self.timestep=0
        self.m=0
        self.delta_tilda=1.0
        self.B=[0 for i in range(self.numActions)]
        self.ucbs = [0] * self.numActions
        self.upbs = [0] * self.numActions
        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.avgPayoffsums = [0] * self.numActions
        
        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0
        self.regret = 0
        self.regretBounds = 0
        
        self.arm_reward = [0]*self.numActions
        
        self.nm=0
        

        
        
        
        while True:
            
            #Arm selection
            #Count the number of arms not deleted
            count=0
            arm=-1
            for i in range(self.numActions):
                if self.B[i]!=-1:
                    count=count+1
                    arm=i
            
            print "round:"+str(self.m)
            
            #if remaining arms more than 1
            if count > 1:
                
                #Choose each arm nm number of times
                print "horizon:"+str(self.horizon)
                print "DT:"+str(self.delta_tilda)

                self.nm=math.ceil( 2*(math.log(self.horizon*self.delta_tilda*self.delta_tilda))/(self.delta_tilda*self.delta_tilda) )
                print 'nm: '+str(self.nm)
                
                for i in range(self.numActions):
                    
                    for j in range(int(self.nm)):
                        
                        if self.B[i]!=-1:
                            theReward = self.rewards(i, self.timestep)
                            
                            self.arm_reward[i]=self.arm_reward[i]+theReward
                            self.numPlays[i] += 1
                            self.payoffSums[i] += theReward
                            self.avgPayoffsums[i] = self.payoffSums[i] / self.numPlays[i]
                            self.ucbs[i] = (self.avgPayoffsums[i]) + self.upperBound(self.timestep, self.numPlays[i], self.horizon, self.delta_tilda) 
                            self.upbs[i] = self.upperBound(self.timestep, self.numPlays[i], self.horizon, self.delta_tilda) 
                            

                            self.cumulativeReward += theReward
                            self.bestActionCumulativeReward += theReward if i == self.bestAction else self.rewards(self.bestAction, self.timestep)
                            self.regret = self.bestActionCumulativeReward - self.cumulativeReward
                            self.actionRegret.append(self.regret)

                            self.timestep=self.timestep+1
                
                print "timestep:"+str(self.timestep)
                print "upbs:"+str(self.upbs)
                print "ucbs:"+str(self.ucbs)
                        

                
            #Arm Elimination
            if count > 1:
                arm=-1
                max1=-9999999
                for i in range(self.numActions):
                    if (self.avgPayoffsums[i]) > max1:
                        max1=(self.avgPayoffsums[i])
                        arm=i
                print 'arm:'+str(arm)
                
                for i in range(self.numActions):
                    
                    if ((self.avgPayoffsums[i])+ self.upperBound(self.timestep, self.numPlays[i], self.horizon, self.delta_tilda)) < ((self.avgPayoffsums[arm])- self.upperBound(self.timestep, self.numPlays[arm], self.horizon, self.delta_tilda)) and self.B[i]!=-1:
                        self.B[i]=-1
                        print "armR:"+str(i)
            
            
            #Calculate number of remaining arms
            count=0
            arm=-1
            for i in range(self.numActions):
                if self.B[i]!=-1:
                    count=count+1
                    arm=i

            #update parameters
            self.m += 1
            self.delta_tilda=self.delta_tilda/2

            print "B:"+str(self.B)

            if self.m >= self.numRounds or count==1:
                print "All round ends"
                break
        
        print "last arm:"+str(arm) + " turn:"+str(turn) + " wrong:"+str(wrong)

        #if horizon not reached dpull the best Arm outputed till horizon
        while self.timestep<self.horizon:
        
            theReward = self.rewards(arm,self.timestep)
            self.arm_reward[arm]=self.arm_reward[arm]+theReward
            self.numPlays[arm] += 1
            self.payoffSums[arm] += theReward
                    
            self.avgPayoffsums[arm] = self.payoffSums[arm] / self.numPlays[arm]
            
            self.cumulativeReward += theReward
            self.bestActionCumulativeReward += theReward if arm == self.bestAction else self.rewards(self.bestAction, self.timestep)
            self.regret = self.bestActionCumulativeReward - self.cumulativeReward
            self.actionRegret.append(self.regret)
                    
            self.timestep=self.timestep+1
        

        #Print output file for regret for each timestep
        f = open('expt/testRegretUCBR01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()

        return self.cumulativeReward,self.bestActionCumulativeReward,self.regret,arm,self.timestep


if __name__ == "__main__":
    

    wrong=0

    arms=20
    while arms<=20:
        
        for turn in range(0,1):

            #set the random seed, same for all environment
            numpy.random.seed(arms+turn)

            ucb= UCBRevisted()
            cumulativeReward,bestActionCumulativeReward,regret,bestArm,timestep=ucb.ucbRevisited(arms,turn,wrong)

            if bestArm!=arms-2:
                wrong=wrong+1

            print "turn: "+str(turn)+"\twrong: "+str(wrong)+"\tarms: "+str(arms)+"\tbarm: "+str(bestArm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)

            #Print final output file for cumulative regret
            f = open('expt/testUCBR01.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (arms, bestArm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
        arms=arms+1
    
