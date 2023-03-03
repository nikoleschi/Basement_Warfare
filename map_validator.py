from others import get_file_type
from settings import *


class TypeException(Exception):
    def __str__(self):
        return 'Invalid file type!'


class MapException(Exception):
    def __str__(self):
        return 'Invalid map!'


class MapSizeException(MapException):
    def __str__(self):
        return super().__str__() + ' Map size should be 28x14!'


class InvalidCharacterException(MapException):
    def __str__(self):
        return super().__str__() + " Map should contain only these characters - '#', 'c', '1', '2', 'm' or whitespace!"


class MapBorderException(MapException):
    def __str__(self):
        return super().__str__() + " Border of the map must be always filled with walls ('#')!"


class PlayerCountException(MapException):
    def __init__(self, player):
        self.player = player

    def __str__(self):
        return super().__str__() + f" There is more than one player from '{self.player}'!"


class PlayerBoxException(MapException):
    def __str__(self):
        return super().__str__() + " Player indetication should be 2x2 box with one of '1' or '2'!"


class PlayerMissingException(MapException):
    def __init__(self, player):
        self.player = player

    def __str__(self):
        return super().__str__() + f" Player {self.player} is missing!"


class NoPathBetweenPlayersException(MapException):
    def __str__(self):
        return super().__str__() + " There is no path between players!"


class MapValidator:
    def __init__(self, map_path):
        self.path = map_path
        self.valid = True
        self.map_matrix = []
        try:
            self._validate()
        except (MapException, TypeException) as msg:
            self.error_message = str(msg)
            self.valid = False

    def _validate(self):
        self._check_file_type()
        self._validate_map()

    def _validate_map(self):
        with open(self.path) as file:
            self.map_layout = [line.strip('\n') for line in file]

        players = {
            PLAYER_1: False,
            PLAYER_2: False
        }
        if len(self.map_layout) != ROW_SIZE:
            raise MapSizeException()
        for row_index, row in enumerate(self.map_layout):
            row_list = []
            if len(row) != COL_SIZE:
                raise MapSizeException()
            for col_index, col in enumerate(row):
                if col not in ALL_SYMBOLS:
                    raise InvalidCharacterException()
                if row_index in HORIZONTAL_BORDER or col_index in VERTICAL_BORDER:
                    if col != WALL:
                        raise MapBorderException()
                if col in PLAYER_SYMBOLS:
                    if not players[col]:
                        player_coords = self._get_players_coords(row_index, col_index)
                        if not self._check_player_blocks(player_coords, col):
                            raise PlayerBoxException()
                        players[col] = player_coords
                    elif (row_index, col_index) not in players[col]:
                        raise PlayerCountException(col)
                row_list.append(BLANK_SPACE) if col != WALL else row_list.append(WALL)
            self.map_matrix.append(row_list)

        for player in players.keys():
            if not players[player]:
                raise PlayerMissingException(player)

        self._check_path(players[PLAYER_1][0], players[PLAYER_2][0])

    def _check_path(self, start, end):
        visited = set()
        stack = [start]

        while stack:
            current = stack.pop()
            if current == end:
                return
            visited.add(current)
            row, col = current
            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            for neighbor in neighbors:
                n_row, n_col = neighbor
                if (0 <= n_row < len(self.map_matrix) and 0 <= n_col < len(self.map_matrix[0]) and
                        self.map_matrix[n_row][n_col] != WALL and neighbor not in visited):
                    stack.append(neighbor)

        raise NoPathBetweenPlayersException()

    def _check_file_type(self):
        if get_file_type(self.path) != TXT_TYPE:
            raise TypeException()

    def _get_players_coords(self, x_index, y_index):
        return (x_index, y_index), (x_index, y_index + 1), (x_index + 1, y_index), (x_index + 1, y_index + 1)

    def _check_player_blocks(self, coords, player):
        for x, y in coords:
            if self.map_layout[x][y] != player:
                return False

        return True
