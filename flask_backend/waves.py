import os
from flask import Flask, send_file
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

app = Flask(__name__)

# Set the path to the 'static' folder inside 'flask_backend' directory explicitly
static_dir = os.path.join(os.path.dirname(__file__), 'static')

# Ensure the 'static' directory exists
if not os.path.exists(static_dir):
	os.makedirs(static_dir)

@app.route("/stuff")
def f():
	filename = os.path.join(static_dir, 'pschdn_1917.png')
	return send_file(filename, mimetype='image/png')

@app.route("/animation")
def serve_animation():
	# Full path to the animation file
	filename = os.path.join(static_dir, 'animation.gif')

	# If the animation doesn't exist, generate it
	if not os.path.exists(filename):
		generate_animation(filename)

	return send_file(filename, mimetype='image/gif')

def generate_animation(filename):
	# Example of generating a simple animation
	fig, ax = plt.subplots()
	x = np.linspace(0, 2 * np.pi, 200)
	line, = ax.plot(x, np.sin(x))

	def update(frame):
		line.set_ydata(np.sin(x + frame / 10.0))
		return line,

	ani = animation.FuncAnimation(fig, update, frames=100, interval=50)
	ani.save(filename, writer="pillow")  # Save as GIF using Pillow writer
	plt.close(fig)
	print(f"Animation saved as {filename}")
