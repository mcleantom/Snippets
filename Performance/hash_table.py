def a_not_in_b(A, B):
    """
    Find the value in A that is not in B
    """
    H = set(B)
    for item in A:
        if item not in H:
            return item

if __name__=="__main__":
    # The set method in python uses a hash table for O(1) lookup speed versus a list which is O(N)

    import time
    import random

    def naieve_a_not_in_b(A, B):
        for item in A:
            if item not in B:
                return item

    N = 1000000
    L = list(range(N))
    L[-3] = -random.randint(0, 1000000)
    R = list(range(N))

    st = time.time()
    naieve_a_not_in_b(L, R)
    print("elapsed 1", time.time() - st)
    st = time.time()
    a_not_in_b(L, R)
    print("elapsed 2", time.time() - st)