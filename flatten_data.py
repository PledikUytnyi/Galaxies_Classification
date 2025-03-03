import pandas as pd
import numpy as np
import ast
from datetime import datetime
from numpy.lib.stride_tricks import sliding_window_view
import os


def to_list(row):
    return ast.literal_eval(row)


def lambdas_cutoff_mask(row):
    row = np.array(row)
    mask = (row >= 4000) & (row <= 7000)
    return mask


def flux_cutoff(row):
    return np.array(row['flux'])[np.array(row['mask'])]


def smoothing(row):
    sliding_window = sliding_window_view(row, 5)
    return np.mean(sliding_window, axis=1)


def flattened_chunk(chunks):
    i = -1
    for chunk in chunks:
        i = i + 1
        print(f'start reading chunk {i}', datetime.now())
        prepare_chunk_for_training(chunk)


def load_train_data(file_path):
    chunk_size = 10 ** 3
    chunks = pd.read_csv(
        file_path,
        delimiter=' ',
        header=0,
        chunksize=chunk_size,
        usecols=['lambda_rest', 'flux', 'spiral', 'elliptical', 'uncertain']
    )
    flattened_chunk(chunks)


def prepare_chunk_for_training(chunk):
    print('start read csv', datetime.now())
    train_data = chunk
    print('finish csv', datetime.now(), len(train_data))

    print('start preparing columns', datetime.now())

    lambdas = train_data['lambda_rest'].apply(to_list)
    print('finish preparing lambda', datetime.now())
    train_data['flux'] = train_data['flux'].apply(to_list)
    print('finish preparing flux', datetime.now())
    train_data['mask'] = lambdas.apply(lambdas_cutoff_mask)
    print('finish preparing mask', datetime.now())
    train_data['filtered_flux'] = train_data.apply(flux_cutoff, axis=1)
    print('finish filtering flux', datetime.now())
    train_data['filtered_flux_len'] = train_data['filtered_flux'].apply(len)
    print('finish filtering flux len', datetime.now())

    print('finish preparing columns', datetime.now())



    print('start filters', datetime.now())
    filtered_data = train_data[train_data['filtered_flux_len'] >= 2400]
    final_train_data = filtered_data[
        'filtered_flux'].apply(lambda x: x[:2400])


    columns = [f'flux_{i}' for i in range(2400)]
    split = pd.DataFrame(final_train_data.to_list(), columns=columns)
    labels = pd.DataFrame(
        data={
            'elliptical': filtered_data['elliptical'],
            'spiral': filtered_data['spiral'],
            'uncertain': filtered_data['uncertain']
        }
    ).reset_index(drop=True)
    merged = pd.concat([labels, split], axis=1)
    print(merged)
    merged.to_csv('all_data_flattened.csv', mode='a', index=False, sep=' ',header=False)
    print('finish filters', datetime.now())


if os.path.exists('all_data_flattened.csv'):
    os.remove('all_data_flattened.csv')

load_train_data('all_data.csv')
