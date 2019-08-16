
# coding: utf-8

# In[1]:


import requests
import bs4
import pandas as pd
from tqdm import tqdm
import datetime
x = datetime.datetime.now()
bond_df = pd.read_csv("") #Directory for Bond Data CSV
i = 0
data = []
loop = tqdm(total = len(bond_df),position=0, leave=False)
while i != len(bond_df):
    for index, row in bond_df.iterrows():
        loop.set_description("Loading")
        loop.update(1)
        URL = 'https://www.treasurydirect.gov/BC/SBCPrice' #Treasury Website
        payload = {"RedemptionDate": f"{str(x.strftime('%m'))}/{str(x.year)}",            #Parameters
                   "btnUpdate.x" : "UPDATE",
                   "Series" : str(row["Series"]),
                   "Denomination" : str(row["Denomination"]),
                   "SerialNumber" : str(row['Bond Serial Number']),
                   "IssueDate" : str(row['Issue Date']),
                   "ViewPos": "0",
                   "ViewType": "Partial",
                   "Version": "6"
                   }
        r = requests.post(URL, params=payload)              #Making a request
        soup = bs4.BeautifulSoup(r.text,"xml")
        mydivs = soup.findAll("tbody")
        df_list = pd.read_html(r.content)                   #Extracting tables
        df = pd.DataFrame(df_list[-1])
        data.append(df_list[-1])
        i += 1
loop.close()
#Combining Tables into DataFrame and making DataFrame neat
bond_data = pd.concat(data)
bond_data.reset_index(drop=True, inplace=True)
del bond_data['Note']
del bond_data['Unnamed: 11']

bond_data.to_csv('') #Name CSV File to your Choice

