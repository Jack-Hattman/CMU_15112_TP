from cmu_graphics import *

def splashScreen_onAppStart(app):
    pass

def splashScreen_redrawAll(app):

    # Draw the background
    drawRect(0, 0, app.width, app.height)

    fontSize = (app.width + app.height) / 40

    titleX = app.width / 2
    titleY = app.height * (1/3)

    drawLabel('SUDOKU', titleX, titleY, size=fontSize, fill='white', font='monospace', bold=True)