import math
import os
import random
import time
from typing import List, Tuple

class Ray:
    def __init__(self, angle: float):
        self.angle = angle
        self.distance = 0
        self.wall_type = ''
        self.hit_point = (0, 0)

class Player:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.angle = 0
        self.FOV = math.pi / 3  # 60 degrees
        self.move_speed = 0.1
        self.turn_speed = 0.1

class Pokemon3D:
    def __init__(self, map_width: int = 20, map_height: int = 15, screen_width: int = 80, screen_height: int = 24):
        self.map_width = map_width
        self.map_height = map_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = Player(map_width/2, map_height/2)
        self.world_map = self.generate_map()
        self.textures = {
            'T': '█',  # Tree
            '~': '≈',  # Water
            '.': '·',  # Grass
            '*': '❀',  # Flower
            '#': '▒',  # Wall
        }
        self.depth = 16.0
        self.running = True

    def generate_map(self) -> List[List[str]]:
        # Initialize with grass
        game_map = [['.'] * self.map_width for _ in range(self.map_height)]
        
        # Add trees and water
        for _ in range(self.map_width * self.map_height // 10):
            x = random.randint(0, self.map_width-1)
            y = random.randint(0, self.map_height-1)
            feature = random.choice(['T', '~'])
            game_map[y][x] = feature
            
        # Add border walls
        for x in range(self.map_width):
            game_map[0][x] = '#'
            game_map[self.map_height-1][x] = '#'
        for y in range(self.map_height):
            game_map[y][0] = '#'
            game_map[y][self.map_width-1] = '#'
            
        return game_map

    def cast_ray(self, ray_angle: float) -> Ray:
        ray = Ray(ray_angle)
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)
        
        # Ray casting loop
        for depth in range(int(self.depth * 10)):
            depth_val = depth * 0.1
            x = self.player.x + depth_val * cos_a
            y = self.player.y + depth_val * sin_a
            
            map_x, map_y = int(x), int(y)
            
            if not (0 <= map_x < self.map_width and 0 <= map_y < self.map_height):
                ray.distance = depth_val
                ray.wall_type = '#'
                break
                
            if self.world_map[map_y][map_x] in ['T', '#', '~']:
                ray.distance = depth_val
                ray.wall_type = self.world_map[map_y][map_x]
                ray.hit_point = (x, y)
                break
        
        return ray

    def render_frame(self):
        frame = []
        for y in range(self.screen_height):
            row = []
            for x in range(self.screen_width):
                ray_angle = self.player.angle - self.player.FOV/2 + (x/self.screen_width) * self.player.FOV
                ray = self.cast_ray(ray_angle)
                
                # Calculate wall height
                wall_height = (self.screen_height / ray.distance) if ray.distance > 0 else self.screen_height
                ceiling = int((self.screen_height - wall_height) / 2)
                floor = self.screen_height - ceiling
                
                if y < ceiling:
                    char = ' '  # Sky
                elif y > floor:
                    char = ':'  # Ground
                else:
                    char = self.textures.get(ray.wall_type, '#')
                    # Add distance shading
                    if ray.distance > self.depth/2:
                        char = '▒' if char == '█' else '.'
                
                row.append(char)
            frame.append(''.join(row))
        return frame

    def handle_input(self):
        import sys, tty, termios

        def getch():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

        # Check if there's input available
        import select
        if select.select([sys.stdin], [], [], 0)[0]:
            key = getch().lower()
            dx = math.cos(self.player.angle) * self.player.move_speed
            dy = math.sin(self.player.angle) * self.player.move_speed
            
            if key == 'w':
                new_x = self.player.x + dx
                new_y = self.player.y + dy
                if self.world_map[int(new_y)][int(new_x)] == '.':
                    self.player.x, self.player.y = new_x, new_y
            elif key == 's':
                new_x = self.player.x - dx
                new_y = self.player.y - dy
                if self.world_map[int(new_y)][int(new_x)] == '.':
                    self.player.x, self.player.y = new_x, new_y
            elif key == 'a':
                self.player.angle -= self.player.turn_speed
            elif key == 'd':
                self.player.angle += self.player.turn_speed
            elif key == 'q':
                self.running = False
        
    def run(self):
        import sys
        import time  # Import the full module

        # ANSI escape codes for cursor control
        CURSOR_UP = '\x1b[A'
        HIDE_CURSOR = '\x1b[?25l'
        SHOW_CURSOR = '\x1b[?25h'
        CLEAR = '\x1b[2J\x1b[H'
        
        target_fps = 30
        frame_time = 1.0 / target_fps
        
        try:
            print(HIDE_CURSOR + CLEAR)  # Hide cursor and clear screen initially
            last_time = time.time()  # Use time.time() instead of time()
            
            while self.running:
                current_time = time.time()  # Use time.time()
                delta = current_time - last_time
                
                if delta >= frame_time:
                    print('\x1b[H')
                    frame = self.render_frame()
                    sys.stdout.write('\n'.join(frame))
                    sys.stdout.write(f"\n\nPosition: ({self.player.x:.1f}, {self.player.y:.1f}) Angle: {math.degrees(self.player.angle):.1f}°")
                    sys.stdout.write("\nUse WASD to move/turn, Q to quit")
                    sys.stdout.flush()
                    
                    self.handle_input()
                    last_time = current_time
                
                time.sleep(0.001)  # Use time.sleep()
                
        except KeyboardInterrupt:
            self.running = False
        finally:
            print(SHOW_CURSOR)

if __name__ == "__main__":
    game = Pokemon3D()
    game.run()