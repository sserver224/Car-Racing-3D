import time
import numpy as np
import pygame as pg
import numpy as np
from math import sin, cos, fabs, pow, sqrt, pi, ceil
from time import sleep
import os
import sys
from XInput import *
import socket
from elm import *
from winreg import *
from tkinter import messagebox
emulator=elm.Elm()
emulator.net_port=35000
emulator.scenario='car'
r=Thread(target=emulator.run)
r.daemon=True
r.start()
def get_resource_path(relative_path):
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def collide_with_walls(walls, current_x, current_y, future_x, future_y):
    for wall in walls:
        if fabs(current_x - wall.x3) < 3000:
            denominator = (current_x - future_x) * (wall.y3 - wall.y4) - \
                (current_y - future_y) * (wall.x3 - wall.x4)

            if denominator != 0:
                t = ((current_x - wall.x3) * (wall.y3 - wall.y4) -
                     (current_y - wall.y3) * (wall.x3 - wall.x4)) / denominator
                u = ((current_x - wall.x3) * (current_y - future_y) -
                     (current_y - wall.y3) * (current_x - future_x)) / denominator
                if 0 < t < 1 and 0 < u < 1:
                    return True
    return False
class Ray:
    def __init__(self, angle):
        self.angle = angle
        self.color = pg.Color("yellow")
        self.width = 1

    def cast(self, position, walls):
        self.x1 = position[0]
        self.y1 = position[1]
        self.x2 = self.x1 + cos(self.angle)
        self.y2 = self.y1 + sin(self.angle)

        min_distance = 10e8
        self.texture = 0

        for wall in walls:
            denominator = (self.x1 - self.x2) * (wall.y3 - wall.y4) - (self.y1 - self.y2) * (wall.x3 - wall.x4)
            if denominator == 0:
                t, u = 0, 0
            else:
                t = ((self.x1 - wall.x3) * (wall.y3 - wall.y4) - (self.y1 - wall.y3) * (wall.x3 - wall.x4)) / denominator
                u = ((self.x1 - wall.x3) * (self.y1 - self.y2) - (self.y1 - wall.y3) * (self.x1 - self.x2)) / denominator

            if t > 0 and 0 < u < 1: 
                x2 = self.x1 + t * (self.x2 - self.x1)
                y2 = self.y1 + t * (self.y2 - self.y1)
                distance = pow(x2 - self.x1, 2) + pow(y2 - self.y1, 2)

                if distance < min_distance:
                    self.texture = (u // 0.001) % 100
                    min_distance = distance
                    self.x2 = x2
                    self.y2 = y2

        return sqrt(min_distance)

    def render(self, screen):
        pg.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2), self.width)
class Progress:
    def __init__(self, car, track, screen_width, screen_height):
        self.car = car
        self.track = track

        self.width = screen_width / 30
        self.height = screen_height / 2

        self.image = pg.transform.smoothscale(pg.image.load(get_resource_path("sprites/checkerboard.png")), (self.width, self.height / 10)).convert()

        self.x = screen_width - 3 * self.width / 2
        self.y = (screen_height - self.height) / 2

        self.outer_rect = pg.Rect(self.x - 4, self.y - 4, self.width + 8, self.height + 8)
        self.outer_color = pg.Color(32, 32, 32)
        self.inner_color = pg.Color("#1f51ff")

    def render(self, screen):
        length = (self.car.x / self.track.final_x) * self.height
        inner_rect = pg.Rect(self.x, self.y + self.height - length, self.width, length)
        pg.draw.rect(screen, self.outer_color, self.outer_rect)
        pg.draw.rect(screen, self.inner_color, inner_rect)
        screen.blit(self.image, (self.x, self.y))
