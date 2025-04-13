from flask import Flask, request, send_file
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

matplotlib.use("Agg")

# Define the absolute path to the 'static' directory
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# Now pass the static folder path explicitly
app = Flask(__name__,static_folder=static_folder)

@app.route("/animation")
def generate_animation():
	#freq = float(request.args.get("frequency", 1.0))  # default = 1.0 Hz
	filename = "static/animation.gif"

	fig,ax = plt.subplots()
	x = np.linspace(0,1,250)
	line, = ax.plot( x,np.zeros(250) )
	ax.set_ylim(-4,4)

	dt = 2E-3
	c = 10

	def update(t):
		ps = [1,2,3,4,5]
		f = 0
		for p in ps:
			k = p * 2*np.pi
			omega = c * k
			f += np.sin(k*x) * np.cos(omega * t)
		line.set_ydata(f)
		return line,

	T = 0.1
	N_steps = int(T/dt)
	frames = np.linspace(0,T,N_steps)
	FPS = 60
	interval = (1/FPS) * 1000
	ani = animation.FuncAnimation(fig, update, frames=frames, blit=True, interval=interval)
	print("Saving GIF...")
	ani.save(filename, writer="pillow", fps=FPS)
	print("Saved!")
	plt.close()

	return send_file(filename, mimetype="image/gif")

#if __name__ == "__main__":
#	app.run(debug=True, port=5000)
