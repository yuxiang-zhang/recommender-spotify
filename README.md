## Inspiration
We are aware of how time-consuming and frustrating it can be to update or expand our playlist. We may spend hours and hours browsing numerous tracks yet few of them match our tastes. Inspired by Spotify's Discover Weekly playlist, we decided to design a system that helps people solve this problem.

## What it does
Our system provides users with recommended tracks based on their selected playlist. After the users sign in with their Spotify accounts, our system will access their current playlists. Users can choose a specific playlist they wish to update or choose to generate a comprehensive recommendation based on the past play history. 

## How we built it
We developed the algorithm using Python, Flask, Pandas, and Spotify API and built the user interface with HTML and CSS on visual-studio code. 
Our system downloads the audio features of the tracks in the selected playlist (or play history) from Spotify API, imports these data into a Pandas DataFrame, compiles the aggregate statistics for each feature, and normalizes them using the min-max approach. Then, it selects the features with the least standard deviation across all features as the target features to feed to the Spotify recommendation API.  

## Challenges we ran into
Because of the time constraints, we were only able to implement the simplest strategy (the one described above) in generating recommendations. We also did not have time to properly evaluate the relevancy/accuracy of recommendations. The efficiency and security of the system were not taken into consideration. 

## Accomplishments that we're proud of
We've proud that our system does work. It generates a new recommended playlist based on the selected input playlist or past play history of the users.  
We've also proud that we both learned some new skills that we can use in future projects or in our careers.

## What we learned
The most important things we learned in this experience are staying positive, collaborating with the teammate, developing new skills, and acquiring knowledge in new fields in a tight period of time.

## What's next for Your New Playlist 
Initially, we were aiming for a recommender system built on top of machine learning algorithms. We wanted to leverage the power of transfer learning and find a pre-trained model for Spotify recommendations. Due to the time constraints, we were only able to complete a minimal version of the system without the machine learning trained models to support it. We would love to extend the system with such power in the next phase. 
Our next steps also include optimizing the algorithm to improve recommendation accuracy, addressing the limitations described above in the challenges section, employing audio features, and designing a more artistic and friendly user interface.
