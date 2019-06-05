from src.Game import Game
from src.GameState import GameState


if __name__ == '__main__':

    map0 = '../game_states/game0_repr.json'
    game_state = GameState(map0)
    game = Game(game_state)
    game.run()
    # game.GUI.window.mainloop()
