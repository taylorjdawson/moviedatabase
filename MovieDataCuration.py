import pandas as pd
import numpy as np
import pickle
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re




def xml2df(xml_data):
    root = ET.XML(xml_data) # element tree
    all_records = []
    for i, child in enumerate(root):
        record = {}
        for subchild in child:
            record[subchild.tag] = subchild.text
            all_records.append(record)
    return pd.DataFrame(all_records)

# def pickleDataFrame():
    # with open('movieDataFrame.pickle', 'wb') as f:
        # pickle.dump(movieDataFrame, f)

def moviesxmlToJSON():
    # TODO: Regex for dates
    # re.sub('@','','@1984') get rid of @ sign in dates
    # TODO: Awards
    DUP_IDS = ['CC80',
               'ECn107',
               'FNm10',
               'JuD11',
               'FB21',
               'GCt30',
               'RC5',
               'MLR6',
               'RdR38',
               None,
               'IAg10',
               'FrW10',
               'OP13',
               'GSt3',
               'ChC5',
               'ChC12',
               'ChC15',
               'PaJ2',
               'FZ8',
               'MRs21',
               'LAl4',
               'CoB1',
               'MxS10',
               'NR1',
               'HyC10',
               'JLT50',
               'JIv42',
               'SR45',
               'PSv10',
               'GeP15',
               'ArH205',
               'MBo12',
               'MeW10',
               'GxR10',
               'JaS13',
               'KRu25',
               'MAp43',
               'JRl10',
               'PDu10',
               'JKp35',
               'GeM17',
               'NiM30',
               'DDo15',
               'FOR12',
               'PAl4',
               'BLe5',
               'KaK10',
               'LeN10',
               'AKo15',
               'ThS5',
               'AnL15',
               'MiM10',
               'NtB10',
               'SfG1']
    movies_xml_data = open('Data/movies.xml').read()
    soup = BeautifulSoup(movies_xml_data, 'xml')
    movie_data = {}
    i = 0
    for film in soup.movies.find_all('film'):
        if film.fid not in DUP_IDS:
            film_id   = film.fid.text if film.fid else 'Null'
            title     = film.t.text if film.t else 'Null'
            year      = film.year.text if film.year else 'Null'
            directors = [{'key':d.dirk.text if d.dirk else 'Null', 'name': d.dirn.text if d.dirn else 'Null'} for d in film.find_all('dir')]
            producers = [{'name': p.pname.text if p.pname else 'Null', 'key': p.prodk.text if p.prodk else 'Null'} for p in film.find_all('prod')]
            studios   = [{'studio': s.studio.text if s.studio else 'Indie'} for s in film.find_all('studios')]
            category  = [{'category': cat.text if cat else 'Null'} for cat in film.find_all('cats')]
            awards    = [{  'award_type': a.awtype.text if a.awtype else 'Null',
                            'award_attribute': a.awattr.text if a.awattr else 'Null',
                            'award_reference': a.awref.text if a.awref else 'Null'} for a in film.find_all('awards')]
            movie_data[str(i)] = dict(film_id=film_id,
                                      title=title,
                                      year=year,
                                      directors=directors,
                                      producers=producers,
                                      studios=studios,
                                      category=category,
                                      awards=awards)
            i += 1
    with open('movies.json', 'w') as f:
        json.dump(movie_data, f, indent=True)


def peopleToJSON():
    people_xml_data = open('Data/movies.xml').read()
    soup = BeautifulSoup(people_xml_data, 'xml')
    people_data = {}
    i = 0
    for person in soup.people.find_all('person'):
        name = person.pname.text if person.pname else 'Null'
        family_name = person.familynm.text if person.familynm else 'Null'
        given_name = person.givennm.text if person.givennm else 'Null'
        date_of_birth = (person.dob.text if isValidYear(person.dob.text) else 'Null') if person.dob else 'Null'
        date_of_death = (person.dod.text if isValidYear(person.dod.text) else 'Null') if person.dod else 'Null'
        people_data[str(i)] = dict( name=name, family_name=family_name, given_name=given_name, date_of_birth=date_of_birth, date_of_death=date_of_death)
        i += 1
    with open('people.json', 'w') as f:
        json.dump(people_data, f, indent=True)

def castToJSON():
    # TODO: Reg integrity between film_id and movies.json
    # TODO: Makre sure names are lower case
    cast_xml_data = open('Data/casts.xml').read()
    soup = BeautifulSoup(cast_xml_data, 'xml')
    cast_data = {}
    i = 0
    for cast in soup.find_all('m'):
        film_id    = cast.f.text if cast.f else 'Null'
        film_title = cast.t.text if cast.t else 'Null'
        name       = cast.a.text if cast.a else 'Null'
        role       = cast.r.text if cast.r else 'Null'

        i += 1


def remakesToJSON():
    # TODO: Check Ref integrity between film_id remake_id and movies.json
    return



def isValidYear(year):
    return bool(re.match('^\d{4}$', year))



# moviesxmlToJSON()

# movieDataFrame = '' #xml2df(xml_data)


import pickle

with open('movieData.json') as json_data:
    movie_ids = json.load(json_data)
    film_ids = [fid['fid'] for fid in md.values()]

with open('film_ids', 'wb') as fp:
    pickle.dump(film_ids, fp)
