## Notes

- 54 movies missing from the movieData.json file because (See [duplicate_movie_ids.txt](duplicate_movie_ids.txt))
they have duplicate ids
- In the movies.json file directors, producers, studios, genre, awards are lists
- 139 genres have data_errors &mdash; shouldn't't be too hard to fix. I will come back to it later
- 2464 people have neither date_of_birth nor date_of_death
- 163 casts members have film_ids not found within movies.xml (See [not_in_movie.txt](not_in_movie.txt))

## Todos
- [ ] Add stage name in the acts_in table
- [ ] Add first and last name in participant table
- [ ] Need to review the duplicate movie ids
- [ ] Review .json files for erroneous data
- [ ] Create directs table, writes table