import matplotlib
matplotlib.use('Agg')  # Force Agg backend to avoid threading issues

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import tempfile
from flask import Flask, send_file

app = Flask(__name__)

@app.route("/animation")
def animation():

    N_frames = 50
    x = np.linspace(0, 1, 250)
    ts = np.linspace(0, 2, N_frames)

    # Function to update the animation
    def wave(t, line):
        ps = [1,2,3,4,5,6]
        y_data = np.zeros_like(x)
        for p in ps:
            y_data += np.sin(p * np.pi * x) * np.sin(p * np.pi * t)
        line.set_data(x, y_data)
        return line,

    # Set up the plot
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1)  # Set the x-axis range
    ax.set_ylim(-10, 10)  # Set the y-axis range (adjust this as necessary)
    line, = ax.plot([], [], lw=2)

    # Create the animation
    ani = FuncAnimation(fig, wave, ts, fargs=[line], interval=50, blit=True)

    # Save the animation as a GIF in a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as tmp_file:
        tmp_file_path = tmp_file.name  # Get the file path
        ani.save(tmp_file_path, writer=PillowWriter(fps=30))  # Save with a suitable fps (adjust if necessary)

    # Send the animation as a response
    return send_file(tmp_file_path, mimetype='image/gif')

if __name__ == "__main__":
    app.run(debug=True, port=5050)
