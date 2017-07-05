"""
Routines to parse input files.
This call routines to fill in the purchases database and to build the network of users.
"""

def parse_log_file(df,g,file_names,file_type,purchase_index):
    """
    Routine that parses an input "log_file".

    ------------
    Arguments:
    df, pandas dataframe, dataframe of purchase history.
    g, dic, users network. 
        See details in user_network.py
    purchase_index, int, keeps track of purchase event ordering
    file_names, dic, input/output file names. Contains:
          batch_log_fname, str, full path to batch_log file
          stream_log_fname, str, full path to stream_log file
          output_fname, str, full path to output file
    file_type: int, 1 for batch_log_file type
                    2 for stream_log_file type

    ------------
    Side effects:
    Updates the purchases dataframe.
    Updates the users network.
    Calls routines to flag a purchase as anomalous. 

    """
    import numpy as np
    import pandas as pd
    from ast import literal_eval  
    from json import dumps
    # My own routines:
    from purchase_statistics import get_purchase_statistics
    from database_operations import db_add_entry,db_reduce

    # Initialize db_size with the purchase_index
    db_size=purchase_index

    # Check that arguments are correct: 
    if ( (file_type != 1) & ( file_type != 2 ) ):
        print("Error found in parse_log_file, file_type should be 1 or 2")
        exit(1)

    # Input/Output file names:
    if ( file_type == 1 ):
        input_file = file_names['batch_log_fname']
    elif ( file_type == 2 ):
        input_file = file_names['stream_log_fname']
        output_file = file_names['output_fname']
        f_out = open(output_file,"w")
    f_in = open(input_file,"r")

    if ( file_type == 1 ):
        # Read first line of the file, and store "D", "T" values:
        line = f_in.readline()
        # Use literal_eval to convert string to dictionary,
        # This is safer than using eval. As its own docs say:
        # help(ast.literal_eval)
        # Help on function literal_eval in module ast:
        #     literal_eval(node_or_string)
        #     Safely evaluate an expression node or a string containing a Python
        #     expression.  The string or node provided may only consist of the following
        #     Python literal structures: strings, numbers, tuples, lists, dicts, booleans, and None.
        dic=literal_eval(line)
        g.network_degree=int(dic['D'])
        g.tracked_number_of_purchases=int(dic['T'])

    # Read rest of the file and construct network
    # Iterate on lines in input file:
    for line in f_in.readlines():
        try:
            dic=literal_eval(line)
        except:
            # If erroneous file, skip
            continue
        # Extract event_type and timestamp into variables:
        event_type=dic['event_type']
        timestamp=dic['timestamp']
        # Add a new friend if event_type = befriend
        if ( event_type == 'befriend' ):
            id1=str(dic['id1'])
            id2=str(dic['id2'])
            g.add_friend(id1,id2)
            g.update_social_network()
        # Remove a friend if event_type = unfriend
        elif( event_type == 'unfriend' ):
            id1=str(dic['id1'])
            id2=str(dic['id2'])
            g.del_friend(id1,id2)
            g.update_social_network()
        # Purchase event:
        elif ( event_type == 'purchase' ):
            purchase_index=purchase_index+1
            db_size=db_size+1
            uid=str(dic['id'])
            amount=np.float(dic['amount'])
            # If user is not in network, add it:
            g.if_notpresent_add_user(uid)
            # Add new row to dataset:
            newrow=[purchase_index,timestamp,uid,amount]
            df=db_add_entry(df,newrow)
            # If dataset is getting big, reduce its size:
            if ( (g.num_users*g.tracked_number_of_purchases*2) < db_size ):
                df=db_reduce(df,g)
                db_size=len(df)

            # Update purchase statistics:
            if ( file_type == 2 ):
                purchase={"id": uid, "amount": amount}
                # Evaluate if purchase is anomalous
                purchase_stats=get_purchase_statistics(purchase,g,df)
                if ( purchase_stats['anomalous'] ):
                    # If anomalous, write an entry into output file:
                    flagged_purchase={"event_type": "purchase",
                    "timestamp": timestamp,
                    "id": uid,
                    "amount": str(amount),
                    "mean": purchase_stats['mean'],
                    "sd": purchase_stats['sd']}
                    f_out.write("{}\n".format(dumps(flagged_purchase)))
                    #
    # Close input/output files
    f_in.close()
    if ( file_type == 2 ):
        f_out.close()

    # Return updated database of purchases
    return df,purchase_index
