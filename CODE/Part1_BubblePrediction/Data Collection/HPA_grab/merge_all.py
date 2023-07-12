import pandas as pd
import glob

rm = ["Middle Atlantic","Midwest","East North Central D","West North Central D",
      "South","South Atlantic","East South Central D","West South Central D","West",
      "Mountain","Pacific"]
mo_num_to_name = {"01":"January","02":"February","03":"March","04":"April","05":"May",
                  "06":"June","07":"July","08":"August","09":"September","10":"October",
                  "11":"November","12":"December"}
all_yr_mo = pd.DataFrame()
#For all .csv in dir:
for file in glob.glob('*.csv'):
    #Get mo and year
    mo = mo_num_to_name[file[4:6]]
    yr = file[:4]

    #Skip header info
    df = pd.read_csv(file, skiprows=16, header=None)
    #Only want state and total HPA info
    df = df.iloc[:,:2]
    #Remove rows where not a state
    df = df.loc[~df.iloc[:,0].isin(rm)]
    #Insert other columns for format
    df['year'] = yr
    df['mo'] = mo
    #Reorder
    cols=[0,"year","mo",1]
    df = df.loc[:,cols]
    
    all_yr_mo = all_yr_mo.append(df)
#Save to csv
#TODO: Make sure this file doesn't already exist
all_yr_mo.to_csv("all_yr_mo.csv")
    