class Sound:
    def __init__(self):
        self.state = "starting"
        
        pg.mixer.init()
        
        self.idle_sound = pg.mixer.Sound(get_resource_path("sounds/idle.mp3"))
        self.brake_sound = pg.mixer.Sound(get_resource_path("sounds/brake.mp3"))
        self.top_sound = pg.mixer.Sound(get_resource_path("sounds/top_speed.mp3"))
        
        self.crash_sound = pg.mixer.Sound(get_resource_path("sounds/crash.mp3"))
        self.scratch_sound = pg.mixer.Sound(get_resource_path("sounds/scratch.wav"))
        self.finish_sound = pg.mixer.Sound(get_resource_path("sounds/finish.wav"))

    def stop_sound(self):
        try:
            if self.state == "idle":
                self.idle_sound.stop()
            elif self.state == "accelerate" or self.state == "decelerate":
                pg.mixer.music.stop()
            elif self.state == "top":
                self.top_sound.stop()
            elif self.state == "brake":
                self.brake_sound.stop()
            elif self.state == "crash":
                self.crash_sound.stop()
            pg.mixer.pause()
        except:
            pass

    def play_idle(self):
        state_changed = False

        if self.state == "starting":
            state_changed = True
        elif self.state == "accelerate" or self.state == "decelerate":
            pg.mixer.music.stop()
            state_changed = True
        elif self.state == "brake":
            self.brake_sound.stop()
            state_changed = True
        elif self.state == "crash":
            self.state_change = True

        if state_changed:
            self.state = "idle"
            self.idle_sound.play(100000)

    def play_accelerate(self, position):
        state_changed = False

        if self.state == "idle":
            self.idle_sound.stop()
            state_changed = True
        elif self.state == "decelerate":
            pg.mixer.music.stop()
            state_changed = True
        elif self.state == "brake":
            self.brake_sound.stop()
            state_changed = True
        elif self.state == "crash":
            state_changed = True

        if state_changed:
            self.state = "accelerate"
            pg.mixer.music.load(get_resource_path("sounds/accelerate.mp3"))
            pg.mixer.music.play(-1, position * 10)

    def stop_accelerate(self):
        if self.state == "accelerate":
            pg.mixer.music.stop()

    def play_decelerate(self, position):
        state_changed = False

        if self.state == "accelerate":
            pg.mixer.music.stop()
            state_changed = True
        elif self.state == "brake":
            self.brake_sound.stop()
            state_changed = True
        elif self.state == "top":
            self.top_sound.stop()
            state_changed = True

        if state_changed:
            self.state = "decelerate"
            pg.mixer.music.load(get_resource_path("sounds/decelerate.mp3"))
            pg.mixer.music.play(0, position * 10)

    def play_brake(self):
        state_changed = False

        if self.state == "accelerate" or self.state == "decelerate":
            pg.mixer.music.stop()
            state_changed = True
        if self.state == "top":
            self.top_sound.stop()
            state_changed = True

        if state_changed:
            self.state = "brake"
            self.brake_sound.play()

    def play_top(self):
        state_changed = False

        if self.state == "accelerate":
            pg.mixer.music.stop()
            state_changed = True

        if state_changed:
            self.state = "top"
            self.top_sound.play(100000)

    def play_crash(self):
        state_changed = False

        if self.state == "idle":
            self.idle_sound.stop()
            state_changed = True
        elif self.state == "brake":
            self.brake_sound.stop()
            state_changed = True
        elif self.state == "top":
            self.top_sound.stop()
            state_changed = True
        elif self.state == "accelerate" or self.state == "decelerate":
            pg.mixer.music.stop()
            state_changed = True

        if state_changed:
            self.state = "crash"
            self.crash_sound.play()

    def play_scratch(self):
        pass

    def play_finish(self):
        pg.mixer.music.stop()
        if self.state == "idle":
            self.idle_sound.stop()
        elif self.state == "brake":
            self.brake_sound.stop()
        elif self.state == "top":
            self.top_sound.stop()            

        self.finish_sound.play()
        sleep(1)
class Minimap:
    def __init__(self, car, track, screen_width, screen_height):
        self.car = car
        self.track = track

        self.radius = screen_width / 12
        self.x = 3 * self.radius / 2
        self.y = screen_height - 3 * self.radius / 2

        self.road_length = self.radius / 6
        self.car_rect = pg.Rect(self.x - 4, self.y - 4, 8, 8)

        self.background_color = pg.Color("black")
        self.road_color = pg.Color(128, 128, 128)
        self.player_color = pg.Color("red")

    def get_position(self):
        for i in range(0, len(self.track.walls), 2):
            if self.track.walls[i].x3 < self.car.x < self.track.walls[i].x4:
                return i
        return 0

    def render(self, screen):
        pg.draw.circle(screen, self.background_color, (self.x, self.y), self.radius)

        car_position = self.get_position()

        # obtain track around car
        track_angles = []
        for offset in range(-10, 12, 2):
            track_position = int((car_position + offset) / 2)
            if 0 < track_position < len(self.track.track_curvature):
                track_angles.append(self.track.track_curvature[track_position])
            else:
                track_angles.append(None)

        front_x, front_y = self.x, self.y - self.road_length / 2
        back_x, back_y = self.x, self.y + self.road_length / 2
        pg.draw.line(screen, self.road_color, (front_x, front_y), (back_x, back_y), 3)

        current_x, current_y = front_x, front_y
        next_x, next_y = 0, 0
        running_angle = 0

        # render track in front of car
        for i in range(6, 11):
            angle = track_angles[i]
            if angle is not None:
                next_x, next_y = current_x + self.road_length * sin(running_angle + angle), current_y - self.road_length * cos(running_angle + angle)
                pg.draw.line(screen, self.road_color, (current_x, current_y), (next_x, next_y), 3)
                current_x, current_y = next_x, next_y
                running_angle += angle
        
        current_x, current_y = back_x, back_y
        next_x, next_y = 0, 0
        running_angle = 0

        # render track behind car
        for i in range(4, -1, -1):
            angle = track_angles[i]
            if angle is not None:
                next_x, next_y = current_x + self.road_length * sin(running_angle + angle), current_y + self.road_length * cos(running_angle + angle)
                pg.draw.line(screen, self.road_color, (current_x, current_y), (next_x, next_y), 3)
                current_x, current_y = next_x, next_y
                running_angle += angle

        pg.draw.rect(screen, self.player_color, self.car_rect)
