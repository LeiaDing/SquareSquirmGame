import tkinter as tk
import random
import sqlite3
import pygame
from tkinter import messagebox
from tkinter import simpledialog
#from PIL import Image, ImageTk

# 初始化pygame用于声音
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("background.wav")  # 替换为您的音乐文件路径
pygame.mixer.music.play(-1)  # -1 表示无限循环播放

        # 设置音乐音量(可选)
pygame.mixer.music.set_volume(0.3)

# 加载声音
#try:
collision_sound = pygame.mixer.Sound("collision.wav")
score_sound = pygame.mixer.Sound("score.wav")
#except:
    #print("无法加载声音文件,游戏将在无声模式下运行")

# 创建数据库连接
conn = sqlite3.connect('game_scores.db')
c = conn.cursor()

# 创建分数表(如果不存在)
c.execute('''CREATE TABLE IF NOT EXISTS scores
             (name TEXT, score INTEGER)''')


class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Square Squirm")
        self.canvas = tk.Canvas(self, width=400, height=600, bg="white")

        self.canvas.pack(fill="both", expand=True)

        # 创建背景
        self.create_background()

        #rabbit_image = Image.open("img.png")  # 确保你有这个图片文件
        #rabbit_image = rabbit_image.resize((50, 50))  # 调整大小
        #self.rabbit_photo = ImageTk.PhotoImage(rabbit_image)

        # 创建兔子玩家
        #self.player = self.canvas.create_image(400, 550, image=self.rabbit_photo)
        self.player = self.canvas.create_rectangle(180, 580, 220, 600, fill="blue")
        self.obstacles = []
        self.score = 0
        self.score_display = self.canvas.create_text(80, 30, text=f"分数: {self.score}", font=("Arial", 16))

        self.bind("<Left>", self.move_left)
        self.bind("<Right>", self.move_right)

        self.game_loop()

    def create_background(self):
        # 绘制蓝天
        self.canvas.create_rectangle(0, 0, 800, 500, fill="#87CEEB", outline="")

        # 添加白云
        self.add_cloud(100, 50)
        self.add_cloud(300, 100)
        self.add_cloud(500, 70)
        self.add_cloud(700, 120)

        # 绘制草地
        self.canvas.create_rectangle(0, 500, 800, 600, fill="#7CFC00", outline="")

    def add_cloud(self, x, y):
        # 绘制一朵简单的云
        self.canvas.create_oval(x, y, x + 60, y + 30, fill="white", outline="")
        self.canvas.create_oval(x + 20, y - 10, x + 100, y + 30, fill="white", outline="")
        self.canvas.create_oval(x + 40, y + 10, x + 120, y + 40, fill="white", outline="")

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
            obstacle = self.canvas.create_rectangle(x, 0, x + 20, 20, fill="red")
            self.obstacles.append(obstacle)

    def move_obstacles(self):
        for obstacle in self.obstacles:
            self.canvas.move(obstacle, 0, 5)
            if self.canvas.coords(obstacle)[3] > 600:
                self.canvas.delete(obstacle)
                self.obstacles.remove(obstacle)
                self.score += 1
                try:
                    score_sound.play()

                except:
                    pass

    def check_collision(self):
        player_coords = self.canvas.coords(self.player)
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            if self.intersect(player_coords, obstacle_coords):
                try:
                    collision_sound.play()
                except:
                    pass
                self.game_over()

    def intersect(self, rect1, rect2):
        return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or rect1[3] < rect2[1] or rect1[1] > rect2[3])

    def update_score(self):
        self.canvas.itemconfig(self.score_display, text=f"Your Score: {self.score}")

    def game_over(self):
        pygame.mixer.music.stop()
        name = tk.simpledialog.askstring("Game over!", f"Your score is {self.score}. Please enter your name:")
        if name:
            c.execute("INSERT INTO scores VALUES (?, ?)", (name, self.score))
            conn.commit()

        self.show_leaderboard()
        self.destroy()

    def show_leaderboard(self):
        c.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 5")
        leaderboard = c.fetchall()

        leaderboard_text = "Leaderboard:\n"
        for i, (name, score) in enumerate(leaderboard, 1):
            leaderboard_text += f"{i}. {name}: {score}\n"

        messagebox.showinfo("Learderboard", leaderboard_text)


if __name__ == "__main__":
    game = Game()
    game.mainloop()

conn.close()
