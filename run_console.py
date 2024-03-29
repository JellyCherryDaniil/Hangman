from hangman_game import HangmanGame

def play_hangman(symbol, game, is_symbol) -> bool:
    """

    Шаг игры Hangman
    :param symbol: Загаданное слово или буква
    :param game: объект типа HangmanGame
    :param is_symbol: является ли введёное буквой
    :return: возвращает результат игры
    """

    if is_symbol:
        guess_function = game.guess
    else:
        guess_function = game.guess_word

    if guess_function(symbol):
        print(game.word)
    else:
        print("Вы не угадали\n"
              f"Слово:{game.word}\n")
        print(game.show_hangman())

    if game.status == "ПОБЕДА":
        print("\nВы выиграли")
        return True
    elif game.status == "проиграли":
        print("\nВы проиграли")
        return True
    return False


def main():
    """
    Точка входа в приложение
    :return:
    """
    programm_over = False
    while not programm_over:
        game_over = False
        game = HangmanGame()
        game.start()
        print("\n------------------------------\n"
              "Игра начинается \n"
              f"Тема игры: {game.theme}\n"
              f"Отгадайте слово: {game.word}")
        while not game_over:
            symbol = input("Введите букву или слово целиком:\n")
            symbol = symbol.lower()

            if len(symbol) == 1 and symbol.isalpha():
                game_over = play_hangman(symbol, game, True)
            elif len(symbol) > 1 and symbol.isalpha():
                game_over = play_hangman(symbol, game, False)
            else:
                print("Введите, пожалуйста, букву или целое слово!")
        continuation = input("Хотите продолжить? (Введите да, чтобы продолжить)\n")
        continuation = continuation.lower()
        if continuation != "да":
            programm_over = True




if __name__ == "__main__":
    main()
