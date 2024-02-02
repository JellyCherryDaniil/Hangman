from random import choice
# GAME_THEME = "Животное"
# test_tuple = (1, 2, 3, 4,"Hello", True)
# test_tuple

WORDS_TUPLE = (
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "АРГОН"),
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "АСТАТ"),
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "БАРИЙ"),
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "БОРИЙ"),
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "ГЕЛИЙ"),
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "ИНДИЙ"),
)


class HangmanGame:
    """
    Описывает класс игры виселицы
    """
    def __init__(self, difficulty=1, ):
        self.health = 5
        self.started = False
        self.word = ""
        self.theme = ""
        self.answer = ""

    def start(self):
        """
        Запуск игры
        :return:
        """
        self.started = True
        self.health = 5
        question_word = choice(WORDS_TUPLE)
        self.theme = question_word[0]
        self.answer = question_word[1]
        self.word = "#" * len(self.answer)

    def guess(self, symbol):
        if symbol in self.answer:
            new_word = list(self.word)
            for index in range(len(self.answer)):
                if self.answer[index] == symbol:
                    new_word[index] = symbol
            self.word = "".join(new_word)
        else:
            self.health -= 1
            if self.health == 0:
                self.game_over()

    def game_over(self):
        self.started = False
        self.health = 0

