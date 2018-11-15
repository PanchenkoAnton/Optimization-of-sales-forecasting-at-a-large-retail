from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

def clustering(filename):
    df = pd.read_csv(filename, header=None)
    f = open('/hugedisk/apanchenko/sales_columns.txt', 'r')
    columns = f.read().split(',')
    columns[10] = 'action_price'

    l = []
    for index, row in df.iterrows():
        if row[10] != '\\N':
            l.append(row)
    a = np.array(l)
    small_df = pd.DataFrame(a, index = list(range(len(l))), columns=columns)
    l = []
    for i in range(len(small_df)):
        small_df['action_price'][i] = float(small_df['action_price'][i])    
        l.append(small_df['regular_price'][i] - small_df['action_price'][i])
    small_df['discount'] = l
    for i in range(len(small_df)):
        if small_df['target'][i] == '\\N':
            small_df['target'][i] = 0.0

    small_df = small_df.sort_values(by=['calday'])

    discounts = []
    for index, row in small_df.iterrows():
        discounts.append(row[11])
    prev = discounts[0]
    sales = []
    sales.append(prev)
    iteri = 0
    for i in range(1, len(discounts)):
        if discounts[i] == prev:
            iteri += 1
            continue
        prev = discounts[i]
        sales.append(prev)
    print(iteri, len(sales), sales)

    model = KMeans(n_clusters=3)
    X = np.array(sales)
    X = X.reshape(-1, 1)
    model.fit(X)
    colors = []
    result = model.predict(X)
    for i in range(len(result)):
        if result[i] == 0:
            colors.append('black')
        elif result[i] == 1:
            colors.append('red')
        else:
            colors.append('blue')
    plt.scatter([5] * 45, X, c=colors)
    plt.xlim(0, 10)
    plt.ylim(0, 20)
    plt.xlabel('')
    plt.ylabel('discount')
    plt.show()
    
if __name__ == "__main__":
    mode = input('Press 1 for all-files-clustering and 0 for one-file-clustering')
    if mode == 1:
        for file in glob.glob('/hugedisk/apanchenko/plantmaterial/*.csv'):
            clustering(file)
    else:
        filename = input('Input filename')
        clustering(filename)
        
