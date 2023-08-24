# GuessWho-Game

The _Guess Who?_ game was designed to be suitable for French children between 5 and 12 years old as part of a neuroscience experiment via videoconference to record the brain activity of both children at the same time, a technique called hyperscanning. Here is an overview of the game board:

![solo](https://github.com/jubnr/GuessWho-Game/assets/91159278/2026d6c9-f46d-4cfe-9e01-4e92462816b1)


## What's new?
_Guess Who?_ is a two-player board game that teaches basic reasoning skills. The game has 24 possible characters with various attributes e.g., gender, facial hair, glasses, etc. In the original board game, players randomly select a character card which the player's opponent must correctly guess the identity of through asking a series of yes or no questions. Each child takes turns asking yes-no questions to eliminate incorrect character possibilities on his/her game board. In the experimental version, I adapted the game to be presented in a digital format with familiar characters from popular animated television and film that targets this age group in France. Here, in addition to developing a digital version of the game board, I also adapted it to allow two different modes: solo and multiplayer. 
Instead of asking the original yes-no questions about features pertaining to the character, children are given clues which are displayed one by one above the game board on the child’s large external monitor.

## How to play?
In order to be suitable for pre-literate younger children as well as older literate children, each clue is represented with a short one- or two-word label and a picture. Three different modes have been created: training, solo and multiplayer. The figure below depicted the menu window that appears when you launch the game. 

![menu](https://github.com/jubnr/GuessWho-Game/assets/91159278/929fb783-1fa4-4b96-91e9-b1efcb2b2acc)

The training mode has been designed to explain the games' rules to the child. In total, each character round consists of four clues. Each child is instructed to remove the characters that do not correspond to the clue by clicking on the character's image using a wireless mouse located next to the external monitor. In response, a red "X" appears over the character indicating that the character has been eliminated. For example, if the clue received is “fille” (“girl”), the child sees a pink silhouette of a female human figure and should eliminate all female characters (see an example below).

![cross](https://github.com/jubnr/GuessWho-Game/assets/91159278/eee19d14-281e-4496-8214-982cee1bfa5e)

### How do you know if you found the right character?
If the character was correctly chosen, the character’s image appears outlined in green while if an incorrect character was chosen, the image is outlined in red. The game board then reinitializes, beginning again with a new set of clues leading to another character.

### Solo mode
For the solo phase, this process is repeated for each of the four clues until only one final character is left un-eliminated. After the four clues are displayed and a final character remains on the board, the correct answer appears in the middle of the screen. 

### Multiplayer mode
During the multiplayer mode, on the other hand, each member of the dyad receives different clues, which they must compare and discuss with another child located elsewhere, and with whom they interact via videoconference, in order to know which characters to eliminate. For instance, one child may receive the clue “sourire” (“smile”) while the other child may receive “garçon” (“boy”). By sharing their clues, both children know to eliminate all characters who are not male and not smiling. The game is designed to induce collaboration by making it impossible to correctly guess the final character without sharing clues. 

## To be able to play
Before launching the game, please modify Spyder settings so that your graphics are interactive:
```python > Preferences > IPython console > Graphics```.
In “Graphics backend” select “Automatic” instead of “Inline”. 

## In case you encountered an issue to run the game
Type in the Spyder terminal (bottom right) to install the following libraries: 

```
pip install matplotlib
pip install imageio
pip install imageio.v2 [PC only]
pip install pygame
pip install button
```

Caution: You may have a message error saying that no button function is found in the folder. So you will need to go in the following path: 
```/Users/[YOUR_NAME]/opt/anaconda3/envs/guess-brain-game/lib/python3.9/site-packages/button/__init__.py```

Remove first two lines from the file:
```
from . import utils
from . import tasks
```

And copy/paste the following code in the ```__init__.py``` file: 
```
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
```
Once done, save changes to ``` __init__.py``` file. 

Credit for the buttons menu: https://github.com/baraltech/Menu-System-PyGame/blob/main/button.py.



  