class Car:
    def __init__(self, x, y, look_angle, screen_width, screen_height):
        self.x = x
        self.y = y
        self.look_angle = np.deg2rad(look_angle)

        car_width = screen_width / 3
        car_height = screen_height / 4
        self.image = pg.transform.smoothscale(
            pg.image.load(get_resource_path("sprites/car.png")), (car_width, car_height)).convert_alpha()

        self.screen_x = screen_width / 2 - car_width / 2
        self.screen_y = 5 * screen_height / 6 - car_height / 2

        self.speed = 0
        self.rpm=0
        self.gear=0
        self.top_speed = 284
        self.reverse_speed = 5
        self.acceleration = 1

        self.deceleration = 0.33
        self.braking = 3

        self.turn_speed = np.deg2rad(1)
        self.telemetry={'speed':0, 'rpm':0, 'gear':0}
        self.front_distance = 300
        self.side_distance = 32

        self.collide_front = False
        self.collide_back = False
        self.collide_left = False
        self.collide_right = False

        self.wall_behind = False
        self.collide_x = 0
        self.collide_y = 0

        self.sound = Sound()

    def update(self, acc, steering, walls):
        if self.speed <= 0:
            self.sound.play_idle()
        if self.speed == self.top_speed:
            self.sound.play_top()
        if acc>0 and not self.collide_front:
            if self.gear==1 and self.speed<40:
                self.speed+=0.9*acc*self.acceleration
            if self.gear==2 and self.speed<105:
                self.speed+=acc*self.acceleration
            if self.gear==3 and self.speed<150:
                self.speed+=0.6*acc*self.acceleration
            if self.gear==4 and self.speed<185:
                self.speed+=0.4*acc*self.acceleration
            if self.gear==5 and self.speed<220:
                self.speed+=0.2*acc*self.acceleration
            if self.gear==6 and self.speed<250:
                self.speed+=0.08*acc*self.acceleration
            if self.gear==7 and self.speed<284:
                self.speed+=0.03*acc*self.acceleration
            if self.speed > self.top_speed:
                self.speed = self.top_speed
            if self.speed>self.top_speed*acc:
                self.sound.play_decelerate(1 - self.rpm/8000)
                if self.speed / self.top_speed > 0.66:
                    self.speed -= 3 * self.deceleration
                elif self.speed / self.top_speed > 0.33:
                    self.speed -= 2 * self.deceleration
                self.speed -= self.deceleration
            else:
                self.sound.play_accelerate(self.rpm/8000)
            self.telemetry={'speed':self.speed, 'rpm':self.rpm, 'gear':self.gear}
            self.x += self.speed * cos(self.look_angle)
            self.y += self.speed * sin(self.look_angle)
            self.sound.play_accelerate(self.rpm/8000)
        if acc<0:
            if self.speed == 0 and not self.collide_back:
                self.x -= self.reverse_speed * cos(self.look_angle)
                self.y -= self.reverse_speed * sin(self.look_angle)
            elif self.speed > 0 and not self.collide_front:
                self.sound.play_brake()
                self.speed -= self.braking*abs(acc)
                if self.speed < 0:
                    self.speed = 0
                self.x += self.speed * cos(self.look_angle)
                self.y += self.speed * sin(self.look_angle)
        if steering<0:
            if self.speed > 0 and not self.collide_front and not self.collide_left:
                self.look_angle -= self.turn_speed * (1.5 - self.speed / self.top_speed)*abs(steering)
            elif self.speed == 0 and acc<0 and not self.collide_back and not self.collide_right:
                self.look_angle += self.turn_speed*abs(steering)
        if steering>0:
            if self.speed > 0 and not self.collide_front and not self.collide_right:
                self.look_angle += self.turn_speed * (1.5 - self.speed / self.top_speed)*steering
            elif self.speed == 0 and acc<0 and not self.collide_back and not self.collide_left:
                self.look_angle -= self.turn_speed*steering
        if acc==0 and self.speed > 0 and not self.collide_front and not self.collide_left and not self.collide_right:
            self.sound.play_decelerate(1 - self.rpm/8000)
            if self.speed / self.top_speed > 0.66:
                self.speed -= 3 * self.deceleration
            elif self.speed / self.top_speed > 0.33:
                self.speed -= 2 * self.deceleration
            self.speed -= self.deceleration
            if self.speed < 0:
                self.speed = 0
            self.x += self.speed * cos(self.look_angle)
            self.y += self.speed * sin(self.look_angle)
        emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * '+str(self.rpm)+')</exec><writeln />'
        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + (self.front_distance + self.speed + self.acceleration) * cos(self.look_angle),
            self.y + (self.front_distance + self.speed + self.acceleration) * sin(self.look_angle)
        ):
            if not self.collide_front:
                w=Thread(target=crash_vibration)
                w.daemon=True
                w.start()
            self.collide_front = True
            self.sound.play_crash()
            self.collide_speed = self.speed
            self.speed = 0
            if self.speed==0:
                self.gear=1

            self.collide_x = self.x + self.front_distance * cos(self.look_angle)
            self.collide_y = self.y + self.front_distance * sin(self.look_angle)
        else:
            if self.x + self.front_distance * cos(self.look_angle) != self.collide_x or self.y + self.front_distance * sin(self.look_angle) != self.collide_y:
                self.collide_front = False

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + (self.front_distance - self.reverse_speed) *
            cos(self.look_angle),
            self.y + (self.front_distance - self.reverse_speed) *
            sin(self.look_angle)
        ):
            if not self.collide_back:
                w=Thread(target=crash_vibration)
                w.daemon=True
                w.start()
            self.collide_back = True
            self.sound.play_crash()
        else:
            self.collide_back = False

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + self.front_distance *
                cos(self.look_angle) + self.side_distance *
            cos(self.look_angle - np.pi / 2),
            self.y + self.front_distance *
                sin(self.look_angle) + self.side_distance *
            sin(self.look_angle - np.pi / 2)
        ):
            self.sound.play_scratch()
            if not self.collide_left:
                w=Thread(target=crash_vibration)
                w.daemon=True
                w.start()
            self.collide_left = True
        else:
            self.collide_left = False

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + self.front_distance *
                cos(self.look_angle) + self.side_distance *
            cos(self.look_angle + np.pi / 2),
            self.y + self.front_distance *
                sin(self.look_angle) + self.side_distance *
            sin(self.look_angle + np.pi / 2)
        ):
            self.sound.play_scratch()
            if not self.collide_right:
                w=Thread(target=crash_vibration)
                w.daemon=True
                w.start()
            self.collide_right = True
        else:
            self.collide_right = False

        if collide_with_walls(
            walls,
            self.x,
            self.y,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle)
        ):
            self.wall_behind = True
        else:
            self.wall_behind = False

        if self.x < 0:
            self.x = 0  

    def render(self, screen):
        screen.blit(self.image, (self.screen_x, self.screen_y))

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.look_angle = 0
class Speedometer:
    def __init__(self, car, screen_width, screen_height):
        self.car = car

        speedometer_width = screen_width / 4
        speedometer_height = screen_height / 4

        self.image = pg.transform.smoothscale(pg.image.load(
            get_resource_path("sprites/speedometer.png")), (speedometer_width, speedometer_height)).convert_alpha()

        self.screen_x = screen_width - (speedometer_width)
        self.screen_y = screen_height - (speedometer_height)
        self.needle_x = screen_width - (speedometer_width / 2)
        self.needle_y = screen_height - 20
        self.needle_length = speedometer_height / 1.7
        self.needle_color = pg.Color("#1f51ff")

    def render(self, screen):
        screen.blit(self.image, (self.screen_x, self.screen_y))
        angle = pi*self.car.rpm / 10000
        tip_x = self.needle_x - self.needle_length * cos(angle)
        tip_y = self.needle_y - self.needle_length * sin(angle)
        pg.draw.line(screen, self.needle_color, (self.needle_x, self.needle_y), (tip_x, tip_y), 3)
