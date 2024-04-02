from dataclasses import dataclass, field

from hangman_game import HangmanGame


@dataclass
class GameManager:
    games: dict = field(default_factory=dict)

    def create_game(self, game_id):
        """

        :param game_id:
        :return:
        """
        # game_status = "начало"
        game = HangmanGame()
        game.start()
        self.games[game_id] = game
        return game

    def remove_game(self, game_id):
        """

        :param game_id:
        :return:
        """
        self.games.pop(game_id)
        # del self.games[game_id]

    def __getitem__(self, index):

        return self.games.get(index)

    def get_game(self, game_id):
        return self.__getitem__(game_id)

    def stop_game(self,game_id):
        game: HangmanGame = self.games[game_id]
        game.game_over()

    def restart_game(self,game_id):
        game: HangmanGame = self.games[game_id]
        game.start()
