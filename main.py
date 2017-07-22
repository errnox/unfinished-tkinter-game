import datetime
import sys
import time
import Tkinter as tk


class Player(object):
  def __init__(self, x=0, y=0, w=15, h=15, vx=0, vy=0, s=5,
               x2=0, y2=0, health=6, color='#34AE45', canvas=None):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.vx = vx
    self.vy = vy
    self.s = s
    self.x2 = self.x
    self.y2 = self.y
    self.color = color
    self.canvas = canvas
    self.health = health
    self.is_on_path = True

    self.circle_timer = 0

  def update(self, t):

    self.x += self.vx
    self.y += self.vy

    # Constrain the player to the visible screen.
    if self.x > self.canvas.winfo_width():
      self.x = 0
    if self.x < 0:
      self.x = self.canvas.winfo_height()
    if self.y > self.canvas.winfo_height():
      self.y = 0
    if self.y < 0:
      self.y = self.canvas.winfo_height()

    if self.vx > 0:
      self.vx -= 1 * self.s / 3
    elif self.vx < 0:
      self.vx += 1 * self.s / 3

    if self.vy > 0:
      self.vy -= 1 * self.s / 3
    elif self.vy < 0:
      self.vy += 1 * self.s / 3

    if self.circle_timer > 0:
      self.circle_timer -= 1

  def render(self, t):
    if self.is_on_path == True and self.circle_timer != 0:
      self.canvas.create_oval(
        self.x2 - 60 * self.circle_timer / 10,
        self.y2 - 60 * self.circle_timer / 10,
        self.x2 + 60 * self.circle_timer / 10,
        self.y2 + 60 * self.circle_timer / 10,
        fill='#4A4A4A', width=0)
      self.canvas.create_oval(
        self.x2 - 50 * self.circle_timer / 10,
        self.y2 - 50 * self.circle_timer / 10,
        self.x2 + 50 * self.circle_timer / 10,
        self.y2 + 50 * self.circle_timer / 10,
        fill='#121212', width=0)

    if (round((self.x + self.w / 2)) != round(self.x2)
        and round(self.y + self.h / 2) != round(self.y2)
        and self.is_on_path == True):
      self.canvas.create_line(
        self.x + self.w / 2, self.y + self.h / 2,
        self.x2, self.y2, fill=self.color, width=4)
      self.canvas.create_line(
        self.x + self.w / 2, self.y + self.h / 2,
        self.x2, self.y2, fill='#000000', width=1.5)
      self.x += (self.x2 - self.x - self.w / 2) * self.s * t
      self.y += (self.y2 - self.y - self.h / 2) * self.s * t
      self.canvas.create_oval(
        self.x2 - 4, self.y2 - 4,
        self.x2 + 4, self.y2 + 4,
        fill=self.color, width=0)
      self.canvas.create_oval(
        self.x2 - 3, self.y2 - 3,
        self.x2 + 3, self.y2 + 3,
        fill='#000000', width=0)
    else:
      self.is_on_path = False

    self.canvas.create_rectangle(
      self.x, self.y, self.x + self.w, self.y + self.h,
      fill=self.color, width=0)

    cw = 5
    gap = 2
    lx = self.health * (cw + gap) / 2 - self.w / 2
    for i in range(self.health):
      self.canvas.create_rectangle(
        (self.x + (i * (cw + gap))) - lx,
        self.y - self.h / 2,
        (self.x + (i * (cw + gap)) + cw) - lx,
        self.y - self.h / 2 + cw,
        fill='#EE3434', width=0)

  def move_left(self):
    self.vx -= 1 * self.s

  def move_right(self):
    self.vx += 1 * self.s

  def move_up(self):
    self.vy -= 1 * self.s

  def move_down(self):
    self.vy += 1 * self.s

  def move_to(self, x, y):
    self.x2 = x
    self.y2 = y
    self.is_on_path = True
    self.circle_timer = 10

  def hurt(self, n=1):
    if self.health > 0:
      self.health -= n

  def heal(self, n=1):
    if self.health <= 6:
      self.health += n


class App(object):
  def __init__(self):
    self.canvas_w = 500
    self.canvas_h = 400

    self.t_now = time.time()
    self.t_prev = time.time()
    self.t_elapsed = time.time()
    self.t_timer = time.time()
    self.t_elapsed = 0
    self.t_lag = 0
    self.t_ms = 0.00016
    self.t_frames = 0
    self.t_fps = 0
    self.t_last = time.time()
    
    self.master = tk.Tk()
    self.generate_widgets()
    self.master.mainloop()

  def generate_widgets(self):
    self.window = tk.Frame(self.master)
    self.window.pack()

    self.master.minsize(self.canvas_w, self.canvas_h)
    self.master.maxsize(self.canvas_w, self.canvas_h)

    self.canvas = tk.Canvas(
      self.window, width=self.canvas_w, height=self.canvas_h,
      bg='#121212')
    self.canvas.pack()

    self.player = Player(
      x=self.canvas_w / 2, y=self.canvas_h / 2, canvas=self.canvas)

    self.master.bind('<Key>', self.handle_keys)
    self.master.bind('<Button-1>', self.handle_mouse)

    self.canvas.after(1000 / 60, self.run())

  def run(self):
    self.t_now = time.time()
    self.t_elapsed = self.t_now - self.t_prev
    self.t_prev = self.t_now

    self.update(self.t_elapsed)
    self.render(self.t_elapsed)

    self.t_frames += 1
    if time.time() - self.t_last > 1:
      self.t_fps = self.t_frames
      self.t_last = time.time()
      self.t_frames = 0

    self.canvas.after(1000 / 60, self.run)

  def update(self, t):
    self.canvas.delete(tk.ALL)
    self.player.update(t)

  def render(self, t):
    self.player.render(t)

    self.canvas.create_text(
      30, 20, text='{} fps'.format(self.t_fps), fill='#FFFFFF')

  def get_time(self):
    # return int(round(time.time()) * 1000)
    return datetime.datetime.now().microsecond

  def handle_keys(self, e):
    if e.keycode == 113:  # left
      self.player.move_left()
    if e.keycode == 111:  # up
      self.player.move_up()
    if e.keycode == 114:  # right
      self.player.move_right()
    if e.keycode == 116:  # down
      self.player.move_down()
    if e.keycode == 30:  # u
      self.player.hurt(1)
    if e.keycode == 31:  # i
      self.player.heal(1)


  def handle_mouse(self, e):
    self.player.move_to(float(e.x), float(e.y))
        

if __name__ == '__main__':
  app = App()
