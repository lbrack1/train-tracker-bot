import pandas as pd
from bs4 import BeautifulSoup
import functools
import os
from datetime import time

################################################################################
#
# PARSE HTML INTO PANDAS DATAFRAME
#
################################################################################

def convert_raw(dates,config,path):
    
    # Make an empty df with dates as index
    month = config['month'].split(" ")[0].lower()
    date_list = dates[month].split(",")
    month_df = pd.DataFrame(date_list, columns = ["Day \ Time"]).set_index("Day \ Time")

    ####################################################
    # Function to read in html file and return dataframe
    ####################################################
    def html_to_dataframe(file, month_df):
    
        #Import raw html file and find all tables
        raw_html = BeautifulSoup(open(file), "lxml")
        all_tables = raw_html.find_all('table')
    
        # Number of tables in html
        num_tables = len(all_tables)
    
        # Dataframe collection
        dataframe_collection = {}
    
        # Loop over number of html tables
        for i in xrange(num_tables):    
            table_df = pd.read_html(str(all_tables[i]))[0].set_index("Day \ Time")
            filestring = file + str(i)
            joined_df = month_df.join(table_df)
            dataframe_collection[filestring] = joined_df
    
        merge = functools.partial(pd.merge, left_index = True, right_index = True)
        all_data_df = functools.reduce(merge, dataframe_collection.values())
        return all_data_df

    # Read in html file names (formalise naming convention?)  
    file_list = []  
    file_list = filter(lambda x: x.endswith('.html'), os.listdir(path + "/raw")) 
    dataframe_collection = {}

    # Loop over html files and convert to html data to dataframe
    os.chdir(path + "/raw")
    for file in file_list:    
        function_df = html_to_dataframe(file, month_df)
        dataframe_collection[file] = function_df

    # Merge each html file df into alldataraw df
    merge = functools.partial(pd.merge, left_index = True, right_index = True)
    all_data_raw = functools.reduce(merge, dataframe_collection.values())

# Clean column header string
    all_data_raw.columns = all_data_raw.columns.str.replace("[ TL]", "")
    all_data_raw.columns = all_data_raw.columns.str.replace("[_x]","")
    all_data_raw.columns = all_data_raw.columns.str.replace("[_y]","")

    # Column header string to datatime
    all_data_raw.columns = pd.to_datetime(all_data_raw.columns,errors='coerce')
    all_data_raw.columns = all_data_raw.columns.strftime('%H:%M')

    # Sort columns by datetime 
    sorted_df = all_data_raw.sort_index(1)

    # Function to parse each element of df and return info if train is delayed
    # takes X which is pandas series
    def getDelays(x):
    # Loop over rows in x pandas series
        for i in xrange(x.size):
        
        # check each row is string and train not cancelled
            if type(x[i]) is str and "Cancelled" not in x[i]:
            
            # Split to take care of data format
                tokens = x[i].split("  ")
            
                # Ensure correct number of items outputted from split
                if len(tokens) == 2:
                    delayMag = int(tokens[0])
                    arriveTime = tokens[1].replace("(","").replace(")","")
                
                    # Return trains delayed by 15 minutes or more
                    if delayMag > 14:
                        delayList = [x.index[i],delayMag,x.name, arriveTime]
                        return delayList

    # Call function to return delayed trains                
    x = sorted_df.apply(getDelays).dropna()

    # Reformat df and take care of datetime objects
    delays = pd.DataFrame.from_items(zip(x.index, x.values)).T
    delays.columns = ['date', 'delay', 'departure time', 'actual arrival time'] 
    delays = delays.set_index('date')
    delays["delay"] = pd.to_timedelta(delays["delay"],unit='m')
    delays["actual arrival time"] = pd.to_datetime(delays["actual arrival time"],errors='coerce')
    delays["departure time"] = pd.to_datetime(delays["departure time"],errors='coerce')
    delays["scheduled arrival time"] = delays["actual arrival time"] - delays["delay"]
    delays["delay"] = delays["delay"] / pd.Timedelta('1 minute')
    delays["actual arrival time"] = delays["actual arrival time"].apply(lambda x: x.strftime('%H:%M'))
    delays["departure time"] = delays["departure time"].apply(lambda x: x.strftime('%H:%M'))
    delays["scheduled arrival time"] = delays["scheduled arrival time"].apply(lambda x: x.strftime('%H:%M'))
    delays = delays.drop_duplicates(keep="first")
    return delays

