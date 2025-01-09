# Treasure Hunt Bayesian Game

An interactive treasure-hunting game built in Python, featuring a probabilistic approach using Bayesian Networks. Players strategically detect and analyze probabilities to locate a hidden treasure on a grid, aiming to conserve points and win the game.

## Features
- **Bayesian Network Integration**: Dynamically updates probabilities of treasure location based on player actions.
- **Signal Detection**: Probe cells on the grid to receive probabilistic signals influenced by the treasure's location.
- **Interactive Gameplay**: A graphical user interface (GUI) built with `tkinter` for an intuitive and engaging experience.
- **Dynamic Scoring**: Lose points with each detection, challenging players to optimize their moves.
- **Win/Loss Conditions**: Players win by digging in the correct cell or lose when they run out of points.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/treasure-hunt-bayesian-game.git
   cd treasure-hunt-bayesian-game
   ```
2. Install dependencies (requires Python 3.7+):
- `pip install -r requirements.txt`
3. Run the game:
- `python main.py`
4. Change grid size:
- Go into modules/config.yaml and change the rows + columns

## How to Play

1. Start the game by running main.py
2. Detect Mode:
    - Click on a cell to detect signals about the treasure's location.
    - Signal Strenghts:
      - + : Green
      - ++ : Yellow
      - +++ : Orange
      - ++++ : Red
3. Dig Mode:
    - Confident about the location? Switch to "Dig Mode" and click a cell to attempt finding the treasure.
4. Win by successfully digging the treasure or lose when your points run out!

## Game Logic

- Each Detection updates the probabilities for all grid cells based on the bayesian Networks
- The Bayesian Network uses Conditional Probability Tables (CPTs) based on the Chebyshev distance between the treasure and each grid cell.

## Acknowledgments
This project was developed as part of an academic assignment to integrate Bayesian reasoning into an interactive application.

## License 
This project is licensed under the MIT License.

## Enjoy the challenge of probabilistic treasure hunting!
Let me know if you need additional details or modifications!






