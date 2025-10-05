import sys;read=sys.stdin.readline
import copy
'''
1. 행렬 입력 기능
2. 행렬식을 이용한 역행렬 계산 기능
3. 가우스-조던 소거법(Gauss-Jordan elimination)을 이용한 역행렬 계산 기능
4. 결과 출력 및 비교 기능
'''

# 1. 행렬 입력 기능
def input_matrix():
    print(">> N을 입력해주세요", end=" ")
    n = int(read())
    matrix = []
    for i in range(1,n+1):
        print(">> %d번째 행" %i, end=" ")
        arr = list(map(float,read().split()))
        matrix.append(arr)
    return matrix

# 2. 행렬식을 이용한 역행렬 계산 기능
# A^(-1) = (1/det(A)) * C^T

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        det = 0
        for i in range(n):
            det += ((-1) ** i) * matrix[0][i] * determinant([ (r[0:i] + r[i+1:])for r in (matrix[1:])])
        return det
    
def get_cofactor_matrix(matrix):
    n = len(matrix)
    cofactor_matrix = [[0 for j in range(n)]for i in range(n)]
    for i in range(n):
        for j in range(n):
            cofactor_matrix[i][j] = ((-1) ** (i + j)) * determinant([ (r[0:j] + r[j+1:])for r in (matrix[0:i] + matrix[i+1:])])
    return cofactor_matrix

def get_inverse_cofactor(matrix, cofactor_matrix):
    det = determinant(matrix)
    cofactor_transpose = get_transpose(cofactor_matrix)
    n = len(matrix)
    inverse_matrix = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            inverse_matrix[i][j] = cofactor_transpose[i][j] * (1 / det)
    return inverse_matrix


def get_transpose(matrix):
    n = len(matrix)
    transposed = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            transposed[j][i] = matrix[i][j]
    return transposed


# 3. 가우스-조던 소거법(Gauss-Jordan elimination)을 이용한 역행렬 계산 기능
def swap(matrix, a, b):
    n = len(matrix)
    temp_arr = matrix[b]
    matrix[b] = matrix[a]
    matrix[a] = temp_arr


def make_unit_matrix(n):
    unit_matrix = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        unit_matrix[i][i] = 1
    return unit_matrix

def get_gauss_jordan(matrix, unit_matrix):
    n = len(matrix)
    for i in range(n):
        node = matrix[i][i]
        if node == 0:
            for j in range(n):
                if matrix[j][i] != 0.0:
                    swap(matrix, i, j)
                    swap(unit_matrix, i, j)
                    node = matrix[i][i]
                    break
        for j in range(n):
            matrix[i][j] /= node
            unit_matrix[i][j] /= node
        for j in range(n):
            if i != j:
                node_for_eliminate = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= matrix[i][k] * node_for_eliminate
                    unit_matrix[j][k] -= unit_matrix[i][k] * node_for_eliminate
    return unit_matrix

# 4. 결과 출력 및 비교 기능
def print_matrix(matrix):
    n = len(matrix)
    i = 1
    for row in matrix:
        print("%d번째 행 :" %i,end=" ")
        print(" ".join(f"{x:.2f}" for x in row))
        i += 1

def compare(matrix_1, matrix_2):
    n = len(matrix_1)
    for i in range(n):
        for j in range(n):
            if abs(matrix_1[i][j] - matrix_2[i][j]) > 1e-3:
                print(matrix_1[i][j])
                print(matrix_2[i][j])
                return print("두 행렬은 서로 다름")
    return print("두 행렬은 동일함")

def check(matrix, inversed_matrix):
    n = len(matrix)
    res_arr = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                res_arr[i][j] += matrix[i][k] * inversed_matrix[k][j]
    print_matrix(res_arr)
    return
def main():
    matrix = input_matrix()
    matrix_for_check = copy.deepcopy(matrix)
    if determinant(matrix) != 0:
        cofactor_matrix = get_cofactor_matrix(matrix)
        inverse_matrix_cofactor = get_inverse_cofactor(matrix, cofactor_matrix)
        unit_matrix = make_unit_matrix(len(matrix))
        gauss_jordan = get_gauss_jordan(matrix, unit_matrix)
        print("------------------------")
        print("행렬식을 이용하여 구한 역행렬")
        print_matrix(inverse_matrix_cofactor)
        print("------------------------")
        print("가우스-조던 소거법을 이용하여 구한 역행렬")
        print_matrix(gauss_jordan)
        print("------------------------")
        compare(inverse_matrix_cofactor, gauss_jordan)
        print("------------------------")
        print("행렬식을 이용하여 구한 역행렬 검산")
        check(matrix_for_check, inverse_matrix_cofactor)
        print("------------------------")
        print("가우스 - 조던 소거법을 이용하여 구한 역행렬 검산")
        check(matrix_for_check, gauss_jordan)
    else:
        print("det(A)=0, 역행렬이 존재하지 않습니다.")

if __name__ == "__main__":
    main()

'''
testcase1.
3 2 1
1 2 3
2 1 3

testcase2.
2 1 3 2
1 0 2 1
4 1 8 5
5 1 3 2

testcase3.
2 1 3 2 2
1 0 2 1 4
4 1 8 5 1
5 1 3 2 7
-1 5 2 2 3
'''
