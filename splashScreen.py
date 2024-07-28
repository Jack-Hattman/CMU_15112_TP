from cmu_graphics import *
from Button import *

def getButtonPositions(app):

    buttonWidths = app.width / 6
    buttonHeights = app.height / 12

    buttonsY = app.height * (2/3)

    startX = (app.width / 2) - (buttonWidths * 3/2)
    
    helpX = (app.width / 2) + (buttonWidths * 1/2)

    return [startX, helpX, buttonsY, buttonWidths, buttonHeights]

def splashScreen_onAppStart(app):

    buttonColors = {
        'fill' : rgb(60, 60, 60),
        'pressedFill' : rgb(20, 20, 20),
        'borderColor' : rgb(240, 240, 240),
        'textColor' : rgb(240, 240, 240)
    }

    startX, helpX, buttonsY, buttonWidths, buttonHeights = getButtonPositions(app)
    
    app.splashStartButton = Button('Start', startX, buttonsY, buttonWidths, 
                                   buttonHeights, buttonColors)
    
    app.splashHelpButton = Button('Help', helpX, buttonsY, buttonWidths,
                                  buttonHeights, buttonColors)
    
def splashScreen_onMousePress(app, mouseX, mouseY):

    # Check if the buttons are pressed
    app.splashStartButton.checkIsPressed(mouseX, mouseY)
    app.splashHelpButton.checkIsPressed(mouseX, mouseY)

def splashScreen_onMouseRelease(app, mouseX, mouseY):

    # Check if the buttons are released
    start = app.splashStartButton.release(mouseX, mouseY)
    help = app.splashHelpButton.release(mouseX, mouseY)

    if start:
        app.lastScreen = 'splashScreen'
        setActiveScreen('gameScreen')

    if help:
        app.lastScreen = 'splashScreen'
        setActiveScreen('helpScreen')

def splashScreen_redrawAll(app):

    # Draw the background
    drawRect(0, 0, app.width, app.height)

    fontSize = (app.width + app.height) / 40

    titleX = app.width / 2
    titleY = app.height * (1/3)

    drawLabel('SUDOKU', titleX, titleY, size=fontSize, fill='white', 
              font='monospace', bold=True)
    
    app.splashStartButton.drawButton()
    app.splashHelpButton.drawButton()