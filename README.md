# Music-Festival-Playlist-Builder

This script scrapes festival lineups from the web and creates relevant Spotify playlists for anybody to listen to! You can view the festival playlists that get generated [here](https://open.spotify.com/user/7m0k6ux7waeubykapbusynvkk?si=Y6eLN6pdRXS6PsVJXaddUQ)

# Install 

Install relevant dependencies 
```pip install -r requirements.txt```

Generate a spotify access token. Instructions for generating that can be found at https://developer.spotify.com/documentation/web-api/quick-start/

I chose to utilize a persistent layer (PostgreSQL) so that I could run the script at my leisure and not worry about duplicate playlist creation. If you prefer a different db or cannot install postgres, modifying the script should be pretty trivial. 

# Running 

```python playlist_builder.py``` 

This could easily be run on a scheduler to keep the playlist generation constant. 

Feel free to reach out with any questions/ideas! 

