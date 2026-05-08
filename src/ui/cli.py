from typing import List

from src.types import BoardPosition, Stone
from src.config import BOARD_SIZE


class CLI:
    def render_board(self, board: List[List[Stone]]) -> str:
        lines = []
        header = "   " + " ".join(chr(ord("A") + i) for i in range(BOARD_SIZE))
        lines.append(header)
        for row_idx, row in enumerate(board):
            row_num = row_idx + 1
            row_str = f"{row_num:2d} " + " ".join(stone.value[0].upper() for stone in row)
            lines.append(row_str)
        return "\n".join(lines)

    def parse_move(self, input_str: str) -> BoardPosition | None:
        input_str = input_str.strip().upper()
        if len(input_str) < 2:
            return None
        col_char = input_str[0]
        row_str = input_str[1:]
        if col_char < "A" or col_char >= chr(ord("A") + BOARD_SIZE):
            return None
        try:
            row = int(row_str) - 1
        except ValueError:
            return None
        if row < 0 or row >= BOARD_SIZE:
            return None
        col = ord(col_char) - ord("A")
        return BoardPosition(row=row, col=col)

    def get_user_input(self, prompt: str) -> str:
        return input(prompt)

    def display_message(self, msg: str) -> None:
        print(msg)
