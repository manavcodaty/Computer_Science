import math
import os
import random
import time
from typing import Dict, List

# ANSI color codes
COLORS = {
    "green": "\033[32m",
    "blue": "\033[34m",
    "yellow": "\033[33m",
    "red": "\033[31m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "reset": "\033[0m",
}


class Pokemon:
    def __init__(self, name: str, rarity: float, habitat: str):
        self.name = name
        self.rarity = rarity
        self.habitat = habitat
        self.caught = False


class World:
    def __init__(self, width: int = 60, height: int = 30):
        self.width = width
        self.height = height
        self.player_x = width // 2
        self.player_y = height // 2
        self.player_direction = 0  # 0: North, 90: East, 180: South, 270: West

        # Visual elements
        self.sprites = {
            "player": {
                0: f"{COLORS['red']}↑{COLORS['reset']}",
                90: f"{COLORS['red']}→{COLORS['reset']}",
                180: f"{COLORS['red']}↓{COLORS['reset']}",
                270: f"{COLORS['red']}←{COLORS['reset']}",
            },
            "terrain": {
                ".": f"{COLORS['green']}⋅{COLORS['reset']}",  # Grass
                "T": f"{COLORS['yellow']}♣{COLORS['reset']}",  # Tree
                "~": f"{COLORS['blue']}≈{COLORS['reset']}",  # Water
                "*": f"{COLORS['magenta']}❀{COLORS['reset']}",  # Flower
            },
        }

        # Game elements
        self.pokemon_list = [
            # Forest Pokemon
            Pokemon("Pidgey", 0.3, "forest"),
            Pokemon("Caterpie", 0.3, "forest"),
            Pokemon("Weedle", 0.3, "forest"),
            Pokemon("Bulbasaur", 0.05, "forest"),
            # Grass Pokemon
            Pokemon("Rattata", 0.3, "grass"),
            Pokemon("Oddish", 0.2, "grass"),
            Pokemon("Bellsprout", 0.2, "grass"),
            Pokemon("Pikachu", 0.05, "grass"),
            # Water Pokemon
            Pokemon("Magikarp", 0.4, "water"),
            Pokemon("Psyduck", 0.2, "water"),
            Pokemon("Poliwag", 0.2, "water"),
            Pokemon("Squirtle", 0.05, "water"),
            # Rare Pokemon
            Pokemon("Charizard", 0.01, "all"),
            Pokemon("Dragonite", 0.01, "all"),
            Pokemon("Mewtwo", 0.001, "all"),
        ]
        self.inventory: List[Pokemon] = []
        self.map = self.generate_map()

    def generate_map(self) -> List[List[str]]:
        map_grid = [["."] * self.width for _ in range(self.height)]

        # Generate terrain features
        for _ in range(self.width * self.height // 20):  # Trees
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            self._generate_feature(map_grid, x, y, "T", 0.7)

        for _ in range(self.width * self.height // 30):  # Water
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            self._generate_feature(map_grid, x, y, "~", 0.8)

        for _ in range(self.width * self.height // 25):  # Flowers
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if map_grid[y][x] == ".":
                map_grid[y][x] = "*"

        return map_grid

    def _generate_feature(
        self, map_grid: List[List[str]], x: int, y: int, feature: str, spread: float
    ) -> None:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                new_x, new_y = x + dx, y + dy
                if (
                    0 <= new_x < self.width
                    and 0 <= new_y < self.height
                    and random.random() < spread
                ):
                    map_grid[new_y][new_x] = feature

    def move_player(self, dx: int, dy: int) -> None:
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            self.player_x, self.player_y = new_x, new_y
            self.check_pokemon_encounter()

    def rotate_player(self, angle: int) -> None:
        self.player_direction = (self.player_direction + angle) % 360

    def check_pokemon_encounter(self) -> None:
        if random.random() < 0.2:
            terrain = self.map[self.player_y][self.player_x]
            terrain_map = {".": "grass", "T": "forest", "~": "water", "*": "grass"}
            current_terrain = terrain_map.get(terrain, "grass")

            possible_pokemon = [
                p
                for p in self.pokemon_list
                if p.habitat == current_terrain or p.habitat == "all"
            ]

            if possible_pokemon:
                pokemon = random.choice(possible_pokemon)
                if random.random() < pokemon.rarity:
                    print(
                        f"\n{COLORS['cyan']}A wild {pokemon.name} appeared!{COLORS['reset']}"
                    )
                    choice = input("Try to catch it? (y/n): ")
                    if choice.lower() == "y":
                        catch_rate = 0.5 + (
                            0.2 if current_terrain == pokemon.habitat else 0
                        )
                        if random.random() < catch_rate:
                            print(
                                f"{COLORS['green']}Caught {pokemon.name}!{COLORS['reset']}"
                            )
                            self.inventory.append(
                                Pokemon(pokemon.name, pokemon.rarity, pokemon.habitat)
                            )
                        else:
                            print(
                                f"{COLORS['red']}{pokemon.name} escaped!{COLORS['reset']}"
                            )
                    time.sleep(1)

    def display(self) -> None:
        os.system("clear")
        print("=== Pokémon World - 8-bit Edition ===")
        print("Controls: WASD=Move, E/Q=Rotate, X=Quit")

        # Draw map with player
        for y in range(self.height):
            for x in range(self.width):
                if x == self.player_x and y == self.player_y:
                    print(self.sprites["player"][self.player_direction], end="")
                else:
                    terrain = self.map[y][x]
                    print(self.sprites["terrain"][terrain], end="")
            print()

        # Status display
        print("\n" + "=" * 40)
        print(f"Position: ({self.player_x}, {self.player_y})")
        print(
            f"Direction: {['North', 'East', 'South', 'West'][self.player_direction//90]}"
        )
        print(f"Pokémon Caught: {len(self.inventory)}")
        if self.inventory:
            print("Collection: " + ", ".join(p.name for p in self.inventory))
        print("=" * 40)


def main():
    world = World()
    commands = {
        "w": (0, -1, 0),  # (dx, dy, rotation)
        "s": (0, 1, 0),
        "a": (-1, 0, 0),
        "d": (1, 0, 0),
        "e": (0, 0, 90),
        "q": (0, 0, -90),
    }

    while True:
        world.display()
        move = input("Enter command: ").lower()

        if move == "x":
            break
        elif move in commands:
            dx, dy, rot = commands[move]
            if rot:
                world.rotate_player(rot)
            else:
                world.move_player(dx, dy)


if __name__ == "__main__":
    main()
