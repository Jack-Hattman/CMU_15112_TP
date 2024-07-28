from cmu_graphics import *
from Button import *

def getButtonPosition(app):

    backWidth = app.width / 6
    backHeight = app.height / 12

    backX = backWidth * 0.5
    backY = backHeight * 0.5

    return [backX, backY, backWidth, backHeight]

def helpScreen_onAppStart(app):

    buttonColors = {
        'fill' : rgb(60, 60, 60),
        'pressedFill' : rgb(20, 20, 20),
        'borderColor' : rgb(240, 240, 240),
        'textColor' : rgb(240, 240, 240)
    }

    backX, backY, backWidth, backHeight = getButtonPosition(app)
    
    app.backButton = Button('Back', backX, backY, backWidth, backHeight, buttonColors)
    
    
def helpScreen_onMousePress(app, mouseX, mouseY):

    # Check if the buttons are pressed
    app.backButton.checkIsPressed(mouseX, mouseY)

def helpScreen_onMouseRelease(app, mouseX, mouseY):

    # Check if the buttons are released
    back = app.backButton.release(mouseX, mouseY)

    if back:
        setActiveScreen(app.lastScreen)
    
def helpScreen_redrawAll(app):

    # Draw the background
    drawRect(0, 0, app.width, app.height)
    
    app.backButton.drawButton()