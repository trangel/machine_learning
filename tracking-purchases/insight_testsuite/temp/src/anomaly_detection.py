"""
Program that solves the anomaly detection insight problem.
"""
def main(argv):
    """
    Main routine that runs the anomaly detection algorithm.

    ---------------
    Optional arguments:
    batch_log_fname, str, batch_log file name
       Default "batch_log.json"
    stream_log_fname, str, stream_log file name
       Default "stream_log.json"
    output_fname, str, output file name
       Default "flagged_purchases.json"

    ------------
    Objects
    df, pandas dataframe, database of history of purchases. Columns:
        timestamp, str, time of event.
        id, str, user ID.
        amount, str, amount of transaction. 
  
    """
    # Import packages
    import pandas as pd

    # Import user defined functions/objects:
    from user_network import user_network
    from parser import parse_log_file

    # Get file names and command line arguments:
    file_names=get_command_line_arguments(argv)

    # Create a graph datastructure which contains our user network.
    # See doc. in user_network.py
    g = user_network()
    
    # Create an empty database to keep the history of purchases
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

def get_full_file_names(batch_log_fname,stream_log_fname,output_fname):
    """
    Define input/output file names with full paths:

    ------------
    Arguments:
    batch_log_fname, str, name of batch_log file
    stream_log_fname, str, name of stream_log file
    output_log_fname, str, name of output file

    ------------
    Side effects:
    If the "log_output_dirname" is not present, it is created.
    Input files are always in "./log_input/"
    Output files are always in "./log_output/"

    ------------
    Output:
    file_names, dic, contains absolute paths to input and ouput files.
        batch_log_fname: batch_log input file name including full path
        stream_log_fname: stream_log input file name including full path
        output_fname: output file name including full path 
    """
    from os import path,getcwd,makedirs

    # Get input and ouput directory path names:
    current_dirname=getcwd()
    log_input_dirname=path.join(current_dirname,"log_input")
    log_output_dirname=path.join(current_dirname,"log_output")

    # Define absolute path of input/output files
    batch_log_fname=path.join(log_input_dirname,batch_log_fname)
    stream_log_fname=path.join(log_input_dirname,stream_log_fname)
    output_fname=path.join(log_output_dirname,output_fname)

    # Create output directory if not present
    if not path.exists(log_output_dirname):
            makedirs(log_output_dirname)

    # Create a "file_names" dictionary with input/output filenames
    file_names={
    'batch_log_fname':batch_log_fname,
    'stream_log_fname':stream_log_fname,
    'output_fname':output_fname}
    
    return file_names

def get_command_line_arguments(argv):
    """
    Gets command line arguments
    """
    import sys, getopt

    # Set defaults:
    batch_log_fname = 'batch_log.json'
    stream_log_fname = 'stream_log.json'
    output_fname = 'flagged_purchases.json'

    try:
       opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
       pass
    for opt, arg in opts:
       if opt in ('-h', '--help') :
          print( "anomaly_detection.py -i1 <batch_log_fname> -i2 <stream_log_fname> -o <output_fname>")
          sys.exit()
       elif opt == "-i1":
          batch_log_fname = arg
       elif opt == "-i2":
          stream_log_fname = arg
       elif opt == "-o":
          output_fname = arg
    print( "Batch log file is {}".format( batch_log_fname))
    print( "Stream log file is {}".format( stream_log_fname))
    print( "Output file is {}".format( output_fname))

    # Include full path into filename and put them into a 
    # dictionary "file_names":
    file_names=get_full_file_names(batch_log_fname,stream_log_fname,output_fname)
    
    return file_names

if __name__ == "__main__": 
    import sys
    main(sys.argv[1:])

