def func_2():
    #Q2
    import pandas as pd

    csv = "https://drive.google.com/uc?id=1lSSw_vZ63uz34wX566c0L3FL7H4AB7X1"
    df = pd.read_csv(csv)

    df['Gender'] = 'male'
    for i in df.index:
      if df["User full name"][i] == 'P':
        df['Gender'][i] = 'female'

    no_of_actions = df['User full name'].value_counts()
    print(no_of_actions)

    df = df.drop(columns=['Description'])
    print(df.head(3))
    print(df.tail(7))

    print(df[df['Gender'] == 'male'])
    return df,no_of_actions,csv