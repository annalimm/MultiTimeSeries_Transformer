def stock_plot(stock_str, df):
    fig = plt.figure(figsize=(15,10))
    st = fig.suptitle(stock_str, fontsize=20)
    st.set_y(0.92)

    ax1 = fig.add_subplot(211)
    ax1.plot(df['Close'], label='Close Price')
    ax1.set_xticks(range(0, df.shape[0], 1464))
    #ax1.set_xticklabels(df['DateTime'].dt.strftime('%Y-%m-%d').loc[::1464])
    ax1.set_ylabel('Close Price', fontsize=18)
    ax1.legend(loc="upper left", fontsize=12)

    ax2 = fig.add_subplot(212)
    ax2.plot(df['Volume'], label='Volume')
    ax2.set_xticks(range(0, df.shape[0], 1464))
    #ax2.set_xticklabels(df['DateTime'].dt.strftime('%Y-%m-%d').loc[::1464])
    ax2.set_ylabel('Volume', fontsize=18)
    ax2.legend(loc="upper left", fontsize=12)