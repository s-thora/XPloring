import contextlib
import io
import unittest

from GameState import GameState
from InputHandler import InputHandler


class TestAttack(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.ih1 = InputHandler(self.game_state1)

        self.map_capital_alias = '../game_states/game_capital_alias.json'
        self.game_state_capital_alias = GameState(self.map_capital_alias)
        self.ih_capital_alias = InputHandler(self.game_state_capital_alias)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

        del self.game_state1
        del self.ih1

        del self.game_state_capital_alias
        del self.ih_capital_alias

    def test_attack(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attack")
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attack envelope")
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attack bandage")
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the bandage.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attack sword")
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the sword.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attack helmet")
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the helmet.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attack west")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the west.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_creature(self):
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attack dragon")
        result_output = stdout.getvalue()
        expected_output = "You hit the green dragon for 1 damage! Green dragon has 59 HP left.\n" \
                          "Green dragon hit you for 10 damage! You have 90 HP left.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attack inventory")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_key(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("take chestplate")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("equip sword")
        self.ih.handle_user_input("equip chestplate")
        self.ih.handle_user_input("go west")
        self.ih.handle_user_input("attack dragon")
        self.ih.handle_user_input("attack dragon")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attack key")
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the key.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("attack key")
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_door(self):
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attack door")
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the door.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_door_ambiguous(self):
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("attack door")
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    # TESTS ON DIFFERENT CASES

    # creature

    def test_alias_capital_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("attack Green Dragon")
        result_output = stdout.getvalue()
        expected_output = "You hit the Green Dragon for 1 damage! " \
                          "Green Dragon has 49 HP left.\n" \
                          "Green Dragon hit you for 10 damage! " \
                          "You have 90 HP left.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("attack green dragon")
        result_output = stdout.getvalue()
        expected_output = "You hit the Green Dragon for 1 damage! " \
                          "Green Dragon has 49 HP left.\n" \
                          "Green Dragon hit you for 10 damage! " \
                          "You have 90 HP left.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_capital_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("attack green Dragon")
        result_output = stdout.getvalue()
        expected_output = "You hit the Green Dragon for 1 damage! " \
                          "Green Dragon has 49 HP left.\n" \
                          "Green Dragon hit you for 10 damage! " \
                          "You have 90 HP left.\n"
        self.assertEqual(expected_output, result_output)
