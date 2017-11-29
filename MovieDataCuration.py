import pandas as pd
import numpy as np
import pickle
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import pickle



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
    # re.sub('@','','@1984') get rid of @ sign in dates
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
    CATEGORIES = dict(ctxx='uncategorized',
                      actn='violence',
                      camp='camp',
                      comd='comedy',
                      disa='disaster',
                      epic='epic',
                      horr='horror',
                      noir='black',
                      scfi='science fiction',
                      west='western',
                      advt='adventure',
                      cart='cartoon',
                      docu='documentary',
                      faml='family',
                      musc='musical',
                      porn='pornography',
                      surl='surreal',
                      surr='surreal',
                      avga='avant garde',
                      cnr='cops and robbers',
                      cnrb='cops and robbers',
                      dram='drama',
                      hist='history',
                      myst='mystery',
                      romt='romantic',
                      susp='thriller',
                      biop='biographical Picture',
                      fant='fantasy',
                      west1='western',
                      tv='television show',
                      tvmini='television mini series',

                      )
    movies_xml_data = open('Data/movies.xml').read()
    soup = BeautifulSoup(movies_xml_data, 'xml')
    movie_data = {}
    i = 0
    for film in soup.movies.find_all('film'):
        if film.fid not in DUP_IDS:
            str()
            film_id   = film.fid.text.lower().strip() if film.fid else 'Null'
            title     = film.t.text if film.t else 'Null'
            year      = (film.year.text if isValidYear(re.sub('@', '', film.year.text)) else 'Null') if film.year else 'Null'
            directors = [{'key':d.dirk.text if d.dirk else 'Null', 'name': d.dirn.text if d.dirn else 'Null'} for d in film.find_all('dir')]
            producers = [{'name': p.pname.text if p.pname else 'Null', 'key': p.prodk.text if p.prodk else 'Null'} for p in film.find_all('prod')]
            studios   = [{'studio': s.studio.text if s.studio else 'Indie'} for s in film.find_all('studios')]
            genres  = [{'genre': ( CATEGORIES[cat.text.lower().strip()] if cat.text.lower().strip() in CATEGORIES else 'data_error ' + cat.text) if cat else 'Null'} for cat in film.find_all('cat')]
            awards    = [{  'award_type': a.awtype.text if a.awtype else 'Null',
                            'award_attribute': a.awattr.text if a.awattr else 'Null',
                            'award_reference': a.awref.text if a.awref else 'Null'} for a in film.find_all('awards')]
            movie_data[str(i)] = dict(film_id=film_id,
                                      title=title,
                                      year=year,
                                      directors=directors,
                                      producers=producers,
                                      studios=studios,
                                      genres=genres,
                                      awards=awards)
            i += 1
    with open('movies.json', 'w') as f:
        json.dump(movie_data, f, indent=True)


def peopleToJSON():
    people_xml_data = open('Data/people.xml').read()
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
    # TODO: Make sure names are lower case

    # Get the list of film_ids that appear in movies.json
    with open('film_ids', 'rb') as f:
        film_ids = pickle.load(f)


    cast_xml_data = open('Data/casts.xml').read()
    soup = BeautifulSoup(cast_xml_data, 'xml')
    cast_data = {}
    i = 0

    for cast in soup.find_all('m'):
        film_id        = ({'id': cast.f.text.lower().strip(), 'in_movie': cast.f.text.lower().strip() in film_ids}) if cast.f else 'Null'
        film_title     = cast.t.text if cast.t else 'Null'
        actor_name     = cast.a.text if cast.a else 'Null'
        character_name = cast.n.text if cast.n else 'Null'
        role           = cast.r.text if cast.r else 'Null'
        cast_data[str(i)] = dict(film_id=film_id, film_title=film_title, actor_name=actor_name, character_name=character_name, role=role)
        i += 1

    with open('casts.json', 'w') as f:
        json.dump(cast_data, f, indent=True)

def remakesToJSON():
    # TODO: Check Ref integrity between film_id remake_id and movies.json

    # Get the list of film_ids that appear in movies.json
    with open('film_ids', 'rb') as f:
        film_ids = pickle.load(f)


    remake_xml_data = open('Data/remakes.xml').read()
    soup = BeautifulSoup(remake_xml_data, 'xml')
    remake_data = {}
    i = 0

    for remake in soup.find_all('remake'):
        remake_id       = (remake.rid.text.lower().strip() if remake.rid.text.lower().strip() in film_ids else 'not in fids' ) if remake.rid else 'Null'
        remake_title    = remake.rtitle.text if remake.rtitle else 'Null'
        remake_year     = (remake.ry.text if isValidYear(remake.ry.text) else 'Null') if remake.ry else 'Null'
        remake_fraction = (remake.frac.text.strip().replace(' ','') if bool(re.match('0*\.[0-9]+', remake.frac.text.strip().replace(' ',''))) else 'Null') if remake.frac else 'Null'
        original_id     = (remake.sid.text.lower().strip() if remake.sid.text.lower().strip() in film_ids else 'not in fids') if remake.sid else 'Null'
        original_title  = remake.stitle.text if remake.stitle else 'Null'
        original_year   = (remake.sy.text if isValidYear(remake.sy.text) else 'Null') if remake.sy else 'Null'
        remake_data[str(i)] = dict(remake_id=remake_id, remake_title=remake_title, remake_year=remake_year, remake_fraction=remake_fraction,
                                   original_id=original_id, original_title=original_title, original_year=original_year)
        i += 1
    with open('remakes.json', 'w') as f:
        json.dump(remake_data, f, indent=True)


def isValidYear(year):
    return bool(re.match('^\d{4}$', year))

def createFilmIdList():
    with open('movies.json') as json_data:
        movie_ids = json.load(json_data)
        film_ids = [fid['film_id'] for fid in movie_ids.values()]
        with open('film_ids', 'wb') as fp:
            pickle.dump(film_ids, fp)

# createFilmIdList()
# moviesxmlToJSON()
# peopleToJSON()
# castToJSON()
remakesToJSON()



