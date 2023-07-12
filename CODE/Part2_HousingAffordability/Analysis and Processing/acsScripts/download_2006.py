import pandas as pd
import numpy as np
from pandas import Series
from zipfile import ZipFile
import os 
import requests

def download_2010():
    year = 2010
    folderAdd = "./{}".format(year)
    #os.mkdir(folderAdd) 
    try: 
        os.mkdir(folderAdd) 
    except OSError as error: 
        print(error)
    #os.path.join(folderAdd, 'houseEarningData.csv')   
    table = 'B24011'
    sequenceNum = 107
    acsURL = "https://www2.census.gov/programs-surveys/acs/summary_file/{}/data".format(year)

    geoURL_file = acsURL + "/1_year_seq_by_state/UnitedStates/g{}1us.csv".format(year)
    rx = requests.get(geoURL_file,allow_redirects=True)
    open(os.path.join(folderAdd, 'geoFile.csv'), 'wb').write(rx.content)

    acsParentURL = "https://www2.census.gov/programs-surveys/acs/summary_file"

    templateURL_file =  acsURL + "/{}_1yr_SummaryFileTemplates.zip".format(year)
    #https://www2.census.gov/programs-surveys/acs/summary_file/2019/data/2019_1yr_Summary_FileTemplates.zip
    

    filePath = os.path.join(folderAdd,"{}_1yr_Summary_FileTemplates.zip".format(year))
    rx = requests.get(templateURL_file,allow_redirects=True)
    open(filePath, 'wb').write(rx.content)

    miniGeoURL_file = acsParentURL + "/{}/documentation/1_year/geography/Mini_Geofile.xlsx".format(year)
    #https://www2.census.gov/programs-surveys/acs/summary_file/2019/documentation/geography/1_year_Mini_Geo.xlsx

    filePath = os.path.join(folderAdd,'1_year_Mini_Geo.csv')
    rx = requests.get(miniGeoURL_file,allow_redirects=True)
    open(filePath, 'wb').write(rx.content)

    if(year ==2019):
        appendicesURL_file =  acsParentURL + "/{}/documentation/1_year/tech_docs/ACS_{}_SF_1YR_Appendices.xlsx".format(year, year)
        filePath = os.path.join(folderAdd,"ACS_{}_SF_1YR_Appendices.xlsx".format(year))
    else:
        appendicesURL_file =  acsParentURL + "/{}/documentation/1_year/user_tools/Sequence_Number_and_Table_Number_Lookup.xls".format(year, year)
        filePath = os.path.join(folderAdd,"ACS_{}_SF_1YR_Appendices.xls".format(year))
    #https://www2.census.gov/programs-surveys/acs/summary_file/2019/documentation/tech_docs/ACS_2019_SF_1YR_Appendices.xlsx
    if(year >2013):
        tableShellURL_file = acsParentURL + "/{}/documentation/1_year/user_tools/ACS{}_Table_Shells.xlsx".format(year, year)
    else:
        tableShellURL_file = acsParentURL + "/{}/documentation/1_year/user_tools/ACS{}_1-Year_TableShells.xls".format(year, year)
    #https://www2.census.gov/programs-surveys/acs/summary_file/2019/documentation/user_tools/ACS2019_Table_Shells.xlsx

    #not needed this file
    rx = requests.get(appendicesURL_file,allow_redirects=True)
    open(filePath.format(year), 'wb').write(rx.content)
    #get the seq if feasible
    appData = pd.read_excel(filePath)
    #print(appData.head())
    s = appData[appData["Table ID"]=="B24011"]
    if(s.shape[0]>=1):
        sequenceNum = s["Sequence Number"].values[0]
        print(sequenceNum)

    filePath = os.path.join(folderAdd,"ACS{}_Table_Shells.csv".format(year))
    rx = requests.get(tableShellURL_file,allow_redirects=True)
    open(filePath, 'wb').write(rx.content)

    summaryURL_file = acsURL + "/1_year_seq_by_state/UnitedStates/{}1us0{}000.zip".format(year,sequenceNum)
    rx = requests.get(summaryURL_file,allow_redirects=True)
    open(os.path.join(folderAdd, 'summaryFile.zip'), 'wb').write(rx.content)

    # specifying the name of the zip file
    file = os.path.join(folderAdd, "summaryFile.zip")
    
    # open the zip file in read mode
    with ZipFile(file, 'r') as zip: 
        # extract all files to another directory
        zip.extractall(os.path.join(folderAdd,'summaryFile'))

    # specifying the name of the zip file
    file = os.path.join(folderAdd,"{}_1yr_Summary_FileTemplates.zip".format(year))
    
    # open the zip file in read mode
    with ZipFile(file, 'r') as zip: 
        # extract all files to another directory
        zip.extractall(os.path.join(folderAdd,'summaryFileTemplates'))

    summaryFileTemplates = "summaryFileTemplates"
    dest = os.path.join(folderAdd, "summaryFileTemplates")
    listContent = os.listdir(dest)
    if(len(listContent)==1): #and os.path.isdir(listContent[0])
        summaryFileTemplates = summaryFileTemplates + "/" + listContent[0]
        print(summaryFileTemplates)

    #read both geo and seq file
    fileName = os.path.join(folderAdd, "{}/{}_SFGeoFileTemplate.xls".format(summaryFileTemplates,year))
    geoFileNames = pd.read_excel(fileName)

    fileName = os.path.join(folderAdd,"{}/Seq{}.xls".format(summaryFileTemplates,sequenceNum))
    seqFileNames = pd.read_excel(fileName) 
    seqFileNames.head()

    fileName = os.path.join(folderAdd,"summaryFile/e{}1us0{:0>3d}000.txt".format(year, sequenceNum))
    acsData = pd.read_csv(fileName, header=None, names=seqFileNames.columns)
    acsData.head()

    #drop all variables which are not relevant
    varNames = ['LOGRECNO'] + list(acsData.filter(regex='B24011.*'))
    acsData = acsData[varNames]

    #df_sheet_all = pd.read_excel('sample.xlsx', sheet_name=None)
    geoData = pd.read_csv(os.path.join(folderAdd,"geoFile.csv"), header=None, names=geoFileNames.columns, encoding='gbk')
    geoData.head()

    #get only data with 310 summary level. 
    #310-> metropolitan statistical area/micropolitan statistical area
    geoData = geoData.loc[geoData.SUMLEVEL==310]
    geoData.reset_index(drop=True,inplace=True)

    geoData['CBSACode'] = geoData['GEOID'].apply(lambda s: s.split('US')[1])

    geoData = geoData[['LOGRECNO','NAME','CBSACode']]
    geoData.dropna(axis=0, subset=['CBSACode'], inplace=True)
    geoData['CBSACode'] = geoData['CBSACode'].astype('int')
    geoData.reset_index(drop=True,inplace=True)
    geoData.head()

    #merge ACS and geoData
    acsEarning = acsData.merge(geoData, on = 'LOGRECNO')

    acsEarning.to_csv(os.path.join(folderAdd,'acsEarning.csv'), index=False)
    return acsEarning