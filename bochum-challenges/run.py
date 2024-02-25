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
        if model:
            l_item = model.to_vec(l_item, bits)
            r_item = model.to_vec(r_item, bits)

        q, r = divmod(l_item + r_item, kyber.q)

        if model:
            model.add_assert(q < kyber.q)

        result.append(r)

    return result

def polySub(model, left, right):
    assert len(left) == len(right)
    result = []

    for index, l_item in enumerate(left):
        r_item = right[index]
        if model:
            l_item = model.to_vec(l_item, bits)
            r_item = model.to_vec(r_item, bits)

        q, r = divmod(l_item - r_item, kyber.q)

        if model:
            model.add_assert(q < kyber.q)

        result.append(r)

    return result

def polyMul(model, left, right):
    assert len(left) == len(right)
    result = []

    for index, l_item in enumerate(left):
        r_item = right[index]

        if model:
            l_item = model.to_vec(l_item, bits)
            r_item = model.to_vec(r_item, bits)

        q, r = divmod(l_item * r_item, kyber.q)

        if model:
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

def polyVecSub(model, left, right):
    assert len(left) == len(right)
    result = []

    for index, l_item in enumerate(left):
        r_item = right[index]
        result.append(polySub(model, l_item, r_item))

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

def msgPolyPrint(poly):
    bits = []
    q2 = kyber.q // 2
    for bit in poly:
        if bit > q2:
            if (kyber.q - bit) > (bit - q2):
                bit = 0
            elif (kyber.q - bit) < (bit - q2):
                bit = 1
            else:
                assert False
        else:
            if bit > (q2 - bit):
                bit = 1
            elif bit < (q2 - bit):
                bit = 0
            else:
                assert False

        bits.append(bit)

    return "".join(map(str, bits))


with cmsh.Model(threads=8) as m:
    s = varArrayPolys()
    e = varArrayPolys()

    print("Building model...")

    computed_t = polyVecAdd(m, polyMatrixMul(m, kyber.A, s), e)
    polyVecEqual(m, computed_t, kyber.t)

    print("\tDone")

    assert m.solve()

    s = polyVecPrint(s)
    e = polyVecPrint(e)

    print(f"s = {s}")
    print(f"e = {e}")

    data = []

    for part in kyber.ct:
        u, v = part
        noisy = polySub(None, v, polyVecDot(None, s, u))
        bits = msgPolyPrint(noisy)
        first = int(bits[0:8], 2)
        second = int(bits[8:], 2)
        data.append(chr(first))
        data.append(chr(second))

    print(f"data: {data}")
