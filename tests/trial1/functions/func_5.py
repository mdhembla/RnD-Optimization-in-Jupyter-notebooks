def func_5(np, isPrime, A, plt):
    X = np.vectorize(isPrime)(A)
    P = A[np.nonzero(X)]
    plt.boxplot(P)
    plt.show()
    return X,P