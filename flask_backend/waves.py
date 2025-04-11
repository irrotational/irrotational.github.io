import os
from flask import Flask, send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Flask backend running."

@app.route("/animation")
def serve_animation():
    filename = "static/animation.gif"

    if not os.path.exists(filename):
        generate_animation(filename)

    return send_file(filename, mimetype="image/gif")

def generate_animation(filename):
    fig, ax = plt.subplots()
    x = np.linspace(0, 2 * np.pi, 200)
    line, = ax.plot(x, np.sin(x))

    def update(frame):
        line.set_ydata(np.sin(x + frame / 10.0))
        return line,

    ani = animation.FuncAnimation(fig, update, frames=100, interval=50)
    ani.save(filename, writer="pillow")  # Save as GIF using Pillow writer
    plt.close(fig)  # Clean up to avoid memory leaks
