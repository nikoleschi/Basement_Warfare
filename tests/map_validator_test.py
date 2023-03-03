import unittest
from map_validator import *


class TestExceptions(unittest.TestCase):
    def test_type_exception_is_subclass_of_exception(self):
        self.assertTrue(issubclass(TypeException, Exception))

    def test_map_exception_is_subclass_of_exception(self):
        self.assertTrue(issubclass(MapException, Exception))

    def test_map_size_exception_is_subclass_of_map_exception(self):
        self.assertTrue(issubclass(MapSizeException, MapException))

    def test_invalid_character_exception_is_subclass_of_map_exception(self):
        self.assertTrue(issubclass(InvalidCharacterException, MapException))

    def test_map_border_exception_is_subclass_of_map_exception(self):
        self.assertTrue(issubclass(MapBorderException, MapException))

    def test_player_count_exception_is_subclass_of_map_exception(self):
        self.assertTrue(issubclass(PlayerCountException, MapException))

    def test_player_box_exception_is_subclass_of_map_exception(self):
        self.assertTrue(issubclass(PlayerBoxException, MapException))

    def test_player_missing_exception_is_subclass_of_map_exception(self):
        self.assertTrue(issubclass(PlayerMissingException, MapException))

    def test_no_path_between_players_exception_is_subclass_of_map_exception(self):
        self.assertTrue(issubclass(NoPathBetweenPlayersException, MapException))


class TestMapValidator(unittest.TestCase):
    def test_valid_map(self):
        map_validator = MapValidator('test_maps/valid_map.txt')
        self.assertTrue(map_validator.valid)

    def test_invalid_file_type(self):
        map_validator = MapValidator('test_maps/invalid_type_map.bmp')
        self.assertFalse(map_validator.valid)
        self.assertEqual(str(TypeException()), map_validator.error_message)

    def test_invalid_map_size(self):
        map_validator = MapValidator('test_maps/invalid_map_size.txt')
        self.assertFalse(map_validator.valid)
        self.assertEqual(str(MapSizeException()), map_validator.error_message)

    def test_invalid_character(self):
        map_validator = MapValidator('test_maps/invalid_character.txt')
        self.assertFalse(map_validator.valid)
        self.assertEqual(str(InvalidCharacterException()), map_validator.error_message)

    def test_invalid_border(self):
        map_validator = MapValidator('test_maps/invalid_border.txt')
        self.assertFalse(map_validator.valid)
        self.assertEqual(str(MapBorderException()), map_validator.error_message)

    def test_multiple_players(self):
        map_validator = MapValidator('test_maps/multiple_players.txt')
        self.assertFalse(map_validator.valid)
        self.assertEqual(str(PlayerCountException(PLAYER_1)), map_validator.error_message)

    def test_invalid_player_box(self):
        map_validator = MapValidator('test_maps/invalid_player_box.txt')
        self.assertFalse(map_validator.valid)
        self.assertEqual(str(PlayerBoxException()), map_validator.error_message)

    def test_missing_player(self):
        map_validator = MapValidator('test_maps/missing_player.txt')
        self.assertFalse(map_validator.valid)
        self.assertEqual(str(PlayerMissingException(PLAYER_2)), map_validator.error_message)

    def test_no_path_between_players(self):
        map_validator = MapValidator('test_maps/no_path_between_players.txt')
        self.assertFalse(map_validator.valid)
        self.assertEqual(str(NoPathBetweenPlayersException()), map_validator.error_message)


if __name__ == '__main__':
    unittest.main()
