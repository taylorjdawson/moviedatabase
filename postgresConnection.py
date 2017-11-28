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

        film_id = 0
        # Needs the name of the actual JSON file
        with open('movies.json', 'r') as moviesJSON:
            for film in moviesJSON:
                cur.execute("INSERT into themoviedatabase.public.movies (film_id,title,year) VALUES (" + film_ID + ", " + film['title'] + ", " + film['year'] + ")")
                film_id+=1

        #cur.execute('insert into cust_name', ('M. T. Head'))

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