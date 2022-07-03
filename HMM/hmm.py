#!/usr/bin/env python3
from __future__ import division
from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *
import random
import math
import numpy as np
import copy
import time
import os
def BW(A, B, pi, O):
    #initialization
    maxiters = 100
    iters = 0
    oldlogprob = -(math.inf)
    #done = 0
    pi_len = len(pi[0])
    O_len = len(O)
    #print(O_len, pi_len)
    while True:
        #print(A,B,pi)
        #the alpha-pass
        c0 = 0
        a0 = [0] * pi_len
        for i in range(pi_len):
            a0[i] = pi[0][i] * B[i][O[0]]
            c0 += a0[i]
            
        #scal alph0[i]
        # if c0==0:
        #     c0 = 1/10000
        c0 = 1/c0
        for i in range(pi_len):
            a0[i] = c0 * a0[i]
            #print(a0[i])
        #compute alpha t[i]
        a = [[0] * pi_len for j in range(O_len)]
        a[0] = a0
        c = [0] * O_len
        c[0] = c0
        for t in range(1, O_len):
            c[t] = 0
            for i in range(pi_len):
                a[t][i] = 0
                for j in range(pi_len):
                    a[t][i] = a[t][i] + a[t-1][j]*A[j][i]
                a[t][i] = a[t][i] * B[i][O[t]]
                c[t] = c[t] + a[t][i] 
            #scale alpha[t][i]
            # if c[t] == 0:
            #     c[t] = 1/10000
            c[t] = 1/c[t]
            for i in range(pi_len):
                a[t][i] = c[t] * a[t][i]
                
        #the beta-pass
        #let b [T-1][i]=1, scaled by c[T-1]
        b = [[0] * pi_len for j in range(O_len)]
        for i in range(pi_len):
            b[-1][i] = c[-1]
        
        #beta-pass
        for t in reversed(range(O_len-1)):
            for i in range(pi_len):
                b[t][i] = 0
                for j in range(pi_len):
                    b[t][i] = b[t][i] + A[i][j]*B[j][O[t+1]]*b[t+1][j]
                # scale βt(i) with same scale factor as αt(i)
                b[t][i] = c[t]*b[t][i]
                
        #compute dg and g
        #No need to normalize γt(i, j) since using scaled α and β
        dg = [[[0 for i in range(pi_len)] for j in range(pi_len)]
             for k in range(O_len)]
        g = [[sum(j) for j in i] for i in dg]
        #g = [[0] * pi_len] * O_len
        for t in range(O_len-1):
            denom = 0
            for i in range(pi_len):
                #g[t][i] = 0
                for j in range(pi_len):
                    #print(t, i)
                    denom = denom + a[t][i]*A[i][j]*B[j][O[t+1]]*b[t+1][j]
            for i in range(pi_len):
            # g[t][i] = 0
                for j in range(pi_len):
                    # if denom==0:
                    #     denom = 1/10000
                    dg[t][i][j] = (a[t][i]*A[i][j]*B[j][O[t+1]]*b[t+1][j])/denom
                    g[t][i] = g[t][i] + dg[t][i][j]
        
        #Special case for γT −1(i) (as above, no need to normalize)
        denom = 0
        for i in range(pi_len):
            denom = denom + a[-1][i]
        for i in range(pi_len):
            # if denom==0:
            #     denom = 1/10000
            g[-1][i] = a[-1][i]/denom
        
        #Re-estimate A, B and pi
        #re-estimate pi
        for i in range(pi_len):
            pi[0][i] = g[0][i]
        
        #re-estimate A
        for i in range(pi_len):
            for j in range(pi_len):
                denom = 0
                numer = 0
                for t in range(O_len-1):
                    denom = denom + g[t][i]
                    numer = numer + dg[t][i][j]
                # if denom==0:
                #     denom = 1/10000                
                A[i][j] = numer/denom
        
        #re-estimate B
        for i in range(pi_len):
            for j in range(len(B[0])):
            #for j in range(len(B[0])):
                denom = 0
                numer = 0
                for t in range(O_len):
                    if O[t] == j:
                        numer = numer + g[t][i]
                    denom = denom + g[t][i]
                #if denom==0:
                #    denom = 1/10000
                B[i][j] = (numer / denom) + 1/130

        for i in range(pi_len):
            for j in range(len(B[0])):
                B[i][j]=B[i][j]/(sum(getrow(B, i)))

        
        #Compute log[P(O | λ)]
        logprob = 0
        for i in range(O_len):
            logprob = logprob + math.log(c[i])
        #print(logprob)
        logprob = -logprob
        
        #To iterate or not to iterate, that is the question...
        iters = iters + 1
        if (iters < maxiters and logprob > oldlogprob):
            oldlogprob = logprob
            #continue
        else:
            L = [A, B, pi]
            return L