def blit_text(surface, text, pos, font, color):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0] 
    max_width, _ = surface.get_size()
    max_width = max_width / 2

    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0] 
        y += word_height
import random
import numpy as np
class Track:
    def __init__(self, max_distance, road_width):
        self.max_distance = max_distance
        self.road_width = road_width

        self.wall_segment_length = 2000
        self.front_load_distance = 8000
        self.back_load_distance = 4000

        self.track_curvature = []
        self.walls = []

        self.current_angle = 0
        self.current_distance = 0

        self.build_bluprint()
        self.build_track()

    def build_bluprint(self):
        self.track_curvature = []

        any_direction = [
            self.straight_track, self.straight_track,
            self.gradual_left_turn, self.gradual_left_turn,
            self.sharp_left_turn, self.sharp_right_turn,
            self.tight_left_turn, self.tight_right_turn
        ]
        left_direction = [
            self.gradual_left_turn, self.gradual_left_turn,
            self.sharp_left_turn, self.tight_left_turn
        ]
        right_direction = [
            self.gradual_right_turn, self.gradual_left_turn,
            self.sharp_right_turn, self.tight_right_turn
        ]

        while self.current_distance < self.max_distance:
            if fabs(self.current_angle) < np.pi / 4:
                next_section = random.choice(any_direction)
                next_section()
            elif self.current_angle <= -np.pi / 4:
                next_section = random.choice(right_direction)
                next_section()
            elif self.current_angle >= np.pi / 4:
                next_section = random.choice(left_direction)
                next_section()

    def straight_track(self):
        self.track_curvature += [0 for _ in range(random.randint(2, 4))]

    def gradual_left_turn(self):
        self.track_curvature += [-0.1, -0.1, -0.1, -0.1, -0.1]
        self.current_distance += 5 * self.wall_segment_length
        self.current_angle -= 0.5

    def gradual_right_turn(self):
        self.track_curvature += [0.1, 0.1, 0.1, 0.1, 0.1]
        self.current_distance += 5 * self.wall_segment_length
        self.current_angle += 0.5

    def sharp_left_turn(self):
        self.track_curvature += [-0.3, -0.3, -0.3]
        self.current_distance += 3 * self.wall_segment_length
        self.current_angle -= 0.9

    def sharp_right_turn(self):
        self.track_curvature += [0.3, 0.3, 0.3]
        self.current_distance += 3 * self.wall_segment_length
        self.current_angle += 0.9

    def tight_left_turn(self):
        self.track_curvature += [-0.2, -0.2, -0.2, -0.2]
        self.current_distance += 4 * self.wall_segment_length
        self.current_angle -= 0.8

    def tight_right_turn(self):
        self.track_curvature += [0.2, 0.2, 0.2, 0.2]
        self.current_distance += 4 * self.wall_segment_length
        self.current_angle += 0.8

    def smooth_hairpin(self):
        if random() > 0.5:
            self.gradual_left_turn()
            self.gradual_right_turn()
        else:
            self.gradual_right_turn()
            self.gradual_left_turn()

    def build_track(self):
        self.walls.append(Wall(0, 0, 0, self.road_width))
        self.walls.append(Wall(0, 0, self.wall_segment_length, 0))
        self.walls.append(
            Wall(0, self.road_width, self.wall_segment_length, self.road_width))

        self.current_angle = 0
        for angle in self.track_curvature:
            self.current_angle += angle
            x3 = self.walls[-2].x4
            y3 = self.walls[-2].y4
            x4 = x3 + self.wall_segment_length * cos(self.current_angle)
            y4 = y3 + self.wall_segment_length * sin(self.current_angle)
            self.walls.append(Wall(x3, y3, x4, y4))

            horizontal_width = self.road_width * \
                sin(self.current_angle + np.pi / 2)
            vertical_width = self.road_width * \
                cos(self.current_angle + np.pi / 2)
            self.walls.append(Wall(
                self.walls[-2].x4, self.walls[-2].y4, x4 + vertical_width, y4 + horizontal_width))

        self.final_x = self.walls[-1].x4

    def load_walls(self, car_position):
        visible_walls = []

        for wall in self.walls:
            if -self.back_load_distance < wall.x3 - car_position < self.front_load_distance:
                visible_walls.append(wall)
        return visible_walls
