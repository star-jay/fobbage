Fobbage is a quiz game in which there is a different approach than the usual question and answer. 
A fobbage quiz consists of the following loop:

- A quiz consists of multiple rounds in which each round consists of multiple questions.
- A single round is gone through two times. 
    - The first time players go through a round, the players make up a plausible answer to every question. This is called a **Bluff**.
    - After the first loop over all the questions, the game master resets the round and starts again from question 1.
    - This time around, the players see multiple choice answers: all the bluffs of every player from the first time around **with the real answer mixed in**. Players have to guess the real answer, this is called the **Guess**. Players can also give **Likes** to answers they find fun or witty.
    - In the second loop over the questions, when all players have guessed, a rundown of every answer is done in which it is visible which players have guessed which answer and thus which players has deceived other players.
- Scoring:
    - Every time a player guesses the right answer out of the multiple choice, they receive 1000 points
    - For every other player that Guesses on a Player's Bluff, the Owner of the Bluff gains 500 points. Guessing on your own Bluff results in 0 points, even if other players have guessed your bluff too.
    
- The quiz has two modes: Player and Host
    - As a Player you only get to Bluff or Guess on your device. What stage you are in is decided by polling the server constantly. We do not use websockets.
    - As a Host, you decide on the main screen (probably projected on a big screen or tv) what goes next. You decide when to progress to the next question and when a round goes into phase 2 (when the guessing starts). 