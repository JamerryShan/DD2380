import itertools

def vertibi(obs, states, Pi, A, B):
    obs_len=len(obs)
    states_len=len(states)
    max_p = [[0] * states_len for i in range(obs_len)]
    path = [[0] * obs_len for i in range(states_len)]
    for i in range(len(states)):
        max_p[0][i] = Pi[0][i] * B[i][obs[0]]       
        path[i][0] = i

    for t in range(1, len(obs)):
        newpath = [[0] * obs_len for i in range(states_len)]
        for y in range(len(states)):
            prob = -1
            for y0 in range(len(states)):
                nprob = max_p[t-1][y0] * A[y0][y] * B[y][obs[t]]
                if nprob > prob:
                    prob = nprob
                    state = y0
                    max_p[t][y] = prob
                    for m in range(t):
                        newpath[y][m] = path[state][m]
                    newpath[y][t] = y

        path = newpath

    max_prob = -1
    path_state = 0
    for y in range(len(states)):
        if max_p[len(obs)-1][y] > max_prob:
            max_prob = max_p[len(obs)-1][y]
            path_state = y

    return path[path_state]
    
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
        # new_merged_list=[]
        #new_merged_list = list(itertools.chain(*res_mat))
        #
        # print(new_merged_list)
        # for i in new_merged_list:
        #    print(i,end=" ")

def getcolumn(A, column_num):
    column = [[i[column_num]] for i in A]
    return column

def getrow(A, row_num):
    row = A[row_num]
    return row

def dotmutiplx(A, B):
    res = []
    for i in range(len(A)):
            res.append(A[i]*B[i])
    return [res]

def matrixtrans(A):
    trans = [[A[row][column] for row in range(0,len(A)) ] for column in range(0,len(A[0]))]
    return trans

def probablility(A, B, pi, O):
    for i in range(len(O)):
        if i == 0:
            temp = dotmutiplx(pi[0], matrixtrans(getcolumn(B, O[i]))[0])
            #print(temp)
        else:
            temp = dotmutiplx(matrixmul(temp, A)[0], matrixtrans(getcolumn(B, O[i]))[0])
    return sum(temp[0])

def main():
    inputlistA = [float(i) for i in input().split()]
    inputlistB = [float(i) for i in input().split()]
    inputlistPi = [float(i) for i in input().split()]
    inputlistO = [int(i) for i in input().split()]
    rowsA, columnsA = int(inputlistA[0]), int(inputlistA[1])
    rowsB, columnsB = int(inputlistB[0]), int(inputlistB[1])
    rowsPi, columnsPi = int(inputlistPi[0]), int(inputlistPi[1])
    vectorA = inputlistA[2:]
    vectorB = inputlistB[2:]
    vectorPi = inputlistPi[2:]
    O = inputlistO[1:]
    matrixA = []
    matrixB = []
    matrixPi = []
    states=[]
    for i in range(0, int(inputlistA[0])):
        states.append(i)
    for i in range(rowsA):
        matrixA.append(vectorA[i*columnsA:i*columnsA+columnsA])
    for i in range(rowsB):
        matrixB.append(vectorB[i*columnsB:i*columnsB+columnsB])
    for i in range(rowsPi):
        matrixPi.append(vectorPi[i*columnsPi:i*columnsPi+columnsPi])

    #result = probablility(matrixA, matrixB, matrixPi, O)
    result = vertibi(O, states, matrixPi, matrixA, matrixB)
    for i in range(0, len(result)):
        print(result[i], end=" ")
    #print(result, end=" ")
    # print(matrixA)
    # print(matrixB)
    # print(matrixPi)
    #m = mat_mul()
    #PiA = matrixmul(matrixPi, matrixA)
    # print(PiA)
    #n = mat_mul()
    #PiAB = matrixmul(PiA, matrixB)
    # print(PiAB)
    #print(len(PiAB), len(PiAB[0]), end=" ")

if __name__ == '__main__':
    main()
