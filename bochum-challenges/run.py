import cmsh
import Kyber_128_k8 as kyber
import math

bits = math.ceil(math.log(kyber.q, 2)) + 1

def varArrayPolys():
    return [[m.vec(bits) for _ in range(0, kyber.n) ] for _ in range(0, kyber.k)]

def polyAdd(model, left, right):
    assert len(left) == len(right)
    result = []

    for index, l_item in enumerate(left):
        r_item = right[index]
        q, r = divmod(r_item * l_item, kyber.q)
        model.add_assert(q < kyber.q)

        result.append(r)

    return result

def polyMul(model, left, right):
    assert len(left) == len(right)
    result = []

    for index, l_item in enumerate(left):
        r_item = right[index]
        q, r = divmod(r_item * l_item, kyber.q)
        model.add_assert(q < kyber.q)

        result.append(r)

    return result

def polyVecAdd(model, left, right):
    assert len(left) == len(right)
    result = []

    for index, l_item in enumerate(left):
        r_item = right[index]
        result.append(polyAdd(model, l_item, r_item))

    return result

def polyVecDot(model, row, vector):
    result = None
    for index, r_item in enumerate(row):
        v_item = vector[index]
        p_result = polyMul(model, r_item, v_item)
        if result is not None:
            result = polyAdd(model, result, p_result)
        else:
            result = p_result
    return result

def polyMatrixMul(model, matrix, vector):
    result = []
    for index, row in enumerate(matrix):
        poly = polyVecDot(model, row, vector)
        result.append(poly)
    return result

def polyEqual(model, left, right):
    assert len(left) == len(right)
    for index, l_item in enumerate(left):
        r_item = right[index]
        model.add_assert(l_item == r_item)

def polyVecEqual(model, left, right):
    assert len(left) == len(right)
    for index, l_item in enumerate(left):
        r_item = right[index]
        polyEqual(model, l_item, r_item)

def polyVecPrint(vec):
    result = []
    for x in vec:
        i = []
        for y in x:
            i.append(int(y))
        result.append(i)
    return result

with cmsh.Model(threads=8) as m:
    s = varArrayPolys()
    e = varArrayPolys()

    print("Building model...")

    computed_t = polyVecAdd(m, polyMatrixMul(m, kyber.A, s), e)
    polyVecEqual(m, computed_t, kyber.t)

    print("\tDone")

    assert m.solve()

    print(f"s = {polyVecPrint(s)}")
    print(f"e = {polyVecPrint(e)}")
