from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Canvas and ball properties
WIDTH = 800
HEIGHT = 500
BALL_COUNT = 15
BALL_RADIUS = 15

class Ball:
    def __init__(self, id_num):
        self.id = id_num
        self.radius = BALL_RADIUS
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.vx = random.choice([-4, -3, -2, 2, 3, 4])
        self.vy = random.choice([-4, -3, -2, 2, 3, 4])
        # Bright vibrant styling using HSL 
        self.color = f"hsl({random.randint(0, 360)}, 85%, 60%)"

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Wall collisions handling 
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.vx *= -1
            self.x = max(self.radius, min(self.x, WIDTH - self.radius))
            
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.vy *= -1
            self.y = max(self.radius, min(self.y, HEIGHT - self.radius))

    def to_dict(self):
        return {'id': self.id, 'x': self.x, 'y': self.y, 'radius': self.radius, 'color': self.color}

# Instantiate our simulator environment
balls = [Ball(i) for i in range(BALL_COUNT)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
def update():
    for ball in balls:
        ball.move()
    return jsonify([ball.to_dict() for ball in balls])

if __name__ == '__main__':
    app.run(debug=True)
