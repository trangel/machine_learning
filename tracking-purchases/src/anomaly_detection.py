def main():
    """
    Main routine that runs the anomaly detection algorithm.
    """
    # Import packages
    import pandas as pd

    # Import user defined functions/objects:
    from user_network import user_network
    from parse import parse_log_file

    # Get file names (including path to files) into a 
    # dictionary "file_names" defined in "get_file_names()"
    file_names=get_file_names()

    # Create a graph datastructure which contains our user network.
    # See doc. in user_network.py
    g = user_network()
    
    # Create an empty database to keep the history of purchases
    #columns=["timestamp","purchase_index","id","amount"]
    columns=["timestamp","id","amount"]
    df=pd.DataFrame(columns=columns)

    # Parse the "batch_log.json" file
    file_type=1;
    df=parse_log_file(df,g,file_names,file_type)
    #g.show_social_networks()

    # Parse stream_log_file
    file_type=2
    df=parse_log_file(df,g,file_names,file_type)
    #g.show_social_networks()
    #df.to_csv("df.csv")

def get_file_names():
    """
    Define input/output file names.

    ------------
    Side effects:
    If the "log_output_dirname" is not present, it is created.

    ------------
    Output:
    file_names, dic, contains absolute paths to input and ouput files.
        batch_log: path to "bath_log.json" input file 
        stream_log: path to "stream_log.json" input file 
        flagged_purchases: path to "flagged_purchases.json" output file 
    """
    from os import path,getcwd,makedirs

    # Get input and ouput directory path names:
    current_dirname=getcwd()
    log_input_dirname=path.join(current_dirname,"log_input")
    log_output_dirname=path.join(current_dirname,"log_output")

    # Define absolute path of input/output files
    batch_log_fname=path.join(log_input_dirname,"batch_log.json")
    stream_log_fname=path.join(log_input_dirname,"stream_log.json")
    flagged_purchases_fname=path.join(log_output_dirname,"flagged_purchases.json")

    # Create output directory if not present
    if not path.exists(log_output_dirname):
            makedirs(log_output_dirname)

    # Create a "file_names" dictionary with input/output filenames
    file_names={'batch_log':batch_log_fname,
    'stream_log':stream_log_fname,
    'flagged_purchases':flagged_purchases_fname}
    
    return file_names

if __name__ == "__main__": main()

