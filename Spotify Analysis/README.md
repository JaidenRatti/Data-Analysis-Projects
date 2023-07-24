# Spotify-Song-Recommender

## What is this? ##

Recommendation.ipynb recommends songs by taking in two public Spotify links. 

The first link is either a 
- playlist: this is the 'seed' playlist (the one you want to add songs to)
- song: this is the 'seed' song (you want to find songs similar to this)

The second playlist is a playlist that you want to extract songs from to add to your 'seed' playlist or see what is similar to your 'seed' song

The program will then recommend the most similar songs (an arbitrary amount) from the second playlist that match the vibe of your 'seed' entry.


## What would it be used for? ## 

Know a friend with a long and unorganized playlist that you want to take songs from but don't have the time to sort through?

Want to listen to music from a new artist but don't know which songs you'd like?

Really like a specific song and want to find new songs in other playlists like that one?

Curious how similar your music tastes are to another playlist?


## How is it different than Spotify? ##

Spotify currently recommends a few songs at the bottom of a playlist, yet this is pretty much it when it comes to recommending songs for playlists. Finding music from new artists should be streamlined to current music tastes (since listening history & time are valuable data). Sifting through large playlists can be annoying, so imagine this as a, "Here's what you would like from this playlist based on your music" highlight at the top of every playlist.  


## How does it work? (High-level) ##

All songs in the seed playlist/song are converted to a df with unique audio features and weights associated to each feature thanks to the Spotify API (i.e danceability, valence, see the full list [here](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)).

Each of these features from the seed entry get averaged and converted to an array (essentially a vector). 

The audio features for each song in the second playlist are converted into arrays (once again, vectors).

Distance between the average seed array and each array in the second playlist is calculated (using Euclidian Distance, not Cosine Similarity since magnitude matters). Shorter the distance = More similar the song. Here's an image if you are interested. 

![image](https://user-images.githubusercontent.com/49047523/211133338-72072fc6-2d61-4ea1-b43a-57972edcb0e1.png)
[Source](https://medium.com/@sasi24/cosine-similarity-vs-euclidean-distance-e5d9a9375fc8)


The songs in the second playlist are then sorted by distance (similarity) to the first playlist. User can then select how many songs they want recommended from this list. 


## Additions Currently Working on ##

Let users add a song link instead of seed playlist :white_check_mark:

A separate program that takes two playlists or songs and neatly visualizes the differences in different audio features
