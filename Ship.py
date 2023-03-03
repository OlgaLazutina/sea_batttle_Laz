from random import randint

class ExcepBoard(Exception):
    pass
class BoardOut(ExcepBoard):
    def __str__(self):
        return "Мимо доски, кэп!"
class BoardUsed(ExcepBoard):
    def __str__(self):
        return "Такой выстрел уже был, кэп!"
class BoardWrongShip(ExcepBoard): #исключения, чтобы нормально размещать корабли, без извешения пользователя
    pass

class Dot():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship():
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.o == 0:
                cur_x += i
            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooting(self, shoot):
        return shoot in self.dots


class Board():
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size

        self.count = 0

        self.field = [['o'] * size for _ in range(size)]
        self.buzy = [] # список отстреляных точек
        self.ships = [] # список  точек корбаля
#здесь мы выводим игровое поле
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):

            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("x", "o") #не понимаю что это такое и ка оно работает
        return res
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))
    #метод выстрела
    def shot(self, d):
        if self.out(d):
            raise BoardOut()#"Мимо доски, кэп!"

        if d in self.buzy:
            raise BoardUsed()#"Такой выстрел уже был, кэп!"
        self.buzy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contur(ship, verd = True)
                    print('Минус корабль, кэп!')
                    return False
                else:
                    print('Есть подбитие, кэп!')
                    return True
        self.field[d.x][d.y] = '.'
        print("Промазали, кэп!")
        return False
    def begin(self):
        self.buzy = []


    # здесь мы обозначаем поле в котром нельзя ставить
    # другие корбали, согласно правилу кучности
    def contur(self, ship, verb = False):
        near = [
            (-1,-1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y +dy)
                self.field [cur.x] [cur.y] = "*"
                if not(self.out (cur)) and cur not in self.buzy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                        self.buzy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.buzy:
                raise BoardWrongShip()
        for d in ship.dots:
            self.field[d.x][d.y] = "x"
            self.buzy.append(d)

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

class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShip:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()


