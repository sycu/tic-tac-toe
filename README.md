# TicTacToe AI
Simple Python TicTacToe game with Minimax and Alpha-Beta algorithms 

## Dependencies
```shell script
pip install -r requirements.txt
```

## Configuration
At the bottom of tictactoe.py file there are two lines which configure players' strategies:
```python
player_1_input = UserInput()
player_2_input = AlphaBetaInput()
```

Possible classes are:
- UserInput - controlled by user
- MinimaxInput - Minimax algorithm
- AlphaBetaInput - Minimax with Alpha-Beta pruning

## Usage
```python
python tictactoe.py
```
