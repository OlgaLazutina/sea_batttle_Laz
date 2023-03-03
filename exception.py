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
