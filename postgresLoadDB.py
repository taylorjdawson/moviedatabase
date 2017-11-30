#!/usr/bin/python
import psycopg2
import json


def loadActors():
    return
def loadPeople():
    return
def loadCasts():
    return
def loadMovies():
    return


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = dict(
            host='dhansen.cs.georgefox.edu',
            database ='themoviedatabase',
            user = 'tdawson16',
            password ='banker85=government=Maybe=',
        )

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')

        print('Loading List of Awards ...')
        # Ingest Award Ref Table
        # TODO ADD Award Ref Table


        print('Loading List of Studios ...')
        # Ingest studio Ref Table
        # TODO ADD Studio Ref TABLE


        print('Loading Actors...')


        # Ingest participants
        #TODO Add duplicate entry protection
        participant_id = 0
        participants = []

        with open('Data_json/actors.json', 'r') as f:
            persons = json.load(f)

            for person in persons.values():

                participants.append(person['stage_name'].lower())


                cur.execute("INSERT into participant(participant_id, date_of_birth, date_of_death, gender, name, family_name, first_name)"
                            " VALUES ( " + str(participant_id) + " , " + person['date_of_birth'] + " , " + person['date_of_death']
                            + " , '" + person['gender'] + "' , '" + person['stage_name'] + "' , '" + person['family_name'] + "' , '" + person['first_name'] + "' );")
                participant_id += 1

        print('Loading Participants...')
        # Ingest other participants like directors, producers
        with open('Data_json/people.json', 'r') as f:
            participantJSON = json.load(f)

            for person in participantJSON.values():
                participants.append(person['name'].lower())
                cur.execute("INSERT into participant(participant_id, date_of_birth, date_of_death, gender, name, family_name, first_name)"
                            " VALUES ( " + str(participant_id) + " , " + person['date_of_birth'] + " , " + person['date_of_death']
                            + " , null , '" + person['name'] + "' , '" + person['family_name'] + "' , '" + person['given_name'] + "' );")
                participant_id += 1

        # Ingest Films
        print('Loading Films...')
        film_id = 0
        movieList = []
        with open('Data_json/movies.json', 'r') as f:
            moviesJSON = json.load(f)

            for film in moviesJSON.values():
                movieList.append(film['film_id'])
                cur.execute("INSERT into themoviedatabase.public.movies (film_id,title,year, genre) VALUES " + # TODO: Include more than one genre
                            " ( " + str(film_id) + " , '" + film['title'] + "' , " + film['year'] + " , '" + (film['genres'][0]['genre'] if film['genres'] else 'Null') + "' );")
                # loads the director table
                for director in film['directors']:
                    if director['name'].lower() in participants:
                        direct_participant = participants.index(director['name'].lower())
                        cur.execute("INSERT into directs_movie (film_id , participant_id ) VALUES ( " + str(film_id) +" , " + str(direct_participant) + " );")
                # loads the writer table
                #write_participant = participants.index(film['writers']['name'])
                #cur.execute("INSERT into writes_movie (film_id , participant_id ) VALUES ( " + film_id + " , " + write_participant + " );")
                film_id += 1

        # Ingest Remakes
        print('Loading Remakes...')
        with open('Data_json/remakes.json', 'r') as f:
            remakesJSON = json.load(f)

            for film in remakesJSON.values():
                if not film['remake_id'] == 'not in fids' and not film['original_id'] == 'not in fids':
                    old_Remake_ID = film['remake_id']
                    new_Remake_ID = movieList.index(old_Remake_ID)
                    fraction = film['remake_fraction']
                    old_Original_ID = film['original_id']
                    new_Original_ID = movieList.index(old_Original_ID)
                    cur.execute("INSERT into is_remake_of (remake_film_id, original_film_id, fraction)" +
                                " VALUES ( " + str(new_Remake_ID) + " , " + str(new_Original_ID) + " , " + fraction + " );" )

        # Ingest Cast Lists
        print('Loading Acts_in table')
        with open('Data_json/casts.json', 'r') as f:
            actsinJSON = json.load(f)

            for person in actsinJSON.values():
                if person['actor_name'] in participants and person['film_id']['id'] in movieList:
                    actor_id = participants.index(person['actor_name'])
                    film_id = movieList.index(person['film_id']['id'])
                    cur.execute("INSERT INTO acts_in (participant_id, role, film_id, role_type) VALUES ( " + str(actor_id) + " , '"
                                + person['character_name'] + "' , " + str(film_id) + " , '" + person['role'] + "' );" )

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
        conn.commit()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()