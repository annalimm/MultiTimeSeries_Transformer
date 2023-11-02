def df_split(df):
    # we maintain chronological order for time-series
    train_samples = int(len(df) * 0.8)
    val_samples = int(len(df) * 0.1)

    df_train = df[:train_samples]
    df_val = df[train_samples: train_samples + val_samples]
    df_test = df[train_samples + val_samples:]

    # we csn remove date column, because the time information is now embedded in a different form  
    df_train = df_train.loc[:, df_train.columns != 'Time']
    df_val = df_val.loc[:, df_val.columns != 'Time']
    df_test = df_test.loc[:, df_test.columns != 'Time']

    print('Train df shape: {}'.format(df_train.shape))
    print('Val df shape: {}'.format(df_val.shape))
    print('Test df shape: {}'.format(df_test.shape))
    return df_train, df_val, df_test