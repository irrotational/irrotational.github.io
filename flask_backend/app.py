from flask import Flask, send_file
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import io

app = Flask(__name__)

@app.route("/animation")
def serve_animation():
    fig, ax = plt.subplots()
    x, y = [], []
    line, = ax.plot([], [], lw=2)

    def init():
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        return line,

    def update(frame):
        x.append(frame)
        y.append(frame)
        line.set_data(x, y)
        return line,

    ani = FuncAnimation(fig, update, frames=range(10), init_func=init, blit=True)

    buf = io.BytesIO()
    ani.save(buf, format='gif', writer='pillow')
    buf.seek(0)

    return send_file(buf, mimetype='image/gif')
