import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn')


def split_plot(df_train, df_val, df_test, param = str, title = None, y_lbl = None):

    fig = plt.figure(figsize=(15,12))
    st = fig.suptitle("Data Separation", fontsize=20)
    st.set_y(0.95)

    ax1 = fig.add_subplot(211)
    ax1.plot(np.arange(df_train.shape[0]), df_train[param], label = 'Training data')

    ax1.plot(np.arange(df_train.shape[0],
                    df_train.shape[0]+df_val.shape[0]), df_val[param], label = 'Validation data')

    ax1.plot(np.arange(df_train.shape[0]+df_val.shape[0],
                    df_train.shape[0]+df_val.shape[0]+df_test.shape[0]), df_test[param], label = 'Test data')

    ax1.set_xlabel('Date')
    ax1.set_ylabel(y_lbl)
    ax1.set_title(title, fontsize=16)
    ax1.legend(loc="best", fontsize=12)