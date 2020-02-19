import numpy as np
import scipy.linalg as sla
import clipboard
from fractions import Fraction


def first(A, str1, str2, k, f=0):
    str1 -= 1
    str2 -= 1
    for i in range(A.shape[1]):
        A[str1, i] += k * A[str2, i]
    if f:
        print(A)


def out(A, f, y1=1, x1=1, y2=None, x2=None):
    if x2 is None:
        x2 = A.shape[0]
        y2 = A.shape[1]
    s = '\\begin{pmatrix}\n'
    for i in range(x1 - 1, x2):
        for j in range(y1 - 1, y2):
            if A[i, j].denominator != 1:
                # s += f'\\frac{ {A[i, j].numerator} }{ {A[i, j].denominator} }'
                s += f'{A[i, j].numerator}/{A[i, j].denominator}'
            else:
                s += str(A[i, j]) + ' '
            if j < A.shape[1] - 1:
                s += '& '
        if i < A.shape[0] - 1:
            s += '\\\ \n'
        else:
            s += '\n'
    s += '\\end{pmatrix}\n'
    s += '\\longrightarrow ' + '\\\\' * f + '\n'
    return s


def second(A, str1, str2, f=0):
    str1 -= 1
    str2 -= 1
    for i in range(A.shape[1]):
        A[str1, i], A[str2, i] = A[str2, i], A[str1, i]
    if f:
        print(A)


def third(A, str1, k, f=0):
    str1 -= 1
    for i in range(A.shape[1]):
        A[str1, i] *= k
    if f:
        print(A)


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def isnum(c):
    l = '0123456789-/'
    return c in l


def inp(): # input your matrix
    m, n = map(int, input().split())
    lst = list()
    for i in range(m):
        lst.append(list(map(int, input().split())))
    A = np.array(lst)
    print(A)
    A = A.astype('object')
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] = Fraction(A[i, j], 1)
    return A


def inp_str(is_fraq = True): # insert any string whith NxM numbers and any other symbols
    n, m = map(int, input().split())
    a = input().replace('−', '-')
    s = set()
    another = ''
    if '(' in a:
        cnt = 0
        for e in a:
            if e == '(':
                cnt += 1
            if cnt > 0:
                another += e
            if e == ')':
                cnt -= 1
    if len(another) != 0:
        a = another
    for e in a:
        if not isnum(e):
            s.add(e)
    for e in s:
        a = a.replace(e, ' ')
    A = np.array(list(map(Fraction, a.split()))).reshape(n, m)
    if is_fraq:
        A = A.astype('object')
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                A[i, j] = Fraction(A[i, j], 1)
    return A


def divCom(X, cols, cnt, s):
    f = False # print matrix only in case we have differences
    for e in range(X.shape[0]):
        g = 0
        first_elem_sign = 0
        for l in range(X.shape[1]):
            if first_elem_sign == 0 and X[e, l] != 0:
                first_elem_sign = 2 * int(X[e, l] > 0) - 1 # поправка на знак первого элемента строчки
            g = abs(gcd(g, X[e, l]))
        if g > 1:
            f = True
            third(X, e + 1, Fraction(first_elem_sign, g))
    if f:
        s += out(X, cnt == cols)
        if cnt == cols:
            cnt = 0
        cnt += 1
    return cnt, s


def make_fraqs(X, cols, cnt, s):
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if X[i, j] == 1:
                break
            if X[i, j] != 0:
                third(X, i + 1, Fraction(1, X[i, j]))
                s += out(X, cnt == cols)
                if cnt == cols:
                    cnt = 0
                cnt += 1
                break
    return s, X


def sort_rows(X):
    main_nums = list()
    f = False
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if X[i, j] != 0:
                main_nums.append(j)
                break
            if len(main_nums) < i:
                main_nums.append(999)
    for i in range(1, len(main_nums)):
        cur = main_nums[i]
        cur_string = X[i].copy()
        j = i - 1
        while j >= 0 and cur < main_nums[j]:
            X[j + 1] = X[j].copy()
            main_nums[j + 1] = main_nums[j]
            j -= 1
            f = True
        main_nums[j + 1] = cur
        X[j + 1] = cur_string
    return f


def improve(X, cols, cnt, s):
    for i in range(X.shape[0] - 1, -1, -1):
        first_non_zero = 0
        for j in range(X.shape[1]):
            if X[i, j] != 0:
                first_non_zero = j
                break
        if first_non_zero == 0:
            continue
        str_num = i
        for j in range(i - 1, -1, -1):
            if X[j, first_non_zero] != 0:
                k = Fraction(X[j, first_non_zero] * X[str_num, first_non_zero],
                gcd(X[j, first_non_zero], X[str_num, first_non_zero]))
                third(X, j + 1, Fraction(k, X[j, first_non_zero]))
                first(X, j + 1, str_num + 1, Fraction(-k, X[str_num, first_non_zero]))
                s += out(X, cnt == cols)
                if cnt == cols:
                    cnt = 0
                cnt += 1
        cnt, s = divCom(X, cols, cnt, s)
    return make_fraqs(X, cols, cnt, s)


def solve(X, cols=3):
    start = 0
    s = out(X, 0)
    cnt = 2
    if X.shape[1] >= 5 and cols > 2:
        cols -= 1
    for j in range(X.shape[1]):
        num = -1
        for i in range(start, X.shape[0]):
            if X[i, j] == 0:
                continue
            elif num == -1:
                num = i
            else:
                k = Fraction(X[i, j] * X[num, j], gcd(X[i, j], X[num, j]))
                third(X, i + 1, Fraction(k, X[i, j]))
                first(X, i + 1, num + 1, Fraction(-k, X[num, j]))
                s += out(X, cnt == cols)
                if cnt == cols:
                    cnt = 0
                cnt += 1
        start += 1
        cnt, s = divCom(X, cols, cnt, s)
    s += out(X, cnt == cols) * sort_rows(X)
    if cnt == cols:
        cnt = 0
    cnt += 1
    return improve(X, cols, cnt, s)


def inv(X):
    A = np.concatenate((X, np.eye(X.shape[0], dtype='object')), axis=1)
    return solve(A)[1][:, A.shape[1] // 2:]