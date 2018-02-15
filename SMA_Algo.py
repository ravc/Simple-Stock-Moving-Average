from datetime import *
from iexfinance import Share
from multiprocessing.dummy import Pool as ThreadPool
import quandl, getpass

def mavg(stock, N):
    
    qlist = ['WIKI' + '/' + stock]
    
    #the start and end date do not take into account non trading days so adjust accordingly
    start = (datetime.today() - timedelta(days=100)).date()
    end = (datetime.today() - timedelta(days=1)).date()
    
    #this should only return data from the valid trading days
    data = quandl.get(qlist, returns='numpy', start_date=start, end_date=end, collapse='daily', order='desc')
        
    #the data received is as follows: date, open, high, low, close
    
    #returns the average
    return sum(data[i][4] for i in range (0,N-1))/N

def savg(stock): #this is the similar as above except it is for a 50 day average that is used only for extra validation
    qlist = ['WIKI' + '/' + stock]
    
    start = (datetime.today() - timedelta(days=100)).date()
    end = (datetime.today() - timedelta(days=1)).date()
    
    data = quandl.get(qlist, returns='numpy', start_date=start, end_date=end, collapse='daily', order='desc')
        
    #data: date, open, high, low, close
    
    #this calculates the average price of the stock over the last 50 days which should be fairly stable
    high = sum(data[i][2] for i in range (0,49))/50
    low = sum(data[i][3] for i in range (0,49))/50
    
    return (high + low)/2

def lquote(stock):
    #this gets the current stock price
    return Share(stock).get_price()

def order(stock, cash): 
    #if price is negative it means you sold stock and positive means bought
    print('Bought ' + str(cash) + ' amount of ' + stock + '\n')

def buy_sell(stock):
    if ((mavg(stock,16)>mavg(stock,26))&(lquote(stock)<savg(stock))):
        
        #the cash value used is arbitrary, you would need to use an amount that is valid
        order(stock, 200) 
    elif ((mavg(stock,26)>mavg(stock,16))&(lquote(stock)>savg(stock))):
        
        #the cash value used is arbitrary, you would need to use an amount that is valid
        order(stock, -200)
    else:
        print(stock + ' no action\n')

quandl.ApiConfig.api_key = 'YOUR API KEY HERE'

stocks = ['YOUR', 'STOCKS', 'HERE']

#threads are being used to do as many transactions at the same time as possible. 
#the limiting factor for this is currently quandl.

pool = ThreadPool(2) #you can increase the ThreadPool if you have a paid quandl account
pool.map(buy_sell, stocks)

pool.close()
pool.join()
