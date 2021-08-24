# caitlyn

## Developer Log

- [Phase 1: Building SIVIR](#phase-1-building-sivir)
  - [Task 01: Do You Think This Is A Game?](#task-01-do-you-think-this-is-a-game)

### Phase 1: Building SIVIR

For this project, I'll have to build a custom dataset full of game screenshots, which I'm naming SIVIR (Screenshot Images of Videogames for Identification Research). We'll be getting all of it from the Twitch API, using thumbnails and clips of streamers. 

#### Task 01: Do You Think This Is A Game?

That's the question I'm trying to get Caitlyn to answer, anyways. I figured that in the long term scope of this project I'd have Caitlyn watching clips and streams and thumbnails on her own, and it would be an issue if she was only expecting pictures of games and trying to guess what game it was. Chances are there would be a lot of stuff in game categories where the streamer just happened to be doing a chat break or playing a different game entirely (annoying for me, but what can you do). So the idea was to make a little model that would first filter out the "bad" images, where there were no games to detect and it would just mess up the training.

So the plan was as follows:
 - Build a smaller dataset (Pre-SIVIR) with "game" and "not game" labels
 - Get favorable results with as lightweight of a CNN as possible, if not, try ResNet18 or another out-of-the-box larger model
 - Use the model to build a larger SIVIR by filtering out the non-game screenshots when labelling games

It's important to me now that this preliminary model is as small as possible so inference times will be low, but we'll see how difficult this task actually is. I've spent the past week or so building Pre-SIVIR by scraping the Twitch API of the top 100 games and picking around 200-1000 good images of each. I also took thumbnails from each category where streamers weren't playing games and put them into the "Not Game" category, along with a heavy sampling of categories like Just Chatting, Music, Science and Technology, and "Pools, Hot Tubs, and Beaches" (looks like Twitch's analytics department is working overtime). 

Altogether, Pre-SIVIR has around 38,000 images of games and 20,000 images of non-games. I have unlimited space on my university Google Drive, so I'll host it [here](https://drive.google.com/file/d/1jksM6F0pnA_3fxajx5n7WmIvSeus6csD/view?usp=sharing) for anyone who's trying to do more work with games and screenshots.

I'm quite fond of PyTorch for experiments, but I'm planning to eventually deploy Caitlyn as a website or extension, so I'll try to stick with the TensorFlow universe for now. I'm putting together quite possibly the smallest good CNN to test it, so we'll see how it goes in the next section.
