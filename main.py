from lib import Game, HumanController, AIController


def main():
    game = Game(clear_console=True)
    game.add_players(AIController, HumanController)
    # game.add_players(AIController, AIController)


    while True: 
        game.loop()
        response = str(input('Play again?Press (Y) to continue, else press anything else to quit. \n'))
        if response.lower() != 'y':
            break

    game.release()
    print('Shutting down')


if __name__ == '__main__':
    main()