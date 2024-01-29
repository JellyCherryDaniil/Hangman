from hangman_game import GAME_THEME


def main():
    """
    Точка входа в приложение
    :return:
    """
    game_over = False
    print("Игра начинается \n"
          f"Тема игры: {GAME_THEME}")

    while not game_over:
        symbol = input("Введите букву: \n")
        if len(symbol) == 1 and symbol.isalpha():
            ...
        else:
            print("Введите, пожалуйста, только одну букву!")


if __name__ == "__main__":
    main()
