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
    import pandas as pd
 
    df2=pd.DataFrame(columns=df.columns)
    for uid in g.get_users():
        df3=df.loc[df['id']==uid]
        df3=df3.sort_values(by=['timestamp','purchase_index'],ascending=[False,True])
        #df3 = df3.reset_index(drop=True)
        #df3=df3.ix[:,:g.tracked_number_of_purchases+1]
        df3=df3.head(g.tracked_number_of_purchases+1)
        df2=pd.concat([df2, df3],ignore_index=True)
    # Sort by timestamp in descending order, and then by index in ascending order.
    df2=df2.sort_values(by=['timestamp','purchase_index'],ascending=[False,True])
    return df2
