import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

def scrap():
    page = requests.get("http://networkrepository.com/bn.php")
    soup = BeautifulSoup(page.content, 'html.parser')

    header = [pt.get_text() for pt in soup.find_all("th")[0:-2]]
    header = [pt[:-3] if "\xa0\xa0\xa0" in pt else pt for pt in header]

    names = soup.find_all(class_="btn_gray_sm")
    names = [pt['href'].split('.')[0].split('-',1)[1] for pt in names]

    graphs = soup.find_all(class_="success hrefRow tooltips")
    graphs = [pt.select("td")[1:-2] for pt in graphs]

    df = pd.DataFrame(columns=header)

    for i in range(len(graphs)):
        data = [pt.get_text() for pt in graphs[i]]
        data.insert(0, names[i])
        df = df.append(pd.Series(data, index=header), ignore_index=True)

    return df

df = scrap()
# df.to_excel('bnphp.xlsx')