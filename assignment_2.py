from copy import deepcopy
import sys;read=sys.stdin.readline
global N
N = 5
'''
1. 관계 행렬 입력 기능 (크기는 5 x 5)
2. 동치 관계 판별 기능
3. 동치 관계일 경우, 동치류 출력 기능
4. 폐포 구현 기능
'''
#1. 관계 행렬 입력 기능
def input_matrix():
    matrix = [list(map(int, read().split())) for i in range(N)]
    print("\n당신의 입력")
    output_matrix(matrix)
    return matrix

def output_matrix(matrix):
    for i in range(N):
        print(matrix[i])

#반사 : 자기 자신을 향하는 관계 존재 여부
def reflect(matrix):
    for i in range(N):
        for j in range(N):
            if i == j and matrix[i][j] != 1:
                return False
    return True

#대칭 : (x, y)가 있을 때 (y, x)도 있어야 함
def symmetric(matrix):
    for i in range(N):
        for j in range(N):
            if (matrix[i][j] == 1) and (matrix[j][i] == 0):
                return False
    return True

#추이
def transitive(matrix):
    for i in range(N):
        for j in range(N):
            if (matrix[i][j] == 1):
                for k in range(N):
                    if (matrix[j][k] == 1) and (matrix[i][k] == 0):
                        return False
    return True

#동치 관계 확인, 각 원소 동치류 출력
def equi_check(matrix):
    flag_comment = ["반사", "대칭", "추이"]
    flag_li = [False, False, False]
    flag_li[0] = reflect(matrix)
    flag_li[1] = symmetric(matrix)
    flag_li[2] = transitive(matrix)
    if flag_li[0] and flag_li[1] and flag_li[2] == 1:
        print("동치 관계입니다.")
        equi_print(matrix)
        return (True, flag_li)
    else:
        error_flag = [flag_comment[i] for i, flag in enumerate(flag_li) if not flag]
        print("{}관계가 아니기 때문에 동치 관계가 아닙니다.".format(", ".join(error_flag)))
        return (False, flag_li)

def equi_print(matrix):
    equi_dict = {}
    for i in range(N):
        equi_dict[i] = []
        for j in range(N):
            if matrix[i][j] == 1:
                equi_dict[i].append(j + 1)
    for i in range(N):
        print("{}의 동치류 : {}".format(i + 1, equi_dict[i]))

#반사 폐포 구현
def reflex_closure(matrix):
    for i in range(N):
        matrix[i][i] = 1
    print("\n반사 폐포 적용 후 행렬")
    output_matrix(matrix)

#대칭 폐포 구현
def symmetric_closure(matrix):
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1 and matrix[j][i] == 0:
                matrix[j][i] = 1
    print("\n대칭 폐포 적용 후 행렬")
    output_matrix(matrix)

#추이 폐포 와샬 알고리즘을 이용해 구현
def transitive_closure(matrix):
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if matrix[i][k] and matrix[k][j]:
                    matrix[i][j] = 1
    print("\n추이 폐포 적용 후 행렬")
    output_matrix(matrix)

#(추가 기능) 동치가 되기 위해 필요한 폐포만을 적용하여 출력
def make_equi(matrix, flag_li):
    is_equi = False
    while not(flag_li[0] and flag_li[1] and flag_li[2]) and not is_equi:
        for i in range(3):
            if not flag_li[i] and i == 0:
                reflex_closure(matrix)
                flag_li[i] = True
            elif not flag_li[i] and i == 1:
                symmetric_closure(matrix)
                flag_li[i] = True
            elif not flag_li[i] and i == 2:
                transitive_closure(matrix)
                flag_li[i] = True
        is_equi, flag_li = equi_check(matrix)

def main():
    matrix = []
    matrix = input_matrix()
    is_equi, flag_li = equi_check(matrix)
    if not is_equi:

        r_matrix_copy = deepcopy(matrix)
        s_matrix_copy = deepcopy(matrix)
        t_matrix_copy = deepcopy(matrix)
        e_matrix_copy = deepcopy(matrix)

        reflex_closure(r_matrix_copy)
        equi_check(r_matrix_copy)

        symmetric_closure(s_matrix_copy)
        equi_check(s_matrix_copy)

        transitive_closure(t_matrix_copy)
        equi_check(t_matrix_copy)

        print("동치로 만들기")
        make_equi(e_matrix_copy, flag_li)


if __name__ == "__main__":
    main()
