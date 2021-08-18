# caitlyn

## Developer Log

- [Phase 1: Building SIVIR](#phase-1-building-sivir)
  - [Task 01: Screenshot Classification](#task-01-screenshot-classification)

### Phase 1: Building SIVIR

For this project, I'll have to build a custom dataset full of game screenshots, which I'm naming SIVIR (Screenshot Images of Videogames for Identification Research). We'll be getting all of it from the Twitch API, using thumbnails and clips of streamers. There's just one major problem, though: Streamers are often lazy and don't actually change the game when they stop playing or switching games.

To tell that a streamer is playing a different game than the one they're actually listed as is something that's not even possible right now (it would mean that I would have to have a trained model already, which is what I'm trying to build this dataset for in the first place), so I'll be tackling an easier task: first training a shallow version of Caitlyn to determine what is a screenshot and what is a camera video, using a smaller set of data that I'll go over and make sure is 100% correctly labelled. This way, I can scrape tens of thousands of images and get Caitlyn to filter out the images that aren't actually screenshots, leaving us with a hopefully mostly clean set of images that we can call SIVIR.

#### Task 01: Screenshot Classification
