import random
import arcade

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SNAKE_SPPED = 5

class Snake(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 5
        self.height = 5
        self.color = arcade.color.AMERICAN_ROSE
        self.body_size = 0
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.speed = SNAKE_SPPED
        self.body_parts = []
        self.direction = "left"

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)

    def move(self, x, y):
        for part in range(len(self.body_parts)-1, 0,-1):
            new_center_x = self.body_parts[part-1].center_x
            new_center_y = self.body_parts[part - 1].center_y
            self.body_parts[part].center_x = new_center_x
            self.body_parts[part].center_y = new_center_y
        if self.center_x < x-1 and self.direction != "left":
            self.center_x += self.speed
            self.direction = "right"
        elif self.center_x > x+1 and self.direction != "right":
            self.center_x -= self.speed
            self.direction = "left"
        elif self.center_y < y-1 and self.direction != "down":
            self.center_y += self.speed
            self.direction = "up"
        elif self.center_y > y+1 and self.direction != "up":
            self.center_y -= self.speed
            self.direction = "down"
        else:
            self.center_x += self.speed
            self.center_y += self.speed
            self.direction = "up"

class Food(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.center_x = random.randint(5, 470)
        self.center_y = random.randint(5, 470)
        texture = arcade.load_texture("apple.png")
        self.texture = texture
        self.scale = 0.1

    def draw(self):
        arcade.draw_texture_rectangle(self.center_x, self.center_y, 25, 25, self.texture)

class Poop(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.center_x = random.randint(5, 470)
        self.center_y = random.randint(5, 470)
        texture = arcade.load_texture("poop.png")
        self.texture = texture
        self.scale = 0.1

    def draw(self):
        arcade.draw_texture_rectangle(self.center_x, self.center_y, 25, 25, self.texture)

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=500, height=500, title="Snake Game")
        arcade.set_background_color(arcade.color.SAND_DUNE)
        self.score = 0
        self.game_over = False
        self.snake = Snake()
        self.snake.color = arcade.color.SNOW
        self.snake.body_parts.append(self.snake)
        self.food = Food()
        self.poop = Poop()
        self.body_update()

    def on_draw(self):
        arcade.start_render()
        for part in self.snake.body_parts:
            part.draw()
        self.food.draw()
        self.poop.draw()
        arcade.draw_text("Snake Game",170,475,arcade.color.RED_ORANGE,20,5,"left",("calibri"),True,True)
        arcade.draw_text(f"Score: {self.score}", 12, 475, arcade.color.APPLE_GREEN, 15)
        if self.game_over == True:
            arcade.draw_text("GAME OVER", 133, 250, arcade.color.DARK_YELLOW, 28)

    def body_update(self):
        new_part = Snake()
        new_part.center_x = self.snake.body_parts[-1].center_x
        new_part.center_y = self.snake.body_parts[-1].center_y
        self.snake.body_parts.append(new_part)
        self.on_draw()

    def on_update(self, delta_time: 0.1):
        self.snake.move(self.food.center_x, self.food.center_y)
        if arcade.check_for_collision(self.snake, self.food):
            self.food.center_x = random.randint(5, 470)
            self.food.center_y = random.randint(5, 470)
            self.body_update()
            self.score += 2
        if arcade.check_for_collision(self.snake, self.poop):
            self.poop.center_x = random.randint(5, 470)
            self.poop.center_y = random.randint(5, 470)
            self.score -= 1 

        if self.snake.center_x > 500 or self.snake.center_x < 0 or self.snake.center_y > 500 or self.snake.center_y < 0:
            self.game_over= True

        if self.score < 0:
            self.game_over = True
        if self.game_over == True:
            return

game = Game()
arcade.run()