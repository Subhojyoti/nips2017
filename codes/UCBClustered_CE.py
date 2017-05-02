'''
Created on Sept 11, 2016

@author: Subhojyoti
'''

import math
import random
import numpy
from sets import Set

class ClusUCB_CE(object):
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



    #Count the number of remaining Sets
    def remSets(self):
        count=0
        for i in range(len(self.sets)):
            if bool(self.sets[i])==True:
                count=count+1
                arm=i
        return count


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

        print "Init:" +str(self.sets)


    #Create equal sized Clusters
    def setCreation(self):

        self.setInit()

        print "rangeTake: "+ str(self.rangetake)


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

        for i in range(self.numActions):
            for j in range(i+1,self.numActions):

                if len(self.sets[j])!=0 and  len(self.sets[i])+len(self.sets[j]) <= self.setSizeLimit:

                    self.sets[i]=self.sets[j]|self.sets[i]
                    #print self.sets[i],self.sets[j]
                    self.sets[j].clear()

                #i=i+2
        #self.calculate_setMaxPay()
        #self.calculate_setMinPay()
        print self.sets

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



                    self.func=math.log(self.horizon)

                    c=math.sqrt((math.log(self.func*self.horizon*self.rangetake*self.rangetake))/(2*self.weightSet*(self.nm)))


                    if (self.avgPayOffSums[maxSetArm] + c < self.avgPayOffSums[take]-c and take!=maxSetArm):

                        print "Remove Set:"+ str(k), str(len(self.sets[k]))

                        for arms in self.sets[k]:
                            self.B[arms]=-1


                        self.sets[k].clear()


    #Calculate number of pulls each round
    def calculate_pulls(self):


        self.func=math.log(self.horizon)
        self.nm=int(math.ceil((2*math.log(self.func*self.horizon*self.rangetake*self.rangetake))/(self.rangetake)))


        print "nm:"+str(self.nm)
        return self.nm


    '''
    Running the Clustered UCB
    '''

    def clusUCB_CE(self,arms,p,turn,wrong):

        '''
        Set Environment
        '''
        self.numActions = arms

        self.horizon=60000
        #self.horizon=100000 + self.numActions*self.numActions*1000



        self.rangetake=1.0
        self.bestAction=self.numActions-2



        self.numRounds = math.floor(0.5*math.log10(self.horizon/math.e)/math.log10(2))

        print "\n\nnumrounds:"+str(self.numRounds)

        self.means =[0.06 for i in range(self.numActions)]


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
        self.weightSet=1.0
        self.weightArm=1.0
        self.p=p

        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.avgPayOffSums = [0] * self.numActions
        self.variance = [0] * self.numActions

        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0
        self.regret = 0
        self.regretBounds = 0

        self.arm_reward = [0]*self.numActions
        self.setSizeLimit=math.ceil((self.numActions*1.0)/self.p)
        print "sizeLimit: "+str(self.setSizeLimit)
        self.func=math.log(self.horizon)

        self.actionRegret=[]



        #Group Arms
        self.setCreation()
        
        while True:

            print "\n\nRound: "+str(self.m)
            print "AvgPayOffsums: " + str(self.avgPayOffSums)
            print "Final sets: "+str(self.sets)

            print "B: "+str(self.B)


            self.calculate_pulls()


            #Pull all arms equally in the round
            for i in range(len(self.sets)):
                if len(self.sets[i])>=1:


                    for arm in self.sets[i]:

                        if self.B[arm]!=-1:
                            for k in range(self.nm):
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


            self.SetElimination()



            print "Sets: "+str(self.sets)
            print "SetLimit: "+str(self.setSizeLimit) + " epsilon: "+str(self.rangetake) + " func: "+str(self.func)

            print "NumPlays:" + str(self.numPlays)
            print "Total Plays: "+str(sum(self.numPlays))
            print self.remSets()

            #update parameters
            self.rangetake=self.rangetake/2
            self.weightSet=pow(2,self.m)*pow(2,self.m)*2.0
            self.weightArm=pow(2,self.m)*pow(2,self.m)*pow(2,self.m)*pow(2,self.m)*2.0


            if (self.m>= self.numRounds or self.remSets() == 1) or self.timestep>self.horizon:
                break

            self.m=self.m+1


        #Find the max arm
        maxarm=self.min1
        take=-1
        for i in range(self.numActions):
            if self.B[i]!=-1:
                if maxarm<self.avgPayOffSums[i]:
                    maxarm=self.avgPayOffSums[i]
                    take=i
        arm=take


        print "last arm:"+str(arm) + " turn:"+str(turn) + " wrong:"+str(wrong)

        #if horizon not reached dpull the best Arm outputed till horizon
        while self.timestep<self.horizon:

            theReward = self.rewards(arm,self.timestep)
            self.arm_reward[arm]=self.arm_reward[arm]+theReward
            self.numPlays[arm] += 1
            self.payoffSums[arm] += theReward

            self.avgPayOffSums[arm] = self.payoffSums[arm] / self.numPlays[arm]

            self.cumulativeReward += theReward
            self.bestActionCumulativeReward += theReward if arm == self.bestAction else self.rewards(self.bestAction, self.timestep)
            self.regret = self.bestActionCumulativeReward - self.cumulativeReward
            self.actionRegret.append(self.regret)

            self.timestep=self.timestep+1


        #Print output file for regret for each timestep
        f = open('expt/testRegretclUCB_CE01.txt', 'a')
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

            ucb= ClusUCB_CE()
            cumulativeReward,bestActionCumulativeReward,regret,bestArm,timestep=ucb.clusUCB_CE(arms,10,turn,wrong)
            if bestArm!=arms-2:
                wrong=wrong+1

            print "turn: "+str(turn)+"\twrong: "+str(wrong)+"\tarms: "+str(arms)+"\tbarm: "+str(bestArm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)


            #Print final output file for cumulative regret
            f = open('expt/clUCB_CE01.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (arms, bestArm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()

        arms=arms+1

        print "total wrong: "+str(wrong)
