# raycaster.py
import math
from typing import List, Tuple


class RayCaster:
    def __init__(self, screen_width: int = 80, screen_height: int = 24):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.FOV = math.pi / 3  # 60 degrees FOV
        self.depth = 16
        self.wall_chars = {
            "T": "█",  # Tree
            "~": "≈",  # Water
            ".": "·",  # Grass
            "*": "❀",  # Flower
        }

    def calculate_ray(
        self,
        map_data: List[List[str]],
        player_pos: Tuple[int, int],
        player_angle: float,
        ray_angle: float,
    ) -> Tuple[float, str]:
        x, y = player_pos
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # Ray casting
        distance = 0
        while distance < self.depth:
            distance += 0.1
            ray_x = x + distance * cos_a
            ray_y = y + distance * sin_a

            map_x, map_y = int(ray_x), int(ray_y)

            if not (0 <= map_x < len(map_data[0]) and 0 <= map_y < len(map_data)):
                return distance, "#"

            if map_data[map_y][map_x] != ".":
                return distance, map_data[map_y][map_x]

        return self.depth, "."

    def render_frame(
        self,
        map_data: List[List[str]],
        player_pos: Tuple[int, int],
        player_angle: float,
    ) -> List[str]:
        frame = []

        for y in range(self.screen_height):
            row = []
            for x in range(self.screen_width):
                # Calculate ray angle for this column
                ray_angle = (
                    player_angle - self.FOV / 2 + (x / self.screen_width) * self.FOV
                )

                distance, wall_type = self.calculate_ray(
                    map_data, player_pos, player_angle, ray_angle
                )

                # Calculate wall height based on distance
                wall_height = (
                    (self.screen_height / distance)
                    if distance > 0
                    else self.screen_height
                )
                ceiling = int((self.screen_height - wall_height) / 2)
                floor = self.screen_height - ceiling

                if y < ceiling:
                    char = "."  # Sky
                elif y > floor:
                    char = ":"  # Ground
                else:
                    char = self.wall_chars.get(wall_type, "#")
                    # Add shading based on distance
                    if distance > self.depth / 2:
                        char = "▒" if char == "█" else "."

                row.append(char)
            frame.append("".join(row))

        return frame
