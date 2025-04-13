---
layout: default
title: Waves with JS
---

<canvas id="waveCanvas" width="600" height="300"></canvas>

<script src="https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"></script>

<script type="text/javascript">
async function main() {
    const pyodide = await loadPyodide();
    await pyodide.loadPackage(["numpy"]);

    await pyodide.runPythonAsync(`
import numpy as np
from js import document, performance

canvas = document.getElementById("waveCanvas")
ctx = canvas.getContext("2d")
width, height = canvas.width, canvas.height

N = 100
x = np.linspace(0, 1, N)
ps = [1, 2, 3, 4, 5]
c = 10
start = performance.now()

def draw(now):
    t = (now - start) / 50000
    ctx.clearRect(0, 0, width, height)
    ctx.beginPath()

    for i in range(N):
        xi = x[i]
        f = sum(np.sin(p * 2 * np.pi * xi) * np.cos(c * p * 2 * np.pi * t) for p in ps)
        y = height / 2 - f * 20
        px = xi * width
        if i == 0:
            ctx.moveTo(px, y)
        else:
            ctx.lineTo(px, y)

    ctx.strokeStyle = "blue"
    ctx.lineWidth = 2
    ctx.stroke()
    `);

    // Get Python draw function and create a JS proxy
    const draw = pyodide.globals.get("draw");
    const drawProxy = pyodide.toPy((now) => {
        draw(now);
        requestAnimationFrame(drawProxy);
    });

    requestAnimationFrame(drawProxy);
}

main();
</script>


