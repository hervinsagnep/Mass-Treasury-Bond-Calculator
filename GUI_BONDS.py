import tkinter as tk
from tkinter import filedialog
import pandas as pd
import requests
import bs4
from tqdm import tqdm
import datetime
x = datetime.datetime.now()
root = tk.Tk()
root.title("Treasury Bond")
def get_path():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("CSV files", "*.csv"),("all files", "*.*")))
    return root.filename
bond_df = pd.read_csv(get_path())
i = 0
data = []
loop = tqdm(total=len(bond_df), position=0, leave=False)
while i != len(bond_df):
    for index, row in bond_df.iterrows():
        loop.set_description("Loading")
        loop.update(1)
        URL = 'https://www.treasurydirect.gov/BC/SBCPrice'  # Treasury Website
        payload = {"RedemptionDate": f"{str(x.strftime('%m'))}/{str(x.year)}",  # Parameters
                   "btnUpdate.x": "UPDATE",
                   "Series": str(row["Series"]),
                   "Denomination": str(row["Denomination"]),
                   "SerialNumber": str(row['Bond Serial Number']),
                   "IssueDate": str(row['Issue Date']),
                   "ViewPos": "0",
                   "ViewType": "Partial",
                   "Version": "6"
                   }
        r = requests.post(URL, params=payload)  # Making a request
        soup = bs4.BeautifulSoup(r.text, "xml")
        mydivs = soup.findAll("tbody")
        df_list = pd.read_html(r.content)  # Extracting tables
        df = pd.DataFrame(df_list[-1])
        data.append(df_list[-1])
        i += 1
loop.close()
# Combining Tables into DataFrame and making DataFrame neat
bond_data = pd.concat(data)
bond_data.reset_index(drop=True, inplace=True)
del bond_data['Note']
del bond_data['Unnamed: 11']


canvas1 = tk.Canvas(root, width=300, height=300, bg='lightsteelblue2', relief='raised')
canvas1.pack()


def exportCSV():
    global df

    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    bond_data.to_csv(export_file_path, index=None, header=True)
    root.destroy()


saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white',
                             font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=saveAsButton_CSV)

root.mainloop()
