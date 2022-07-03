import itertools


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
    for i in range(rowsA):
        matrixA.append(vectorA[i*columnsA:i*columnsA+columnsA])
    for i in range(rowsB):
        matrixB.append(vectorB[i*columnsB:i*columnsB+columnsB])
    for i in range(rowsPi):
        matrixPi.append(vectorPi[i*columnsPi:i*columnsPi+columnsPi])
        
    result = probablility(matrixA, matrixB, matrixPi, O)
    print(result)
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
    #new_merged_list = []
    #new_merged_list = list(itertools.chain(*PiAB))
    # print(new_merged_list)
    #for i in new_merged_list:
    #    print(i, end=" ")


if __name__ == '__main__':
    main()