def matrixmul(A, B):
    row_len = len(A)
    column_len = len(B[0])
    cross_len = len(B)
    res_mat = [[0] * column_len for i in range(row_len)]
       # print(res_mat)
    for i in range(row_len):
        for j in range(column_len):
            for k in range(cross_len):
                temp = A[i][k] * B[k][j]
                res_mat[i][j] += temp
        # print(res_mat)
    return res_mat

def getcolumn(A, column_num):
    column = [[i[column_num]] for i in A]
    return column

def getrow(A, row_num):
    row = A[row_num]
    return row

def dotmutiplx(A, B):
    res = []
    #rint(A,B)
    for i in range(len(A)):
        #print(A[i], B[i])
        res.append(A[i]*B[i])
    return [res]

def matrixtrans(A):
    trans = [[A[row][column] for row in range(0,len(A)) ] for column in range(0,len(A[0]))]
    return trans
# observation prob
def probablility(A, B, pi, O):
    for i in range(len(O)):
        if i == 0:
            temp = dotmutiplx(pi[0], matrixtrans(getcolumn(B, O[i]))[0])
            #print(temp)
        else:
            temp = dotmutiplx(matrixmul(temp, A)[0], matrixtrans(getcolumn(B, O[i]))[0])
    return sum(temp[0])
    



class PlayerControllerHMM(PlayerControllerHMMAbstract):
    models=None
    ob_seq=None
    flag = 0
    flags=None
    flags=None
    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        A = [[1/16]*16 for i in range(16)]
        B = [[1/8]*8 for i in range(16)]        
        pi = [[1/16]*16]
        delta = 1/5065255
        for i in range(16):
            A[i][1]-=delta
            A[i][-1]+=delta
            B[i][1]+=delta
            B[i][-1]-=delta
        pi[0][2]+=delta
        pi[0][4]+=delta
        pi[0][5]+=delta
        pi[0][8]-=delta
        pi[0][10]-=delta
        pi[0][14]-=delta
        L = [A, B, pi]
        self.models = [copy.deepcopy(L) for i in range(8)]
        self.ob_seq = [[] for i in range(N_FISH)]
        self.flags=[0,0,0,0,0,0,0]

    def possibility(self, O):
        maxp=0
        sort=0
        for i in range(7):
            #print(self.models[i][0], self.models[i][1], self.models[i][2], O)
            p=probablility(self.models[i][0], self.models[i][1], self.models[i][2], O)
            if p>maxp:
                maxp=p
                sort=i
        #print(sort)
        return sort

    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """
        
        for i in range(N_FISH):
            self.ob_seq[i].append(observations[i])
        
        if step<110:
            return None
        else:
            if self.flag<=70:
                self.flag += 1
            return (self.flag-1, self.possibility(self.ob_seq[self.flag-1]))
        
        #return None
        

    

    def reveal(self, correct, fish_id, true_type):
        """
        This methods gets called whenever a guess was made.
        It informs the player about the guess result
        and reveals the correct type of that fish.
        :param correct: tells if the guess was correct
        :param fish_id: fish's index
        :param true_type: the correct type of the fish
        :return:
        """
        #print(true_type,self.models)
        if self.flags[true_type] == 0:
            self.flags[true_type] = 1
            result=BW(self.models[true_type][0], self.models[true_type][1], self.models[true_type][2], self.ob_seq[fish_id])
            self.models[true_type][0]=result[0]
            self.models[true_type][1]=result[1]
            self.models[true_type][2]=result[2]