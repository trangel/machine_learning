def main():
    import pandas as pd
    # User defined functions/objects:
    from user_network import user_network
    from parse import parse_log_file

    # Get file names (including path to files):
    #batch_log_fname,stream_log_fname=get_file_names()
    file_names=get_file_names()

    # Create a graph datastructure which contains our user network.
    g = user_network()
    
    # Create an empty database to keep the history of purchases
    #columns=["timestamp","purchase_index","id","amount"]
    columns=["timestamp","id","amount"]
    df=pd.DataFrame(columns=columns)

    # Parse the "batch_log.json" file
    file_type=1
    df=parse_log_file(df,g,file_names,file_type)
    #g.show_social_networks()

    # Parse stream_log_file
    file_type=2
    df=parse_log_file(df,g,file_names,file_type)
    #g.show_social_networks()
    #df.to_csv("df.csv")

def get_file_names():
    from os import path,getcwd,makedirs
    # Get directory path  names:
    current_dirname=getcwd()
    log_input_dirname=path.join(current_dirname,"log_input")
    log_output_dirname=path.join(current_dirname,"log_output")
    batch_log_fname=path.join(log_input_dirname,"batch_log.json")
    stream_log_fname=path.join(log_input_dirname,"stream_log.json")
    flagged_purchases_fname=path.join(log_output_dirname,"flagged_purchases.json")
    #
    if not path.exists(log_output_dirname):
            makedirs(log_output_dirname)


    file_names={'batch_log':batch_log_fname,
    'stream_log':stream_log_fname,
    'flagged_purchases':flagged_purchases_fname}
    
    #return batch_log_fname,stream_log_fname
    return file_names
if __name__ == "__main__": main()