def start_menu():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    screen_width, screen_height = pg.display.get_surface().get_size()
    pg.display.set_caption("Car Racing 3D v0.5 (c) sserver")
    clock = pg.time.Clock()
    title_font = pg.font.SysFont(None, 48)
    text_font = pg.font.SysFont(None, 36)

    bg_color = pg.Color(48, 48, 48)
    font_color = pg.Color("white")
    emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * 0)</exec><writeln />'
    title_text = title_font.render("Car Racing 3D v0.5 (c) sserver", True, font_color)
    title_rect = title_text.get_rect(center=(screen_width / 2, 18))

    left_text =  "CONTROLS:\n\
Use RT/LT/LS or arrows to drive the car\n\
Press R or START to restart\n\
RevHeadz OBD IP: Run ipconfig to view\n\
For controller users, press SELECT to select option then START to choose. Selection will be shown on the title bar.\n\
IMPORTANT: If unresponsive, click on the game window. Collision detection is a bit buggy. Keyboard controls are ignored if a controller is connected.\n\
ABOUT:\n\
Developed by sserver224\nmywebsite1324.neocities.org"
    
    button_1 = pg.image.load(get_resource_path("buttons/button_1.png"))
    button_2 = pg.image.load(get_resource_path("buttons/button_2.png"))
    button_3 = pg.image.load(get_resource_path("buttons/button_3.png"))
    button_4 = pg.image.load(get_resource_path("buttons/button_4.png"))
    selection=1
    running = True
    pg.display.set_icon(pg.image.load(get_resource_path("sprites/logo.bmp")))
    pg.display.set_caption("Car Racing 3D v0.5 (c) sserver - Currently selected: 3 mi")
    while running:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()

                if 500 < mouse_x < 700:
                    if 100 < mouse_y < 200:
                        return 5
                    elif 225 < mouse_y < 325:
                        return 10
                    elif 350 < mouse_y < 450:
                        return 15
                    elif 475 < mouse_y < 575:
                        return 20
            
        screen.fill(bg_color)

        screen.blit(title_text, title_rect)
        blit_text(screen, left_text, (1, 100), text_font, font_color)
        screen.blit(button_1, (500, 100))
        screen.blit(button_2, (500, 225))
        screen.blit(button_3, (500, 350))
        screen.blit(button_4, (500, 475))
        if get_connected()[0]:
            if get_button_values(get_state(0))['BACK']:
                selection+=1
                if selection>4:
                    selection=1
                pg.display.set_caption("Car Racing 3D v0.5 (c) sserver - Currently selected: "+str(selection*3)+" mi")
                while get_button_values(get_state(0))['BACK']:
                    pass
            if get_button_values(get_state(0))['START']:
                return selection*5
        pg.display.flip()
    set_vibration(0, 0, 0)
    pg.quit()
    return None
