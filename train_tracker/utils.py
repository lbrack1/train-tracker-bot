import os
import sys

################################################################################
#
# TRAIN TRACKER UTILS
#
################################################################################

# Function to read in config file
def read_config(filestr, path):
        
    # Change to config directory
    os.chdir(path + "/config")
    
    config = {}
    # Read config file
    with open(filestr) as f: 
        for line in f:
            x = line.rstrip('\n')
            (key, val) = x.split('=')
            config[str(key)] = val
       
    return config
    
# Function to read command line arguments 
def read_arg(args):
    
    if len(args) == 1:
        print "Error: No command line arguments passed. Run with -help to view options"
        sys.exit()
    
    if len(args) == 2:
        
        if args[1] == "-help":
            print "Don't fear! Help is here.\n"
            print "-scrape   Run to convert scrape delayed trains data using values specified in config.txt"
            print "-convert_raw  Run to convert raw scraped html to readable csv data"
            sys.exit()
            
        if args[1] == "-scrape":
            print "Running Train Tracker data scraper \n"
            run_command = "scrape"
            return run_command
        
        if args[1] == "-convert_raw":
            print "Running Train Tracker raw data converter \n"
            run_command = "convert_raw"
            return run_command
            
        else: 
            print "Error no recognised command line arguments passed. Run with -help to view options"
            sys.exit()
    
    if len(args) > 2:
        print "Error: Too many command line arguments passed. Run with -help to view options"
        sys.exit()
