import urllib
import re

url_base = "https://www.census.gov/construction/bps/txt/tb2u"
years = ["2016","2017","2018","2019"]
months = ["01","02","03","04","05","06","07",
          "08","09","10","11","12"]
#NOTE: Nov and Dec 2019 do not exist
for y in years:
    for mo in months:
        #print(y + " | " + mo)
        url = url_base + y + mo + ".txt"
        file = urllib.request.urlopen(url)
        out_file = y + mo + ".csv"
        fout = open(out_file, "wt")
        for line in file:
            dd = line.decode("utf-8").strip()
            chunks = re.split('\s\s+', dd)
            fout.write(','.join(chunks) + '\n')
        fout.close()

#url = "https://www.census.gov/construction/bps/txt/tb2u201601.txt"
#file = urllib.request.urlopen(url)
#fout = open('201601_1.csv', "wt")
#for line in file:
#    dd = line.decode("utf-8").strip()
#    chunks = re.split('\s\s+', dd)
#    fout.write(','.join(chunks) + '\n')
#fout.close()