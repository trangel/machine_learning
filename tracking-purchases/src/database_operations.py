"""
Functions dealing with the database of purchases
"""

def db_add_entry(df,newrow):
    """
    Adds a new entry into a pandas dataframe

    --------------
    Arguments:
    df, pandas dataframe, contains history of purchases
    newrow, dictionary, new row to be added to database

    --------------
    Side effects:
    Database is sorted by timestamp, and then by purchase index.

    """
    df.loc[len(df.values)]=newrow
    # Sort by timestamp in descending order, and then by index in ascending order.
    df=df.sort_values(by=['timestamp','purchase_index'],ascending=[False,True])
    #df = df.reset_index(drop=True)
    return df

def db_reduce(df,g):
    """
    Reduces the size of the dataset.
    It keeps only a number of records=(tracked_number_of_purchases+1) per user in the network. 
    The rest of entries are thrown since these are not taken into account to evaluate purchase statistics. 

    --------------
    Arguments:
    df, pandas dataframe, contains history of purchases
    g, dic, user_network class (see user_network.py)

    --------------
    Side effects:
    Database is sorted by timestamp, and then by purchase index.

    """
    import pandas as pd

    # We make an empty dataframe (df2) with same columns as the original one (df) 
    df2=pd.DataFrame(columns=df.columns)
    # cycle over users in user network:
    for uid in g.get_users():
        # Select elements where ID = uid
        df3=df.loc[df['id']==uid]
        # Sort values
        df3=df3.sort_values(by=['timestamp','purchase_index'],ascending=[False,True])
        #df3 = df3.reset_index(drop=True)
        #df3=df3.ix[:,:g.tracked_number_of_purchases+1]

        # Take only the first records
        df3=df3.head(g.tracked_number_of_purchases+1)
        # Append these entries into df2 dataset
        df2=pd.concat([df2, df3],ignore_index=True)

    # Sort by timestamp in descending order, and then by index in ascending order.
    df2=df2.sort_values(by=['timestamp','purchase_index'],ascending=[False,True])
    return df2
