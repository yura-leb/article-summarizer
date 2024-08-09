import bibtexparser
import pandas as pd
from tqdm import tqdm
import digest as dg
import requests
import json
import os
from sys import argv

def make_star(ranking):
    rank = int(ranking[-1])
    if rank == 5:
        return "green"
    elif rank >= 3:
        return "yellow"
    else:
        return "red"
    
def make_math(math):
    if math == 1:
        return "yes"
    else:
        return "no"
    
months = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",    
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}


if __name__ == "__main__":
    
    # folder must be formatted as Month_Year. Example: June_2024
    if len(argv) == 2:
        folder = argv[1]
    else:
        folder = input("Enter folder name: formatted like 'June_2024'")
    month, year = folder.split('_')

    with open(f'data/{folder}/nlp.bib', 'r') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    if "urldate" in bib_database.entries[0].keys():
        df = pd.DataFrame(bib_database.entries)[['title', 'url', 'urldate', 'month', 'year', 'priority', 'ranking', 'groups']]
    else:
        df = pd.DataFrame(bib_database.entries)[['title', 'eprint', 'month', 'year', 'priority', 'ranking', 'groups']]
    
    df['title'] = df['title'].str.replace('}|{', '', regex=True)

    if "url" not in df.columns: 
        df["url"] = "https://arxiv.org/pdf/" + df['eprint']
        df["urldate"] = df["month"] + " " + df["year"]
    else:
        df['url'] = df['url'].str.replace('/abs/', '/pdf/', regex=True)
    
    subdf = df.loc[(df['month']==month)&(df['year']==year)&(df['ranking'].notna())&(df['priority'].notna())]
    parse_result = []

    pc = dg.PromptsContainer()
    for i, row in tqdm(subdf[subdf["ranking"].notna()].iterrows()):
        title = row["title"]
        print(i)
        print(row['title'], row['url'], row['urldate'], row['priority'], row['ranking'])
        r = requests.get(row['url'], )
        file_name = f'data/{folder}/{title}.pdf'
        with open(file_name, 'wb') as output:
            output.write(r.content)
        result = pc.parse_article_json(file_name)
        result["title"] = title
        result["ml"] = result["datasets_models"].find("Models:") != -1
        result["ds"] = result["datasets_models"].find("Datasets:") != -1
        result["f"] = True
        result["poc"] = True
        result["date"] = row["urldate"]
        result["star"] = make_star(row["ranking"])
        result["link_github"] = "Manual for now"
        result["math"] = make_math(1)
        result["link_article"] = row["url"]

        parse_result.append(result)

    with open(f'data/{folder}/output.json', 'w') as f:
        json.dump(parse_result, f)
