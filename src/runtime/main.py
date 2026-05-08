from src.service import GameEngine
from src.ui import CLI


def main() -> None:
    engine = GameEngine()
    cli = CLI()
    while not engine.get_state().is_game_over:
        state = engine.get_state()
        cli.display_message(cli.render_board(state.board))
        cli.display_message(f"Current player: {state.current_player.value}")
        input_str = cli.get_user_input("Enter move (e.g., A1): ")
        position = cli.parse_move(input_str)
        if position is None:
            cli.display_message("Invalid move. Try again.")
            continue
        if not engine.make_move(position.row, position.col):
            cli.display_message("Invalid move. Try again.")
            continue
    state = engine.get_state()
    cli.display_message(cli.render_board(state.board))
    if state.winner:
        cli.display_message(f"Winner: {state.winner.value}")
    else:
        cli.display_message("Game over - draw")
