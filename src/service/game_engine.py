from typing import List

from src.types import GameState, Stone
from src.config import BOARD_SIZE, WIN_COUNT


class GameEngine:
    def __init__(self) -> None:
        self._board: List[List[Stone]] = [
            [Stone.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]
        self._current_player = Stone.BLACK
        self._winner: Stone | None = None
        self._is_game_over = False

    def make_move(self, row: int, col: int) -> bool:
        if not self.is_valid_position(row, col) or self._is_game_over:
            return False
        self._board[row][col] = self._current_player
        if self.check_winner(row, col, self._current_player):
            self._winner = self._current_player
            self._is_game_over = True
        elif self.is_board_full():
            self._is_game_over = True
        else:
            self._current_player = (
                Stone.WHITE if self._current_player == Stone.BLACK else Stone.BLACK
            )
        return True

    def check_winner(self, row: int, col: int, stone: Stone) -> bool:
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]
        for dr, dc in directions:
            count = 1
            count += self._count_direction(row, col, dr, dc, stone)
            count += self._count_direction(row, col, -dr, -dc, stone)
            if count >= WIN_COUNT:
                return True
        return False

    def _count_direction(
        self, row: int, col: int, dr: int, dc: int, stone: Stone
    ) -> int:
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self._board[r][c] == stone:
            count += 1
            r += dr
            c += dc
        return count

    def get_state(self) -> GameState:
        return GameState(
            board=self._board,
            current_player=self._current_player,
            winner=self._winner,
            is_game_over=self._is_game_over,
        )

    def is_valid_position(self, row: int, col: int) -> bool:
        if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
            return False
        return self._board[row][col] == Stone.EMPTY

    def is_board_full(self) -> bool:
        for row in self._board:
            for stone in row:
                if stone == Stone.EMPTY:
                    return False
        return True
