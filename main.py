import random
from random import randint
import copy


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Точка находится вне доски!'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'В эту точку уже стреляли!'


class DotIsWrong(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, length):
        self.length = length
        self.first_dot = Dot(randint(0, 5), randint(0, 5))
        self.orient = random.choice(['vert', 'hor'])
        self.qua_of_lives = length

    def dots(self):
        list_of_dots = []
        for i in range(self.length):
            cur_x = self.first_dot.x
            cur_y = self.first_dot.y
            if self.orient == 'vert':
                cur_x += i
            else:
                cur_y += i
            list_of_dots.append(Dot(cur_x, cur_y))
        return list_of_dots


class Board:
    def __init__(self, hid):
        self.status_of_dots = [['o', 'o', 'o', 'o', 'o', 'o'],
                               ['o', 'o', 'o', 'o', 'o', 'o'],
                               ['o', 'o', 'o', 'o', 'o', 'o'],
                               ['o', 'o', 'o', 'o', 'o', 'o'],
                               ['o', 'o', 'o', 'o', 'o', 'o'],
                               ['o', 'o', 'o', 'o', 'o', 'o']]
        self.list_of_ships = []
        self.hid = hid
        self.qua_of_alive_ships = 7

    def add_ship(self, length):
        new_ship = Ship(length)
        for dot in new_ship.dots():
            if self.out(dot):
                raise DotIsWrong
            else:
                for ship in self.list_of_ships:
                    if dot in ship.dots():
                        raise DotIsWrong
                    if dot in self.contour(ship):
                        raise DotIsWrong
        self.list_of_ships.append(new_ship)
        for dot in new_ship.dots():
            self.status_of_dots[dot.x][dot.y] = '■'

    def contour(self, ship):
        list_of_engaged_dots = []
        for dot in ship.dots():
            list_of_engaged_dots.append(Dot(dot.x + 1, dot.y))
            list_of_engaged_dots.append(Dot(dot.x - 1, dot.y))
            list_of_engaged_dots.append(Dot(dot.x, dot.y + 1))
            list_of_engaged_dots.append(Dot(dot.x, dot.y - 1))
            list_of_engaged_dots.append(Dot(dot.x + 1, dot.y + 1))
            list_of_engaged_dots.append(Dot(dot.x - 1, dot.y - 1))
            list_of_engaged_dots.append(Dot(dot.x + 1, dot.y - 1))
            list_of_engaged_dots.append(Dot(dot.x - 1, dot.y + 1))
        return list_of_engaged_dots

    def output_board(self):

        def output(board):
            print('   | 1 | 2 | 3 | 4 | 5 | 6 |')
            for i in range(6):
                print(i + 1, ' |', end='')
                for j in range(6):
                    print('', board[i][j], '|', end='')
                print()

        if self.hid:
            new_board = copy.deepcopy(self.status_of_dots)
            for i in range(6):
                for j in range(6):
                    if new_board[i][j] == '■':
                        new_board[i][j] = 'o'
            print('Доска компьютера:')
            output(new_board)
        else:
            print('Ваша доска:')
            output(self.status_of_dots)

    @staticmethod
    def out(dot):
        if -1 < dot.x < 6 and -1 < dot.y < 6:
            return False
        else:
            return True

    def check_shoted(self, dot):
        if self.status_of_dots[dot.x][dot.y] == 'x' or self.status_of_dots[dot.x][dot.y] == 'T':
            return True

    def shot(self, dot):
        if self.status_of_dots[dot.x][dot.y] == 'o':
            self.status_of_dots[dot.x][dot.y] = 'T'
            print('Промах!')
            return False
        elif self.status_of_dots[dot.x][dot.y] == '■':
            self.status_of_dots[dot.x][dot.y] = 'x'
            for ship in self.list_of_ships:
                for ship_dots in ship.dots():
                    if dot.__eq__(ship_dots):
                        ship.qua_of_lives -= 1
                        if ship.qua_of_lives == 0:
                            print('Убит!')
                            return True
                        else:
                            print('Ранен!')
                            return True



class Player:
    def __init__(self):
        self.board = Board(False)
        self.enemy_board = Board(True)

    def ask(self):
        pass

    def move(self):
        dot = None
        while dot is None:
            dot_check = self.ask()
            try:
                if Board.out(dot_check):
                    raise BoardOutException
                if self.enemy_board.check_shoted(dot_check):
                    raise BoardUsedException
            except BoardOutException:
                print('Точка находится вне доски!')
            except BoardUsedException:
                print('В эту точку уже стреляли!')
            else:
                dot = dot_check
        if self.enemy_board.shot(dot):
            return True
        else:
            return False




class AI(Player):
    def ask(self):
        dot = Dot(randint(0, 5), randint(0, 5))
        return dot


class User(Player):
    def ask(self):
        list_dot = list(map(int, input(f'Введите координаты выстрела через пробел: ').split(' ')))
        dot = Dot(list_dot[0] - 1, list_dot[1] - 1)
        return dot


class Game:
    def __init__(self):
        self.user = User()
        self.user_board = self.random_board(False)
        self.ai = AI()
        self.ai_board = self.random_board(True)

    def random_board(self, hid):
        new_board = None
        while new_board is None:
            new_board = self.random_ships(hid)
        return new_board

    def random_ships(self, hid):
        new_board = Board(hid)
        ships = [3, 2, 2, 1, 1, 1, 1]
        for len in ships:
            qua_of_att = 0
            while True:
                qua_of_att += 1
                if qua_of_att > 2500:
                    return None
                try:
                    new_board.add_ship(len)
                    break
                except DotIsWrong:
                    pass
        return new_board

    def greet(self):
        print('Добро пожаловать в игру "Морской бой"!')
        print('--------------------------------------')
        print('Ваша задача - выбить все корабли компьютера')

    def loop(self):

        def check_win(board):
            qua_of_dead = 0
            for ship in board.list_of_ships:
                if ship.qua_of_lives == 0:
                    qua_of_dead += 1
            if qua_of_dead == 7:
                return False
            else:
                return True

        self.user.board = self.user_board
        self.user.enemy_board = self.ai_board
        self.ai.board = self.ai_board
        self.ai.enemy_board = self.user_board
        user_move = True
        while check_win(self.user_board) and check_win(self.ai_board):
            self.user_board.output_board()
            self.ai_board.output_board()
            if user_move:
                if self.user.move():
                    continue
                else:
                    user_move = False
                    continue
            else:
                if self.ai.move():
                    continue
                else:
                    user_move = True
                    continue
        if user_move:
            print('Игра окончена, победил игрок!')
        else:
            print('Игра окончена, победил компьютер!')

    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()
