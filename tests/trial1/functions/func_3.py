def func_3(df):
    #Q3
    import matplotlib.pyplot as plt

    perc = df['Origin'].value_counts(normalize=True) * 100
    perc.plot(kind='pie')
    return perc