class Wall:
    def __init__(self, x3, y3, x4, y4):
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4

        self.color = pg.Color("blue")
        self.width = 5

    def render(self, screen):
        pg.draw.line(screen, self.color, (self.x3, self.y3), (self.x4, self.y4), self.width)
def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def generate_rays(look_angle, fov, screen_width, res):
    return [Ray(angle) for angle in np.arange(look_angle - fov / 2, look_angle + fov / 2, fov * res / screen_width)]

def play_game(track_distance):
    global port, address
    def gear_up():
        car.gear+=1
        if car.gear==2:
            while car.rpm>car.speed*58+750:
                car.rpm-=231
        if car.gear==3:
            while car.rpm>car.speed*40.3+750:
                car.rpm-=231
        if car.gear==4:
            while car.rpm>car.speed*32.6+750:
                car.rpm-=231
        if car.gear==5:
            while car.rpm>car.speed*27.4+750:
                car.rpm-=231
        if car.gear==6:
            while car.rpm>car.speed*24.2+750:
                car.rpm-=231
        if car.gear==7:
            while car.rpm>car.speed*21.3+750:
                car.rpm-=231
    def gear_down():
        car.gear-=1
        if car.gear==2:
            while car.rpm<car.speed*58+750:
                    car.rpm+=231
        if car.gear==3:
            while car.rpm<car.speed*40.3+750:
                    car.rpm+=231
        if car.gear==4:
            while car.rpm<car.speed*32.6+750:
                    car.rpm+=231
        if car.gear==5:
            while car.rpm<car.speed*27.4+750:
                    car.rpm+=231
        if car.gear==6:
            while car.rpm<car.speed*21.3+750:
                    car.rpm+=231
        if car.gear==1:
            while car.rpm<car.speed*95+750:
                    car.rpm+=231
    # initialize pygame
    pg.init()
    screen = pg.display.set_mode((1280, 720), pg.SCALED)
    screen_width, screen_height = pg.display.get_surface().get_size()
    pg.display.set_caption("Car Racing 3D v0.5 (c) sserver")
    clock = pg.time.Clock()
    font = pg.font.SysFont(None, 36)

    # critical settings
    fov = np.deg2rad(60)
    height_scale = 100000
    shader_exponent = 2
    res = 1
    fps = 48
    road_width = 400

    # static elements
    bg_color = pg.Color(21, 1, 3)
    font_color = pg.Color("white")
    road_color = pg.Color(48, 48, 48)
    road_rect = pg.Rect(0, screen_height / 2, screen_width, screen_height / 2)
    title_text = font.render("Car Racing 3D v0.5 (c) sserver", True, font_color)
    title_rect = title_text.get_rect(center=(screen_width / 2, 18))

    # load objects
    car = Car(0, road_width / 2, 0, screen_width, screen_height)
    speedometer = Speedometer(car, screen_width, screen_height)
    track = Track(track_distance * 20000, road_width)
    rays = generate_rays(car.look_angle, fov, screen_width, res)
    walls = track.load_walls(car.x)
    progress_bar = Progress(car, track, screen_width, screen_height)
    minimap = Minimap(car, track, screen_width, screen_height)
    skyline = pg.transform.smoothscale(pg.image.load(get_resource_path("sprites/skyline.jpg")), (screen_width, screen_height / 2)).convert()
    skyline_turn_sensitivity = 200

    # dynamic loader of walls
    load_walls = pg.USEREVENT + 1
    pg.time.set_timer(load_walls, 1000)

    # timers and controls
    race_timer = None
    timer_started = False
    acc=0
    steering=0
    running = True
    # main loop
    while running:
        clock.tick(fps)
        screen.fill(bg_color)
        skyline_x = -skyline_turn_sensitivity * car.look_angle
        screen.blit(skyline, (skyline_x, 0))
        if skyline_x > 0:
            screen.blit(skyline, (skyline_x - screen_width, 0))
        elif skyline_x < 0:
            screen.blit(skyline, (skyline_x + screen_width, 0))
        pg.draw.rect(screen, road_color, road_rect)
        if get_connected()[0]:
            gas=get_trigger_values(get_state(0))[1]
            brake=get_trigger_values(get_state(0))[0]
            if gas>0 and brake==0:
                acc=gas
            elif brake>0:
                acc=-1*brake
            else:
                acc=0
            if acc>0:
                set_vibration(0, max(0, acc*(max(0, (50*acc)-car.speed)/(50*acc))), max(0, acc*(max(0, (50*acc)-car.speed)/(50*acc))))
            elif acc<0:
                if car.speed>20:
                    set_vibration(0, 1.0, 1.0)
                else:
                    set_vibration(0, max(0, -1*acc*(max(0, car.speed)/20)/2), max(0, -1*acc*(max(0, car.speed)/20)))
            else:
                set_vibration(0, 0, 0)
            if get_button_values(get_state(0))['START']:
                car.reset(0, road_width / 2)
                timer_started = False
                walls = track.load_walls(car.x)
                rays = generate_rays(car.look_angle, fov, screen_width, res)
            steering=get_thumb_values(get_state(0))[0][0]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_program()
            if event.type == pg.KEYDOWN and not get_connected()[0]:
                if event.key == pg.K_ESCAPE:
                    car.sound.stop_sound()
                    running = False
                if event.key == pg.K_UP:
                    acc=1
                if event.key == pg.K_DOWN:
                    acc=-1
                if event.key == pg.K_LEFT:
                    steering=-1
                if event.key == pg.K_RIGHT:
                    steering=1
                if event.key == pg.K_r:
                    # restart track
                    car.reset(0, road_width / 2)
                    timer_started = False
                    walls = track.load_walls(car.x)
                    rays = generate_rays(car.look_angle, fov, screen_width, res)
            if event.type == pg.KEYUP and not get_connected()[0]:
                if event.key == pg.K_UP:
                    acc=0
                if event.key == pg.K_DOWN:
                    acc=0
                if event.key == pg.K_LEFT:
                    steering=0
                if event.key == pg.K_RIGHT:
                    steering=0
            if event.type == load_walls:
                walls = track.load_walls(car.x)

                if clock.get_fps() < 24:
                    # automatically lower graphics if fps is low
                    res += 1
                    rays = generate_rays(car.look_angle, fov, screen_width, res)
        car.update(acc, steering, walls)
        if car.gear==0:
            if acc>0:
                car.rpm+=415*acc
            if car.rpm>750:
                car.rpm-=97
        if car.gear==1:
            car.rpm=car.speed*95+750
        if car.gear==2:
            car.rpm=car.speed*58+750
        if car.gear==3:
            car.rpm=car.speed*40.3+750
        if car.gear==4:
            car.rpm=car.speed*32.6+750
        if car.gear==5:
            car.rpm=car.speed*27.4+750
        if car.gear==6:
            car.rpm=car.speed*24.2+750
        if car.gear==7:
            car.rpm=car.speed*21.3+750
        if acc<0 and car.rpm>750:
            car.rpm-=100
        if car.rpm<750:
            car.rpm=750
        if car.rpm>8000:
            car.rpm=8000
        if acc<=0:
            if car.rpm>3800:
                if car.rpm<4000 and car.gear>0:
                    gear_down()
            if car.rpm<1200 and car.gear>0:
                gear_down()
        if (acc>0 and (((car.rpm>4000*acc and car.gear==1) or car.rpm>6700*acc) and car.rpm>2000) and car.gear<7) or (acc>0 and car.gear==0):
            gear_up()
        if acc>0:
            if not timer_started:
                race_timer = time.time()
                timer_started = True
        # check if race finished
        if car.x > track.final_x:
            emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * 0)</exec><writeln />'
            emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int(4 * 0)</exec><writeln />'
            car.speed=0
            car.rpm=0
            car.gear=0
            set_vibration(0, 0, 0)
            car.sound.play_finish()
            set_vibration(0, 0, 0)
            pg.quit()
            running = False
            set_vibration(0, 0, 0)
            return (time.time() - race_timer)
        
        # ray casting
        if (steering!=0) and (car.speed > 0 or acc<0):
            rays = generate_rays(car.look_angle, fov, screen_width, res)

        distances = np.zeros(len(rays), float)
        for i, ray in enumerate(rays):
            distances[i] = ray.cast((car.x, car.y), walls)

        # rendering walls
        for x, distance in enumerate(distances):
            height = height_scale / distance
            if height > screen_height:
                height = screen_height
            texture = translate(rays[x].texture * 2, 0, 200, 32, 64)
            raw_color = translate(height ** shader_exponent, 0, screen_height ** shader_exponent, 100, 200)
            pg.draw.line(screen, [raw_color, texture, 0], (x * res, (screen_height - height) / 2), (x * res, (screen_height + height) / 2), res)
        
        # rendering car
        if not car.wall_behind:
            car.render(screen)

        # rendering UI elements 
        speedometer.render(screen)
        progress_bar.render(screen)
        minimap.render(screen)

        # rendering text
        fps_display = font.render("FPS: " + str(int(clock.get_fps())), True, font_color)
        gear_display=font.render("Gear: "+str(car.gear), True, font_color)
        speed_display=font.render("MPH: "+str(round(car.speed*0.621371)), True, font_color)
        screen.blit(fps_display, (0, 0))
        screen.blit(speed_display, (1040, 500))
        screen.blit(gear_display, (1040, 470))
        screen.blit(title_text, title_rect)

        if timer_started:
            time_display = font.render(str(round(time.time() - race_timer, 2)), True, font_color)
            screen.blit(time_display, (screen_width - 100, 0))
        
        pg.display.flip()
