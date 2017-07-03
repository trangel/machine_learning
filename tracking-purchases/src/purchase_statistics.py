from user_network import user_network as user_network
import pandas as pd

def get_purchase_statistics(purchase,g,df):
    """
    Gets purchase statistics based on the history of purchases.

    -----------
    Arguments
    purchase, dic, dictionary containing details of the purchase:
        user, str, user ID
        amount, str, amount in purchase


    g, dic, dictionary containing the user network.
        For details, see user_network.py

    df, dataframe, pandas dataframe containing the history of purchases.

    --------------
    Output
    purchase_stats, dict, contains:
        mean, numpy float, statistical mean for the history of purchases.
        std, numpy float, standard deviation for the history of purchases.
        anomalous, logical, whether or not the purchase if flagged as anomalous. 
    """
    # Finds if a purchase is anomalous
    user=purchase['id']
    amount=purchase['amount']

    # Get social network for that user:
    social_network=g.get_user(user).social_network

    purchase_stats={}
    if ( len(social_network) == 0 ):
        purchase_stats['anomalous':False]
        return purchase_stats
    else:
        purchase_history=\
        df.loc[df['id'].isin(social_network)].head(g.tracked_number_of_purchases)['amount'].values
        if ( len(purchase_history) < 2 ):
            purchase_stats['anomalous':False]
            return purchase_stats
        else:
            return eval_purchase(purchase_history,amount)

def eval_purchase(purchase_history,amount):
    """
    Evaluates the statistical mean and average for the history of purchases.
    
    --------------
    Arguments
    purchase_history, numpy array, history of purchases.
    amount, numpy float, amount of current purchase.

    --------------
    Output
    purchase_stats, dict, contains:
        mean, numpy float, statistical mean for the history of purchases.
        std, numpy float, standard deviation for the history of purchases.
        anomalous, logical, whether or not the purchase if flagged as anomalous. 
    """
    import numpy as np
    # Get mean and standard deviaton:
    # Several methods can get the mean and standard deviation:
    # is anomalous if amount > mean + (3*sd)
    #
    # Mean value:
    # I could implement this as: mean=ll.sum()/len(ll), but I prefer to use libraries to improve the efficiency of the code:
    mean=np.mean(purchase_history)
    # Standard deviation= sd=np.sqrt( sum((ll-mean)**2)/len(ll))
    sd=np.std(purchase_history)
    if ( amount > ( mean + 3.0*sd) ):
        anomalous=True
    else:
        anomalous=False
    purchase_stats={'mean': truncate(mean),'sd': truncate(sd),'anomalous':anomalous} 
    return purchase_stats

def truncate(n):
    """
    Truncates a number to 2 decimals

    _____________
    Argument
    n, float, number
    
    -------------
    Output
    Returns a string with the number truncate to two decimals.
    """
    from math import floor
    nn=floor((n) * 10**2) / 10**2
    return "%.2f" % (nn) 
