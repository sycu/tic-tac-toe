import pygame
from typing import List, Optional, Tuple

Board = List[List[Optional[int]]]
Position = Tuple[int, int]
INFINITY = 1000000  # Actually anything greater than 1 will work, as the only possible scores are -1, 0 and 1


class PlayerInput:
    def move(self, window: pygame.Surface, board: Board, player: int) -> Position:
        raise NotImplemented()


class UserInput(PlayerInput):
    def move(self, window: pygame.Surface, board: Board, player: int) -> Position:
        clock = pygame.time.Clock()
        while True:
            clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    col = x // (window.get_width() // 3)
                    row = y // (window.get_height() // 3)

                    if not board[row][col]:
                        return col, row


class AlphaBetaInput(PlayerInput):
    def move(self, window: pygame.Surface, board: Board, player: int) -> Position:
        best_score = -INFINITY
        best_move = (0, 0)

        for y in range(3):
            for x in range(3):
                if board[y][x] is None:
                    board[y][x] = player
                    score = self.__alpha_beta(board, player, False, -INFINITY, INFINITY)
                    board[y][x] = None
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        return best_move

    def __alpha_beta(self, board: Board, player: int, maximizing: bool, alpha: int, beta: int) -> int:
        winner = TicTacToe.get_winner(board)
        if winner is not None:
            if winner == 0:
                return 0
            else:
                return 1 if winner == player else -1

        best_score = -INFINITY if maximizing else INFINITY
        get_best_score = max if maximizing else min

        for y in range(3):
            for x in range(3):
                if board[y][x] is None:
                    board[y][x] = player if maximizing else player % 2 + 1
                    score = self.__alpha_beta(board, player, not maximizing, alpha, beta)
                    board[y][x] = None
                    best_score = get_best_score(score, best_score)

                    if maximizing and score > alpha:
                        alpha = score
                    elif not maximizing and score < beta:
                        beta = score

                    if alpha > beta:
                        return best_score

        return best_score


class MinimaxInput(PlayerInput):
    def move(self, window: pygame.Surface, board: Board, player: int) -> Position:
        best_score = -INFINITY
        best_move = (0, 0)

        for y in range(3):
            for x in range(3):
                if board[y][x] is None:
                    board[y][x] = player
                    score = self.__minimax(board, player, False)
                    board[y][x] = None
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        return best_move

    def __minimax(self, board: Board, player: int, maximizing: bool) -> int:
        winner = TicTacToe.get_winner(board)
        if winner is not None:
            if winner == 0:
                return 0
            else:
                return 1 if winner == player else -1

        best_score = -INFINITY if maximizing else INFINITY
        get_best_score = max if maximizing else min

        for y in range(3):
            for x in range(3):
                if board[y][x] is None:
                    board[y][x] = player if maximizing else player % 2 + 1
                    score = self.__minimax(board, player, not maximizing)
                    board[y][x] = None
                    best_score = get_best_score(score, best_score)

        return best_score


class TicTacToe:
    BACKGROUND_COLOR = (86, 113, 18)
    LINE_COLOR = (57, 87, 1)
    LINE_WIDTH = 10
    PLAYER_1_COLOR = (250, 86, 42)
    PLAYER_2_COLOR = (233, 160, 0)

    def __init__(self, window_size: Tuple[int, int], player_1_input: PlayerInput, player_2_input: PlayerInput):
        self.window_size = window_size
        self.player_1_input = player_1_input
        self.player_2_input = player_2_input

    def play(self) -> None:
        pygame.init()
        window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('TicTacToe')

        board = [[None for x in range(3)] for y in range(3)]
        current_player = 1

        while TicTacToe.get_winner(board) is None:
            self.__redraw(window, board)

            player_input = self.player_1_input if current_player == 1 else self.player_2_input
            x, y = player_input.move(window, board, current_player)
            if board[y][x] is not None:
                raise Exception('Invalid move')

            board[y][x] = current_player

            current_player = current_player % 2 + 1

        self.__redraw(window, board)
        return TicTacToe.get_winner(board)

    @staticmethod
    def get_winner(board: Board) -> Optional[int]:
        # Rows
        for y in range(3):
            if board[y][0] and board[y][0] == board[y][1] == board[y][2]:
                return board[y][0]

        # Cols
        for x in range(3):
            if board[0][x] and board[0][x] == board[1][x] == board[2][x]:
                return board[0][x]

        # Diagonals
        if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]

        if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]

        # Draw
        has_empty_field = False
        for y in range(3):
            for x in range(3):
                if not board[y][x]:
                    has_empty_field = True

        if not has_empty_field:
            return 0

        return None

    def __redraw(self, window: pygame.Surface, board: Board) -> None:
        window.fill(self.BACKGROUND_COLOR)
        height = window.get_height()
        width = window.get_width()

        field_height = height // 3
        field_width = width // 3

        # Horizontal lines
        pygame.draw.line(window, self.LINE_COLOR, (0, field_height), (width, field_height), self.LINE_WIDTH)
        pygame.draw.line(window, self.LINE_COLOR, (0, 2 * field_height), (width, 2 * field_height), self.LINE_WIDTH)

        # Vertical lines
        pygame.draw.line(window, self.LINE_COLOR, (field_width, 0), (field_width, height), self.LINE_WIDTH)
        pygame.draw.line(window, self.LINE_COLOR, (2 * field_width, 0), (2 * field_width, height), self.LINE_WIDTH)

        # Player fields
        for y in range(3):
            for x in range(3):
                field_player = board[y][x]

                if field_player == 1:
                    pygame.draw.circle(window, self.PLAYER_1_COLOR, (field_width * x + field_width // 2, field_height * y + field_height // 2), min(field_height, field_width) // 3, self.LINE_WIDTH)
                elif field_player == 2:
                    pygame.draw.line(window, self.PLAYER_2_COLOR, (field_width * x + field_width // 4, field_height * y + field_height // 4), (field_width * x + 3 * field_width // 4, field_height * y + 3 * field_height // 4), self.LINE_WIDTH)
                    pygame.draw.line(window, self.PLAYER_2_COLOR, (field_width * x + field_width // 4, field_height * y + 3 * field_height // 4), (field_width * x + 3 * field_width // 4, field_height * y + field_height // 4), self.LINE_WIDTH)

        pygame.display.update()


if __name__ == '__main__':
    player_1_input = UserInput()
    player_2_input = AlphaBetaInput()

    game = TicTacToe((600, 600), player_1_input, player_2_input)
    winner = game.play()

    print('Winner: %d' % winner)