def crash_vibration():
        set_vibration(0, 1.0, 1.0)
        time.sleep(0.2)
        set_vibration(0, 0, 0)
def exit_program():
    pg.quit()
    set_vibration(0, 0, 0)
    os._exit(0)
if __name__ == "__main__":
    emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * 0)</exec><writeln />'
    emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int(4 * 0)</exec><writeln />'
    CreateKeyEx(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver\Car Racing 3D', reserved=0)
    if get_connected()[0]:
        set_vibration(0, 0, 0)
    try:
        port=QueryValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Car Racing 3D', reserved=0, access=KEY_ALL_ACCESS), 'Port')[0]
        address=QueryValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Car Racing 3D', reserved=0, access=KEY_ALL_ACCESS), 'UDPAddr')[0]
    except OSError:
        port=9999
        address='0.0.0.0'
        SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Car Racing 3D', reserved=0, access=KEY_ALL_ACCESS), 'Port', 0, REG_DWORD, 9999)
        SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Car Racing 3D', reserved=0, access=KEY_ALL_ACCESS), 'UDPAddr', 0, REG_SZ, '0.0.0.0')
    hostname=socket.gethostname()
    IP=socket.gethostbyname(hostname)
    try:
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
    except:
        pass
    while True:
        length = start_menu()
        if length == 0 or length is None:
            break
        play_game(length)
