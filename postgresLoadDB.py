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
        award_id = 0
        award_array = []
        with open('Data_json/awards.json', 'r') as f:
            awards = json.load(f)
            for key in awards.keys():
                award_array.append(key.lower())
            for award in awards.values():
                cur.execute("Insert into awards(award_id, award_name) VALUES ( " + str(award_id)
                            + " , '" + award['awarding organization'] + "' );")
                award_id += 1
        print(str(award_array))


        print('Loading List of Studios ...')
        # Ingest studio Ref Table
        studio_id = 0
        studio_list = []
        with open('Data_json/studios.json','r') as f:
            studios = json.load(f)
            for studio in studios.values():
                studio_list.append(studio['studio_name'].lower())
                cur.execute("Insert into studios(studio_id, studio_name) VALUES (" + str(studio_id)
                            + " , '" + studio['studio_name'] + "' );")
                studio_id += 1


        print('Loading Actors...')
        # Ingest participants
        participant_id = 0
        participants = []

        with open('Data_json/actors.json', 'r') as f:
            persons = json.load(f)

            for person in persons.values():

                participants.append(person['stage_name'].lower())

                cur.execute("INSERT into participant(participant_id, date_of_birth, date_of_"
                            "death, gender, name, family_name, first_name) VALUES ( "
                            + str(participant_id) + " , " + person['date_of_birth'] + " , "
                            + person['date_of_death'] + " , '" + person['gender'] + "' , '"
                            + person['stage_name'] + "' , '" + person['family_name'] + "' , '"
                            + person['first_name'] + "' );")

                for award in person['awards']:
                    if award['award_type'].lower() in award_array:
                        award_index = award_array.index(award['award_type'].lower())
                        cur.execute("INSERT into participant_is_awarded(award_id, participant_id) "
                                    "VALUES ( '" + str(award_index) + "' , '"
                                    + str(participant_id) + "');")

                participant_id += 1

        print('Loading Participants...')
        # Ingest other participants like directors, producers
        with open('Data_json/people.json', 'r') as f:
            participantJSON = json.load(f)

            for person in participantJSON.values():
                participants.append(person['name'].lower())
                cur.execute("INSERT into participant(participant_id, date_of_birth, "
                            "date_of_death, gender, name, family_name, first_name)"
                            " VALUES ( " + str(participant_id) + " , " + person['date_of_birth']
                            + " , " + person['date_of_death'] + " , null , '" + person['name'] + "' , '"
                            + person['family_name'] + "' , '" + person['given_name'] + "' );")
                participant_id += 1

        # Ingest Films
        print('Loading Films...')
        film_id = 0
        movieList = []
        with open('Data_json/movies.json', 'r') as f:
            moviesJSON = json.load(f)
            for film in moviesJSON.values():
                movieList.append(film['film_id'])
                cur.execute("INSERT into themoviedatabase.public.movies (film_id,title,year, genre) VALUES "
                            + " ( " + str(film_id) + " , '" + film['title'] + "' , " + film['year']
                            + " , '" + (film['genres'][0]['genre'] if film['genres'] else 'Null') + "' );")

                # loads the director table
                for director in film['directors']:
                    if director['name'].lower() in participants:
                        direct_participant = participants.index(director['name'].lower())
                        cur.execute("INSERT into directs_movie (film_id , participant_id ) VALUES ( "
                                    + str(film_id) +" , " + str(direct_participant) + " );")

                # loads the writer table
                for writer in film['writers']:
                    write_name = str(writer['name'])
                    cur.execute("INSERT into writes_movie VALUES ( '" + str(film_id) + "' , '"
                                + write_name + "' );")

                # loads the movie awards
                for award in film['awards']:
                    if award['award_type'].lower() in award_array:
                        film_award = award_array.index(award['award_type'].lower())
                        cur.execute("INSERT into movie_is_awarded VALUES ( '" + str(film_id) + "' , '"
                                    + str(film_award) + "');")

                # loads the has_studio table
                for studio in film['studios']:
                    if studio['studio'].lower() in studio_list:
                        this_studio = str(studio_list.index(studio['studio'].lower()))
                        cur.execute("INSERT into has_studio VALUES ( '" + str(film_id)
                                    + "' , '" + this_studio + "' );")

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
                    cur.execute("INSERT into is_remake_of (remake_film_id, original_film_id, fraction)"
                                + " VALUES ( " + str(new_Remake_ID) + " , " + str(new_Original_ID)
                                + " , " + fraction + " );" )

        # Ingest Cast Lists
        print('Loading Acts_in table...')
        with open('Data_json/casts.json', 'r') as f:
            actsinJSON = json.load(f)

            for person in actsinJSON.values():
                if person['actor_name'] in participants and person['film_id']['id'] in movieList:
                    actor_id = participants.index(person['actor_name'])
                    film_id = movieList.index(person['film_id']['id'])
                    cur.execute("INSERT INTO acts_in (participant_id, role, film_id, role_type) VALUES ( "
                                + str(actor_id) + " , '" + person['character_name'] + "' , " + str(film_id)
                                + " , '" + person['role'] + "' );" )


        # close the communication with the PostgreSQL
        cur.close()
        conn.commit()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()