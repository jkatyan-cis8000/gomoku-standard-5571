# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- src/types/__init__.py: Type definitions exported at package level
- src/types/stone.py: Stone type (BLACK, WHITE, EMPTY)
- src/types/board_position.py: BoardPosition dataclass (row, col)
- src/types/game_state.py: GameState dataclass with board, current player, winner
- src/config/__init__.py: Config exports
- src/config/constants.py: BOARD_SIZE (15), WIN_COUNT (5)
- src/service/__init__.py: Service exports
- src/service/game_engine.py: GameEngine class - game logic, move validation, win detection
- src/ui/__init__.py: UI exports
- src/ui/cli.py: CLI class - board rendering, move input parsing
- src/runtime/__init__.py: Runtime exports
- src/runtime/main.py: Main entry point - game loop orchestration

## Interfaces

### Types Layer
- Stone: Enum with BLACK, WHITE, EMPTY values
- BoardPosition: dataclass with row: int, col: int
- GameState: dataclass with:
  - board: List[List[Stone]]
  - current_player: Stone
  - winner: Stone | None
  - is_game_over: bool

### Config Layer
- BOARD_SIZE: int = 15 (standard Gomoku board)
- WIN_COUNT: int = 5 (stones needed to win)

### Service Layer
- GameEngine class:
  - __init__(): Creates empty 15x15 board
  - make_move(row: int, col: int) -> bool: Attempt move, returns success
  - check_winner(row: int, col: int, stone: Stone) -> bool: Check if move wins
  - get_state() -> GameState: Returns current game state
  - is_valid_position(row: int, col: int) -> bool: Check bounds and empty
  - is_board_full() -> bool: Check for draw

### UI Layer
- CLI class:
  - render_board(board: List[List[Stone]]) -> str: Render board to string
  - parse_move(input_str: str) -> BoardPosition | None: Parse "A1" format
  - get_user_input(prompt: str) -> str: Read user input
  - display_message(msg: str) -> None: Print message to user

### Runtime Layer
- main(): Entry point that:
  - Creates GameEngine
  - Creates CLI
  - Loops until game_over
  - Handles user interaction
  - Reports winner

## Shared Data Structures

### BoardPosition
```python
@dataclass
class BoardPosition:
    row: int
    col: int
```

### GameState
```python
@dataclass
class GameState:
    board: List[List[Stone]]
    current_player: Stone
    winner: Stone | None
    is_game_over: bool
```

## External Dependencies

- No external dependencies required. Uses only Python standard library.
