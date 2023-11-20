import numpy as np


def df_split(df):
    
    # we maintain chronological order for time-series
    train_samples = int(len(df) * 0.8)
    val_samples = int(len(df) * 0.1)

    df_train = df[:train_samples]
    df_val = df[train_samples: train_samples + val_samples]
    df_test = df[train_samples + val_samples:]

    # we can remove date column, because the time information is now embedded in a different form
    df_train = df_train.loc[:, df_train.columns != 'Time']
    df_val = df_val.loc[:, df_val.columns != 'Time']
    df_test = df_test.loc[:, df_test.columns != 'Time']

    print('Train df shape: {}'.format(df_train.shape))
    print('Val df shape: {}'.format(df_val.shape))
    print('Test df shape: {}'.format(df_test.shape))
    return df_train, df_val, df_test

    # # convert pd colums inro arrays for Transformer
    # arr_train = df_train.values
    # arr_val = df_val.values
    # arr_test = df_test.values

    # print('Train arr shape: {}'.format(arr_train.shape))
    # print('Test arr shape: {}'.format(arr_val.shape))
    # print('Val arr shape: {}'.format(arr_test.shape))
    # return df_train, df_val, df_test, arr_train, arr_val, arr_test
    
    
def chunks(seq_len, df_train, df_val, df_test, target_col, step, n_pred):

    df_train = df_train.values
    df_val = df_val.values
    df_test = df_test. values

    X_train, y_train = [], []
    # we use all colums for training. split data by subsets with n = "seq_len" rows(timesteps) and move by step = 1 
    # we use n = seq_len-1 parametrs for training and i+1-th parametr as a target (could be optional)
    for i in range(seq_len, len(df_train), step):
        X_train.append(df_train[i-seq_len:i])
        # we use only target_col columns as a target
        y_train.append(df_train[i:i+n_pred, target_col])
    X_train, y_train = np.array(X_train), np.array(y_train)
    
    
    X_val, y_val = [], []
    for i in range(seq_len, len(df_val), step):
        X_val.append(df_val[i-seq_len:i])
        y_val.append(df_val[i:i+n_pred, target_col])
    X_val, y_val = np.array(X_val), np.array(y_val)


    X_test, y_test = [], []
    for i in range(seq_len, len(df_test), step):
        X_test.append(df_test[i-seq_len:i])
        y_test.append(df_test[i:i+n_pred, target_col])
    X_test, y_test = np.array(X_test), np.array(y_test)

    print("Train chunks set shape: ", X_train.shape, y_train.shape)
    print("Val chunks set shape: ", X_val.shape, y_val.shape)
    print("Test chunks set shape: ", X_test.shape, y_test.shape)
    return(X_train, y_train, X_val, y_val, X_test, y_test)