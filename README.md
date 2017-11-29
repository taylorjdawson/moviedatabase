##PostgreSQL
__Host:__ dhansen.cs.georgefox.edu \
__Database:__ themoviedatabase \
__User:__ tdawson16\
__Password:__ banker85=government=Maybe=
## Notes

- 54 movies missing from the movieData.json file because (See [duplicate_movie_ids.txt](duplicate_movie_ids.txt))
they have duplicate ids
- In the movies.json file directors, producers, studios, genre, awards are lists
- 139 genres have data_errors &mdash; shouldn't be too hard to fix. I will come back to it later
- 2464 people have neither date_of_birth nor date_of_death
- 163 casts members (out of 8000+ so not too bad) have film_ids not found within movies.xml (See [not_in_movie.txt](not_in_movie.txt)). 
**Important**: When loading cast members first check that the field `in_movie` is `true`. 
- 13 null values in [remakes.json](Data_json/remakes.json) but only with in the year fields. All `remake_id` and 
`original_id` reference film_ids located in [movies.json](Data_json/movies.json) file

## Todos
- [ ] Add stage name in the acts_in table
- [x] Add first and last name in participant table
- [ ] Need to review the duplicate movie ids
- [ ] Review .json files for erroneous data
- [x] Create directs table, writes table
- [ ]