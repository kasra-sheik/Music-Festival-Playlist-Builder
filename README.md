# Music-Festival-Playlist-Builder

# Install 

Install relevant dependencies 
```pip install -r requirements.txt```

Generate a spotify access token. Instructions for generating that can be found at https://developer.spotify.com/documentation/web-api/quick-start/

I chose to utilize a persistent layer (PostgreSQL) so that I could run the script at my leisure and not worry about duplicate playlist creation. If you prefer a different db or cannot install postgres, modifying the script should be pretty trivial. 

# Running 

```python playlist_builder.py``` 

