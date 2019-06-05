import json
from json import JSONDecodeError
from typing import Dict

from exceptions.GameStateFileException import GameStateFileException
from game_item.Item import Item
from game_item.Consumable import Consumable
from game_item.Weapon import Weapon
from game_item.Armour import Armour
from game_item.Creature import Creature
from game_item.Hero import Hero
from game_item.Room import Room
from game_item.EnvironmentObject import EnvironmentObject


class GameState:

    def __init__(self, file_path: str):
        try:
            self.game_data = self.read_file(file_path)

            self.rooms = self.create_dict(Room, 'rooms')
            self.creatures = self.create_dict(Creature, 'creatures')
            self.environment_objects = self.create_dict(EnvironmentObject, "environment_objects")
            self.items = self.create_item_dict('items')
            self.equipment = self.create_equipment_dict('equipment')
            self.hero = self.create_hero()
        except GameStateFileException as e:
            raise GameStateFileException(e)

    def create_dict(self, type, key_name) -> Dict[str, any]:
        try:
            objects = dict()
            rooms_data = self.game_data[key_name]
            for key, value in rooms_data.items():
                object = type(value)
                objects[key] = object
            return objects
        except KeyError as e:
            raise GameStateFileException(f"Failed to read {key_name} data: cannot find key {e}")

    def create_item_dict(self, key_name):
        try:
            objects = dict()
            data = self.game_data[key_name]["regular"]
            for key in data:
                object = Item(data[key])
                objects[key] = object
            data = self.game_data[key_name]["consumable"]
            for key in data:
                object = Consumable(data[key])
                objects[key] = object
            return objects
        except KeyError as e:
            raise GameStateFileException(f"Failed to read {key_name} data: cannot find key {e}")

    def create_equipment_dict(self, key_name):
        try:
            objects = dict()
            data = self.game_data[key_name]["weapons"]
            for key in data:
                object = Weapon(data[key])
                objects[key] = object
            data = self.game_data[key_name]["armour"]
            for key in data:
                object = Armour(data[key])
                objects[key] = object
            return objects
        except KeyError as e:
            raise GameStateFileException(f"Failed to read {key_name} data: cannot find key {e}")

    def create_hero(self) -> Hero:
        try:
            hero_data = self.game_data['hero']
            return Hero(hero_data)
        except KeyError as e:
            raise GameStateFileException(f"Failed to read hero data: cannot find key {e}")

    @staticmethod
    def read_file(file_path) -> Dict[str, dict]:
        try:
            with open(file_path, encoding='utf-8') as config_file:
                game_data = json.load(config_file)
            return game_data
        except IOError as e:
            raise GameStateFileException(f"Failed to read file: {e}")
        except JSONDecodeError as e:
            raise GameStateFileException(f"Failed to parse JSON file: {e}")
