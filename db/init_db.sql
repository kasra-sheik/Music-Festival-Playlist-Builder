-- ASSUMES POSTGRES INSTALLED PROPERLY 

CREATE DATABASE FestivalPlaylistBuilder; 

CREATE TABLE PLAYLISTS (
	id serial primary key,
	name text unique,
	spotify_id text unique 
);

