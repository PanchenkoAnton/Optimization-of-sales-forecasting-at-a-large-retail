import pandas as pd
import csv
import gc

chunksize = 10 ** 5
i = 0
for chunk_df in pd.read_csv('/hugedisk/apanchenko/sales_w2.csv', chunksize=chunksize, header=None):
    chunk_df.columns = ['plant', 'material', 'cat_id', 'subcat_id', 'group_id', 'calday',
                       'matrix_type', 'target', 'is_action', 'regular_price', 'action_price']
    for index, row in chunk_df.iterrows():
        csv_file = open('/hugedisk/apanchenko/plantmaterial/plant%dmaterial%d.csv' % (row[0], row[1]), 'a')
        writer = csv.writer(csv_file)
        writer.writerow(row)
        csv_file.close()
          
    del chunk_df
    gc.collect()
    
    i += 1
    print('%d%% DONE. The #%d chunk of 4817 was processed! To be continued... ' % (i / 4817 * 100, i))
