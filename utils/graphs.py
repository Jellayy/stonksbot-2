import mplfinance as mpf


def gen_graph(df):
    mc = mpf.make_marketcolors(up='#00a320', down='#ff3334', inherit=True)
    s = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc, gridaxis='horizontal', gridcolor='#454545', gridstyle='solid', edgecolor='#454545', facecolor='#303136')
    saving_params = dict(fname='plot.png', dpi=300, facecolor='#303136')
    # This vwap is a mistake
    # vwap = mpf.make_addplot(df['Volume Weighted'])
    # mpf.plot(df, type='candle', volume=True, addplot=vwap, style=s, savefig=saving_params)
    mpf.plot(df, type='candle', volume=True, style=s, savefig=saving_params)
