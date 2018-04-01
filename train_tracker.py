from train_tracker.scrape_raildar import scrape_raildar
from train_tracker.utils import *
from train_tracker.convert_raw import *
from train_tracker.stats import *
import train_tracker
import inspect
import sys

################################################################################
#
# MAIN TRAIN TRACKER CODE
#
#
#
#
#
#
#
#ascii_train_tracker()
################################################################################

# Read command line arguments
run_command = read_arg(sys.argv)
 
# Get current path to package
path = os.path.dirname(os.path.dirname(inspect.getfile(train_tracker)))

# Read in config files
config = read_config("config.txt", path)
dates = read_config("dates.txt", path)  

################################################################################
# 
# Scrape data from raildar
#
################################################################################     

if run_command == "scrape":  
    
    print "---------------------------------------------------------------------\n"
    print "Scraping https://raildar.co.uk website for all train data in " + config['month']                                                 
    out_times = [config["out"]][0].split(",")
    return_times = [config["return"]][0].split(",")
    for i in xrange(len(out_times)):
        scrape_raildar(config, out_times[i],return_times[i],path) 
        print "Completed < ",
        print i + 1,
        print "/ ",
        print len(out_times),
        print " >\n"

    print "\nData scraping completed!"
    print "\n---------------------------------------------------------------------"

################################################################################
#
# Convert raw html data into a pandas dataframe containing delayed trains
#
################################################################################    

if run_command == "convert_raw":
    print "---------------------------------------------------------------------\n"
    delays = convert_raw(dates,config,path)
    os.chdir(path + "/output")
    delays.to_csv(config["month"].split(" ")[0].lower() + "_delays.csv")
    print delays

else:
	print "Please pass a command line argument"
	exit()

