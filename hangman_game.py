from random import choice
# GAME_THEME = "Животное"
# test_tuple = (1, 2, 3, 4,"Hello", True)
# test_tuple
HANGMAN1_STR = (
    "        $$$$$$$$$$$$$$$\n"
    "        |             $\n"
    "        |             $\n"
    "        |             $\n"
    "        |             $\n"
    "                      $\n"
    "                      $\n"
    "                      $\n"
    "                      $\n"
    "                      $\n"
    "                      $\n"
    " $$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
    " $                          $\n"
)
HANGMAN2_STR = (
    "        $$$$$$$$$$$$$$$\n"
    "        |             $\n"
    "        |             $\n"
    "        |             $\n"
    "        |             $\n"
    "        O             $\n"
    "                      $\n"
    "                      $\n"
    "                      $\n"
    "                      $\n"
    "                      $\n"
    " $$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
    " $                          $\n"
)
HANGMAN3_STR = (
    "        $$$$$$$$$$$$$$$\n"
    "        |             $\n"
    "        |             $\n"
    "        |             $\n"
    "        |             $\n"
    "        O             $\n"
    "      /   \\           $\n"
    "                      $\n"
    "                      $\n"
    "                      $\n"
    "                      $\n"
    " $$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
    " $                          $\n"
)
HANGMAN4_STR = (
    "        $$$$$$$$$$$$$$$\n"
    "        |             $\n"
    "        |             $\n"
    "        |             $\n"
    "        |             $\n"
    "        O             $\n"
    "      / | \\           $\n"
    "        |             $\n"
    "                      $\n"
    "                      $\n"
    "                      $\n"
    " $$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
    " $                          $\n"
)
HANGMAN5_STR = (
    "        $$$$$$$$$$$$$$$\n"
    "        |             $\n"
    "        |             $\n"
    "        |             $\n"
    "        |             $\n"
    "        O             $\n"
    "      / | \\           $\n"
    "        |             $\n"
    "       / \\            $\n"
    "                      $\n"
    "                      $\n"
    " $$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
    " $                          $\n"
)
WORDS_TUPLE = (
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "АРГОН"),
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "АСТАТ"),
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "БАРИЙ"),
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "БОРИЙ"),
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "ГЕЛИЙ"),
    ("ХИМИЧЕСКИЙ ЭЛЕМЕНТ", "ИНДИЙ"),
    ("ТКАНЬ", "АКРИЛ"),
    ("ТКАНЬ", "АТЛАС"),
    ("ТКАНЬ", "БАЙКА"),
    ("ТКАНЬ", "БАРЕЖ"),
    ("ТКАНЬ", "БУРЕТ"),
    ("ТКАНЬ", "ВЕЛЮР"),
    ("СОРТ СЫРА", "АНАРИ"),
    ("СОРТ СЫРА", "БАНОН"),
    ("СОРТ СЫРА", "БОФОР"),
    ("СОРТ СЫРА", "ВИОЛА"),
    ("СОРТ СЫРА", "ГАУДА"),
    ("СОРТ СЫРА", "ДАНБО"),
)


class HangmanGame:
    """
    Описывает класс игры виселицы


    attributes:

    health: Здоровье игрока
    word: Текущее слово
    theme: Тема слова
    answer: Загаданное слово
    status: Статус игры: подготовка, идет игра, ПОБЕДА, проиграли
    """
    def __init__(self, difficulty=1, ):
        self.health = 5
        self.started = False
        self.word = ""
        self.theme = ""
        self.answer = ""
        self.status = "подготовка"

    def start(self):
        """
        Запуск игры
        :return:
        """
        self.status = "идет игра"
        self.started = True
        self.health = 5
        question_word = choice(WORDS_TUPLE)
        self.theme = question_word[0].capitalize()
        self.answer = question_word[1].lower()
        self.word = "#" * len(self.answer)

    def guess(self, symbol) -> bool:
        """
        Метод для угадывания буквы
        :param symbol: буква, которую ввел игрок
        :return: Возвращает истину, если угадал букву, возвразает ложь, если не угадал.
        """
        if symbol in self.answer:
            new_word = list(self.word)
            for index, element in enumerate(self.answer):
                if element == symbol:
                    new_word[index] = symbol
            self.word = "".join(new_word)
            if "#" not in self.word:
                self.game_over("ПОБЕДА")
            return True
        else:
            self.health -= 1
            if self.health == 0:
                self.game_over("проиграли")
            return False

    def game_over(self, status="подготовка"):
        """
        Метод закачивает игру
        :return:
        """
        self.health = 0
        self.status = status

    def show_hangman(self):
        """
        Отрисовка висельника из символов
        :return:
        """

        match self.health:
            case 4:
                return HANGMAN1_STR
            case 3:
                return HANGMAN2_STR
            case 2:
                return HANGMAN3_STR
            case 1:
                return HANGMAN4_STR
            case 0:
                return HANGMAN5_STR

        return ""
