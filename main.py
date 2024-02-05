from hangman_game import HangmanGame


def main():
    """
    Точка входа в приложение
    :return:
    """
    while True:
        game_over = False
        game = HangmanGame()
        game.start()
        print("Игра начинается \n"
              f"Тема игры: {game.theme}\n"
              f"Отгадайте слово: {game.word}")
        while not game_over:
            symbol = input("Введите букву: \n")
            if len(symbol) == 1 and symbol.isalpha():
                symbol = symbol.lower()
                if game.guess(symbol):
                    print(game.word)
                else:
                    print("Вы не угадали\n"
                          f"Слово: {game.word}\n")
                    print(game.show_hangman())

                if game.status == "ПОБЕДА":
                    print("\nВы выиграли")
                    game_over = True
                elif game.status == "проиграли":
                    print("\nВы проиграли")
                    game_over = True

            else:
                print("Введите, пожалуйста, только одну букву!")


if __name__ == "__main__":
    main()
