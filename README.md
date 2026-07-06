This is a game I have coded to develop a more hands-on understanding of reinforcement learning, specifically the ins and outs of Q tables. It was clearly too complex for a Q-learning agent, but I wanted to develop more hands-on familiarity before transitioning to a Deep Q Network agent. 

The game itself has barebones graphics as they were not at all the focus. The game can be played manually with on screen instructions for movement and score displayed on the top corner. No High Score saving has been implemented currently.

Closing the game window will end the program execution, even if the window appears empty.

Prompts:
- Total Rounds: number of rounds (played until death) for the agent to complete
- Shown Round Interval: most rounds will be played silently by the agent for speed and performance, but this determines every nth round will be displayed on screen to allow for visual 
- Observed Rounds after Total finished: Agent plays n rounds after Total Rounds completed, with all additional rounds displayed on screen to develop sense of agent behavior after training
- Mid Status Print interval: Establishes interval at which agent average score will be printed, allowing for confirmation of Agent progress, especially useful during longer training sessions
