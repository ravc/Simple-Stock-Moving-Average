from datetime import *
from iexfinance import Share
from multiprocessing.dummy import Pool as ThreadPool
import quandl, getpass

def mavg(stock, N):
    
    qlist = ['WIKI' + '/' + stock]
    
    start = (datetime.today() - timedelta(days=100)).date()
    end = (datetime.today() - timedelta(days=1)).date()
    
    data = quandl.get(qlist, returns='numpy', start_date=start, end_date=end, collapse='daily', order='desc')
        
    #data: date, open, high, low, close

    return sum(data[i][4] for i in range (0,N-1))/N

def savg(stock):
    qlist = ['WIKI' + '/' + stock]
    
    start = (datetime.today() - timedelta(days=100)).date()
    end = (datetime.today() - timedelta(days=1)).date()
    
    data = quandl.get(qlist, returns='numpy', start_date=start, end_date=end, collapse='daily', order='desc')
        
    #data: date, open, high, low, close
    high = sum(data[i][2] for i in range (0,49))/50
    low = sum(data[i][3] for i in range (0,49))/50
    
    return (high + low)/2

def lquote(stock):
    return Share(stock).get_price()

def order(stock, cash):
    print('Bought ' + str(cash) + ' amount of ' + stock + '\n')

def buy_sell(stock):
    if ((mavg(stock,16)>mavg(stock,26))&(lquote(stock)<savg(stock))):
        order(stock, 200)
    elif ((mavg(stock,26)>mavg(stock,16))&(lquote(stock)>savg(stock))):
        order(stock, -200)
    else:
        print(stock + ' no action\n')

quandl.ApiConfig.api_key = 'YOUR API KEY HERE'

stocks = ['YOUR', 'STOCKS', 'HERE']

pool = ThreadPool(2)
pool.map(buy_sell, stocks)

pool.close()
pool.join()
