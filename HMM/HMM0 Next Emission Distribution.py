import itertools  

class mat_mul():
    def mm(self,A,B):
        row_len = len(A)
        column_len = len(B[0])
        cross_len = len(B)
        res_mat = [[0] * column_len for i in range(row_len)] 
        #print(res_mat)
        for i in range(row_len):
            for j in range(column_len):
                for k in range(cross_len):
                    temp = A[i][k] * B[k][j]
                    res_mat[i][j] += temp
        #print(res_mat)
        return res_mat  
        #new_merged_list=[]
        #new_merged_list = list(itertools.chain(*res_mat))
        #
        #print(new_merged_list)
        #for i in new_merged_list:
        #    print(i,end=" ")

def main():
    inputlistA = [float(i) for i in input().split()]
    inputlistB = [float(i) for i in input().split()]
    inputlistPi = [float(i) for i in input().split()]
    rowsA, columnsA = int(inputlistA[0]), int(inputlistA[1])
    rowsB, columnsB = int(inputlistB[0]), int(inputlistB[1])
    rowsPi, columnsPi = int(inputlistPi[0]), int(inputlistPi[1])
    vectorA = inputlistA[2:]
    vectorB = inputlistB[2:]
    vectorPi = inputlistPi[2:]
    matrixA = []
    matrixB = []
    matrixPi= []
    for i in range(rowsA):
            matrixA.append(vectorA[i*columnsA:i*columnsA+columnsA])         
    for i in range(rowsB):
            matrixB.append(vectorB[i*columnsB:i*columnsB+columnsB])
    for i in range(rowsPi):
            matrixPi.append(vectorPi[i*columnsPi:i*columnsPi+columnsPi])
    #print(matrixA)
    #print(matrixB)
    #print(matrixPi)
    m = mat_mul()
    PiA=m.mm(matrixPi,matrixA)
    #print(PiA)
    n = mat_mul()
    PiAB=n.mm(PiA,matrixB)
    #print(PiAB)
    print(len(PiAB),len(PiAB[0]),end=" ")
    new_merged_list=[]
    new_merged_list = list(itertools.chain(*PiAB))
    #print(new_merged_list)
    for i in new_merged_list:
        print(i,end=" ")

if __name__ == '__main__':
    main()