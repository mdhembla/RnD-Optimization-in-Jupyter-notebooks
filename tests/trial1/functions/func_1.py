def func_1():
    #Q1
    import numpy as np

    A = np.arange(1, 101)
    R = A.reshape((10, 10))

    def isPrime(n):
      if n < 2:
        return 0
      else:
        for i in range(2, int(np.sqrt(n)) + 1):
          if n % i == 0:
            return 0
        return 1

    B = np.vectorize(isPrime)(R)

    C = np.concatenate((R,B))
    return C,B,A,isPrime,R