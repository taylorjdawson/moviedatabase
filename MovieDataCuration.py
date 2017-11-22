import pandas as pd
import numpy as np
import pickle
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

xml_data = open('Data/movies.xml').read()
soup = BeautifulSoup(xml_data, 'xml')

def xml2df(xml_data):
    root = ET.XML(xml_data) # element tree
    all_records = []
    for i, child in enumerate(root):
        record = {}
        for subchild in child:
            record[subchild.tag] = subchild.text
            all_records.append(record)
    return pd.DataFrame(all_records)

def pickleDataFrame():
    with open('movieDataFrame.pickle', 'wb') as f:
        pickle.dump(movieDataFrame, f)

def xmlToJSON(xml_data):
    all_movies = {}
    i = 0
    for film in soup.movies.find_all('film'):
        fid       = film.fid.text if film.fid else 'Null'
        title     = film.t.text if film.t else 'Null'
        year      = film.year.text if film.year else 'Null'
        directors = [{'key':d.dirk.text if d.dirk else 'Null', 'name': d.dirn.text if d.dirn else 'Null'} for d in film.find_all('dir')]
        producers = [{'name': p.pname.text if p.pname else 'Null', 'key': p.prodk.text if p.prodk else 'Null'} for p in film.find_all('prod')]
        studios   = [{'studio': s.studio.text if s.studio else 'Null'} for s in film.find_all('studios')]
        category  = [{'category': cat.text if cat else 'Null'} for cat in film.find_all('cats')]
        all_movies[str(i)] = dict(fid=fid, title=title, year=year, directors=directors, producers=producers, studios=studios, category=category)
        print(json.dump(all_movies))
        i += 1




moviesJSON = xmlToJSON(soup)

movieDataFrame = '' #xml2df(xml_data)