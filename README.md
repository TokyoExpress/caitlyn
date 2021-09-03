# caitlyn

## Developer Log

- [Phase 1: Building SIVIR](#phase-1-building-sivir)
  - [Task 01: Initial Data Collection](#task-01-initial-data-collection)
  - [Task 02: Model Testing](#task-02-model-testing)
  - [Task 03: A Discussion of Scope](#task-03-a-discussion-of-scope)

### Phase 1: Building SIVIR

For this project, I'll have to build a custom dataset full of game screenshots, which I'm naming SIVIR (Screenshot Images of Videogames for Identification Research). We'll be getting all of it from the Twitch API, using thumbnails and clips of streamers. 

#### Task 01: Initial Data Collection

I figured that in the long term scope of this project I'd have Caitlyn watching clips and streams and thumbnails on her own, and it would be an issue if she was only expecting pictures of games and trying to guess what game it was. Chances are there would be a lot of stuff in game categories where the streamer just happened to be doing a chat break or playing a different game entirely (annoying for me, but what can you do). So the idea was to make a little model that would first filter out the "bad" images, where there were no games to detect and it would just mess up the training.

So the plan was as follows:
 - Build a smaller dataset (Pre-SIVIR) with "game" and "not game" labels
 - Get favorable results with as lightweight of a CNN as possible, if not, try ResNet18 or another out-of-the-box larger model
 - Use the model to build a larger SIVIR by filtering out the non-game screenshots when labelling games

It's important to me now that this preliminary model is as small as possible so inference times will be low, but we'll see how difficult this task actually is. I've spent the past week or so building Pre-SIVIR by scraping the Twitch API of the top 100 games and picking around 200-1000 good images of each. I also took thumbnails from each category where streamers weren't playing games and put them into the "Not Game" category, along with a heavy sampling of categories like Just Chatting, Music, Science and Technology, and "Pools, Hot Tubs, and Beaches" (looks like Twitch's analytics department is working overtime). 

Altogether, Pre-SIVIR has around 38,000 images of games and 30,000 images of non-games. I have unlimited space on my university Google Drive, so I'll host it [here](https://drive.google.com/file/d/1RuoT9T8Ghpq9PdsCunSOCDfVxE9NP_IF/view?usp=sharing) for anyone who's trying to do more work with games and screenshots.

I'm quite fond of PyTorch for experiments, but I'm planning to eventually deploy Caitlyn as a website or extension, so I'll try to stick with the TensorFlow universe for now. I'm putting together quite possibly the smallest good CNN to test it, so we'll see how it goes in the next section.

#### Task 02: Model Testing

I started off with the simplest Keras CNN possible, with 2 convolution layers with ReLU, followed by a FC layer and a binary classifier with sigmoid activation. This thing was actually unable to learn no matter how I tweaked the hyperparameters or learning rate (it would just output either all game or all non-game), so my dreams of a super lightweight initial classifier were out the window.

Next, I decided to try transfer learning with ResNet50 (I would've tried RN18 first but RN50 is the smallest one that comes pretrained in Keras). This model was actually able to achieve pretty good results, maxing out and converging to about 90% accuracy. The validation accuracy never seemed to decrease, which seemed very good. Almost too good, and that's when I realized that this model was never going to work. It's not that it was overfitting the training data - again, the validation accuracy was always just as high as the training accuracy. The main issue was that both the training data and validation data only contained images of those top 100 games, which seemed like quite a lot at the beginning, but quickly revealed that it was not nearly enough to encompass the full distribution of games. While games like Call of Duty and Apex Legends will look quite similar in images, games like osu!, Gartic Phone, and PICO PARK are whole different types of games. 

<img src="https://github.com/TokyoExpress/caitlyn/blob/main/pics/warzone.jpg" width=500></img>
<img src="https://github.com/TokyoExpress/caitlyn/blob/main/pics/apex.jpg" width=500></img>

<i>Warzone and Apex are pretty standard games, no issue here.</i>

<img src="https://github.com/TokyoExpress/caitlyn/blob/main/pics/osu.png" width=500></img>
<img src="https://github.com/TokyoExpress/caitlyn/blob/main/pics/picopark.jpg" width=500></img>

<i>osu! and Pico Park, just two of the many games that will absolutely destroy the test accuracy of this model.</i>

In fact, that only reason that we know that those are games is because our intrinsic understanding of what makes up a game goes far beyond simple visuals. It also didn't help that some games were played in a browser, but we couldn't consider something like YouTube or Twitch a game. What if the streamer happened to be watching a game on Twitch? At first glance, it seems like classifying games would be a relatively simple task, but it soon becomes apparent that a model that can differentiate a game, a video of a game, and a colorful website that is in fact not a game must be <i>extremely</i> intelligent by computer vision standards.

<img src="https://github.com/TokyoExpress/caitlyn/blob/main/pics/gartic.jpg" width=500></img>
<img src="https://github.com/TokyoExpress/caitlyn/blob/main/pics/twitch.png" width=500></img>

<i>What should even happen for these?</i>

Anyways, after producing a test set with completely different games, it was obvious that the ResNet model was good at spotting games that it had already seen, but it had no idea what a game really was. Tinkering with the classification threshold yielded two less-than-ideal results: either maximize the recall and remove all non-games, but at the cost of misclassifying some new games as non-games, or maximize the precision and try not to remove any actual game screenshots, which resulted in very little images being certain non-game predictions anyways. The last thing I wanted was for Caitlyn to miss out on a lot of training data because this model thought a new game looked like a non-game and didn't let a majority of the images from that game through. At the same time, the model was so tunnel-visioned that there were a small percentage of games (browser games and non-colorful, simple games, mostly) that it would classify as non-game with > 0.95 certainty, so there was no threshold where I could guarantee no false negatives.

So the model testing stage revealed to me that while it was simple for me, someone who has been playing games his whole life (also with a much smarter brain than these math machines) to think that identifying games would be easy, there had to be a lot more thought put into this project. Did I want to set it up so that this classifier head had almost every type of game in the training data? If so, I would have to manually go and annotate over a million images, which this classifier was supposed to do in the first place. Unless I had more time and a lot more funding, there was no way I could go and gather meaningful images of over 5000 games by myself.

With all these thoughts, I had to make some decisions about the next steps of this project.

#### Task 02: A Discussion of Scope
