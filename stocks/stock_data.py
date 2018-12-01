from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import matplotlib.pyplot as plt 
from retrying import retry



def get_sharpe_ratio(ticker, risk_free_ticker):
    """ Get the sharpe ratio for a ticker
    
    Arguments:
        risk_free_ticker {list} -- price data from a risk free stock
        ticker {list} -- price data from a ticker
    
    Returns:
        int -- sharpe ratio
    """


    plt.plot(ticker, label='ticker')
    plt.plot(risk_free_ticker, label='risk free ticker')
    plt.legend()
    plt.show()

    sizes = [len(risk_free_ticker), len(ticker)]

    arr_length = min(sizes)

    # FOR ^IRX where return = yearly return
    daily_return_risk_free = np.array([(1+(x/100))**(1/250)-1 for x in risk_free_ticker])
    daily_return_risk_free = daily_return_risk_free[0:arr_length]

    # For a normal ticker with price growth
    # daily_return_risk_free = np.array([0])
    # for i in range(1,arr_length):
    #     daily_return_risk_free = np.append(daily_return_risk_free,[(risk_free_ticker[i]-risk_free_ticker[i-1])/risk_free_ticker[i-1]])

    daily_return_ticker = np.array([0])
    for i in range(1,arr_length):
        daily_return_ticker = np.append(daily_return_ticker,[(ticker[i]-ticker[i-1])/ticker[i-1]])

    excess_return = daily_return_ticker - daily_return_risk_free

    # Calculate Sharpe Ratio
    sharpe_ticker_daily = np.mean(excess_return)/np.std(excess_return)
    sharpeRatio = sharpe_ticker_daily*np.sqrt(250)

    return sharpeRatio

@retry(retry_on_exception=ValueError, wait_fixed=2000)
def get_stock_data(ticker, start, end):
    """ Get stock data between start and end
    
    Arguments:
        ticker {str} -- Ticker you want data for
        start {str} -- Start date formatted like "2018-10-30"
        end {str} -- End date formatted like "2018-10-30"
    
    Returns:
        [pandas dataframe] -- Stock data
    """

    yf.pdr_override() # God bless whoever is maintaining this

    data = pdr.get_data_yahoo(ticker, start=start, end=end)

    return data


if __name__ == '__main__':
    yf.pdr_override() # God bless whoever is maintaining this

    itot_data = list(get_stock_data("ITOT", "2005-01-01", "2018-10-30")['Adj Close'])
    irx_data = list(get_stock_data("^IRX", "2005-01-01", "2018-10-30")['Adj Close'])
    savings_acct = [0.02 for i in range(len(itot_data))]

    sharpe = get_sharpe_ratio(itot_data, savings_acct)

    print(sharpe)