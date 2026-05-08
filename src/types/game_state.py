from dataclasses import dataclass
from typing import List

from .stone import Stone


@dataclass
class GameState:
    board: List[List[Stone]]
    current_player: Stone
    winner: Stone | None
    is_game_over: bool
