import tkinter as tk
from random import randint, choice

WIDTH = 600
HEIGHT = 400
SCORE = 0
DELAY_TIME = 30


class Ball:
    def __init__(self, canvas):
        self.radius = randint(10, 90)
        self.x1 = randint(self.radius, WIDTH - self.radius) - self.radius
        self.y1 = randint(self.radius, HEIGHT - self.radius) - self.radius
        self.x2 = self.x1 + self.radius
        self.y2 = self.y1 + self.radius
        self.move_x1 = self.move_x2 = 1
        self.move_y1 = self.move_y2 = 1
        self.color = choice(
            ['#000000', '#FF00FF', '#FF0000', '#800000', '#FFFF00', '#808000', '#00FF00', '#00FFFF', '#000080',
             '#CD5C5C', '#DC143C', '#F0E68C', '#4B0082', '#A52A2A', '#D2691E', '#00FF00', '#808000', '#293133'
             ])
        self.canvas = canvas
        self.ball_id = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=self.color)
        self.canvas.targets[self.ball_id] = self

    def step(self):
        self.x1 += self.move_x1
        self.y1 += self.move_y1
        self.x2 += self.move_x2
        self.y2 += self.move_y2
        if self.x1 <= 0 or self.x2 >= WIDTH:
            self.move_x1 = -self.move_x1
            self.move_x2 = -self.move_x2
        if self.y1 <= 0 or self.y2 >= HEIGHT:
            self.move_y1 = -self.move_y1
            self.move_y2 = -self.move_y2
        self.canvas.after(DELAY_TIME, self.step)

    def move(self):
        self.canvas.move(self.ball_id, self.move_x1, self.move_y1)
        self.canvas.after(DELAY_TIME, self.move)

    def position(self):
        return self.x1, self.y1, self.x2, self.y2

    def destroy(self):
        self.canvas.delete(self.ball_id)
        try:
            del self.canvas.targets[self.ball_id]
        except KeyError:
            pass


class Game(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, background='grey')

        self.targets = {}

        self.balls = [Ball(self)]
        self.count_start = len(self.balls)
        self.count_next = self.count_start
        self.score = 0
        self.score_text = self.create_text(WIDTH - 50,
                                           HEIGHT // 20,
                                           text='Score: {}'.format(self.score),
                                           font=('Times New Roman', 16)
                                           )

        self.bind('<Button-1>', self.click_handler)

    def click_handler(self, event):
        for ball in self.balls:
            if ball.position()[0] < event.x < ball.position()[2] and ball.position()[1] < event.y < \
                    ball.position()[3]:
                ball.destroy()
                self.score += 1
        self.update_score()

    def play(self, ms=120000):
        for ball in self.balls:
            ball.step()
            ball.move()
        self.after(ms, self.play)

    def run(self):
        self.play()
        self.stage()

    def stage(self):
        if len(self.targets) == 0:
            self.end_stage = tk.Button(self.master, text='Stage completed!\nPress for next stage.',
                                       command=self.next_stage)
            self.create_window(WIDTH / 2, HEIGHT / 2, window=self.end_stage)
            self.count_next += randint(1, 3)
        else:
            self.after(100, self.stage)

    def next_stage(self):
        self.end_stage.destroy()
        self.balls = [Ball(self) for _ in range(self.count_start, self.count_next + 1)]
        self.run()

    def update_score(self):
        self.itemconfig(self.score_text, text='Score: {}'.format(self.score))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(str(WIDTH) + 'x' + str(HEIGHT))
        self.resizable(False, False)
        self.title('ClickBalls')

        self.main = Game(self.master)
        self.main.pack(fill=tk.BOTH, expand=1)
        self.main.run()


if __name__ == '__main__':
    app = App()
    app.mainloop()
