class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardExcept as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера {d.x + 1} {d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход, кэп: ").split()

            if len(cords) != 2:
                print("нужны две координаты!")
                continue
            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Нужны числа!")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)
