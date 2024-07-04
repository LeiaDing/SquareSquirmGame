import tkinter as tk
import random
import sqlite3
import pygame
from tkinter import messagebox
conn = sqlite3.connect('game_scores.db')
c = conn.cursor()

# 创建分数
c.execute('''CREATE TABLE IF NOT EXISTS scores
             (name TEXT, score INTEGER)''')

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Square Squirm")
        self.canvas = tk.Canvas(self, width=400, height=600, bg="white")
        self.canvas.pack()

        self.player = self.canvas.create_rectangle(180, 580, 220, 600, fill="blue")
        self.obstacles = []
        self.score = 0
        self.score_display = self.canvas.create_text(50, 30, text=f"分数: {self.score}", font=("Arial", 16))

        self.bind("<Left>", self.move_left)
        self.bind("<Right>", self.move_right)

        self.game_loop()

    def move_left(self, event):
        self.canvas.move(self.player, -20, 0)

    def move_right(self, event):
        self.canvas.move(self.player, 20, 0)

    def game_loop(self):
        self.move_obstacles()
        self.create_obstacle()
        self.check_collision()
        self.update_score()
        self.after(50, self.game_loop)

    def create_obstacle(self):
        if random.randint(1, 10) == 1:
            x = random.randint(0, 380)
            obstacle = self.canvas.create_rectangle(x, 0, x+20, 20, fill="red")
            self.obstacles.append(obstacle)

    def move_obstacles(self):
        for obstacle in self.obstacles:
            self.canvas.move(obstacle, 0, 5)
            if self.canvas.coords(obstacle)[3] > 600:
                self.canvas.delete(obstacle)
                self.obstacles.remove(obstacle)
                self.score += 1
