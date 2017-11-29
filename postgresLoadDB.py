#!/usr/bin/python
import psycopg2
import json


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = dict(
            host='dhansen.cs.georgefox.edu',
            database ='teach_yourself',
            user = 'csis314',
            password ='php',
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
        with open('actors.json' , 'r') as actorJSON:
            for person in actorJSON:
                participants[participant_id] = person['stage_name'].lower()
                cur.execute("INSERT into participant(participant_id, date_of_birth, date_of_death, gender, name, familyname, firstname)"
                            " VALUES (" + participant_id + "," + person['date_of_birth'] + "," + person['date_of_death']
                            + "," + person['gender'] + "," + person['stage_name'] + "," + person['family_name'] + "," + person['first_name'] + ")")
                participant_id+=1

        print('Loading Participants...')
        # Ingest other participants like directors, producers
        with open('participant.json' , 'r') as participantJSON:
            for person in participantJSON:
                participants[participant_id] = person['name']
                cur.execute("INSERT into participant(participant_id, date_of_birth, date_of_death, gender, name, familyname, firstname)"
                            " VALUES (" + participant_id + "," + person['date_of_birth'] + "," + person['date_of_death']
                            + ", null ," + person['name'] + "," + person['family_name'] + "," + person['given_name'] + ")")
                participant_id += 1

        # Ingest Films
        print('Loading Films...')
        film_id = 0
        movieList = []
        with open('movies.json', 'r') as moviesJSON:
            for film in moviesJSON:
                movieList[film_id] = film['film_id']
                cur.execute("INSERT into themoviedatabase.public.movies (film_id,title,year, genre) VALUES " +
                            "(" + film_ID + ", " + film['title'] + ", " + film['year'] + "," + film['genres']['genre'] + ")")
                # loads the director table
                direct_participant = participants.index(film['directors']['name'])
                cur.execute("INSERT into directs (film_id , participant_id ) VALUES (" + film_id +"," + direct_participant + ")")
                # loads the writer table
                write_participant = participants.index(film['directors']['name'])
                cur.execute("INSERT into directs (film_id , participant_id ) VALUES (" + film_id + "," + write_participant + ")")
                film_id+=1

        # Ingest Remakes
        print('Loading Remakes...')
        with open('remakes.json', 'r') as remakesJSON:
            for film in remakesJSON:
                old_Remake_ID = film['remake_id']
                new_Remake_ID = movieList.index(old_Remake_ID)
                fraction = film['remake_fraction']
                old_Original_ID = film['original_id']
                new_Original_ID = movieList.index(old_Original_ID)
                cur.execute("INSERT into is_remake_of (remake_film_id, original_film_id, fraction)" +
                            "VALUES (" + new_Remake_ID + "," + new_Original_ID + "," + fraction + ")" )

        # Ingest Cast Lists
        print('Loading Acts_in table')
        with open('casts.json', 'r') as actsinJSON:
            for person in actsinJSON:
                actor_id = participants.index(person['actor_name'])
                film_id = movieList.index(person['film_id']['id'])
                cur.execute("INSERT INTO acts_in (participant_id, role, film_id, role_type) VALUES (" + actor_id + ","
                            + person['character_name'] + "," + film_id + "," + person['role'] + ")" )


        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()