from cmu_graphics import *
from Button import *

def getDiffButtonPositions(app):

    buttonWidths = app.width / 7
    buttonHeights = app.height / 16

    diffPadding = buttonWidths * 0.25

    diffY = app.height * (1/2)

    diffLeft = (app.width / 2) - ((buttonWidths * 5 + diffPadding * 4) / 2)

    return [diffLeft, diffY, buttonWidths, buttonHeights]

def getHelpButtonPosition(app):

    helpWidth = app.width / 6
    helpHeight = app.height / 12

    helpY = app.height * (5/6)
    helpX = (app.width / 2) - (helpWidth / 2)

    return [helpX, helpY, helpWidth, helpHeight]

def splashScreen_onAppStart(app):

    app.currentGame = None

    buttonColors = {
        'fill' : rgb(60, 60, 60),
        'pressedFill' : rgb(20, 20, 20),
        'borderColor' : rgb(240, 240, 240),
        'textColor' : rgb(240, 240, 240)
    }

    diffLeft, diffY, buttonWidths, buttonHeights = getDiffButtonPositions(app)
    helpX, helpY, helpW, helpH = getHelpButtonPosition(app)

    app.difficultyButtons = []

    app.difficulties = ['easy', 'medium', 'hard', 'expert', 'evil']

    for i in range(len(app.difficulties)):
        difficulty = app.difficulties[i]

        # 1.25 adds the padding
        diffX = diffLeft + (i * buttonWidths * 1.25)

        diffButton = Button(difficulty, diffX, diffY, buttonWidths, buttonHeights, buttonColors)
        app.difficultyButtons.append(diffButton)
    
    app.splashHelpButton = Button('Help', helpX, helpY, helpW, helpH, buttonColors)
    
def splashScreen_onMousePress(app, mouseX, mouseY):

    # Check if the buttons are pressed
    for button in app.difficultyButtons:
        button.checkIsPressed(mouseX, mouseY)

    app.splashHelpButton.checkIsPressed(mouseX, mouseY)

def splashScreen_onMouseRelease(app, mouseX, mouseY):

    # Check if the buttons are released
    for i in range(len(app.difficultyButtons)):
        button = app.difficultyButtons[i]
        difficulty = app.difficulties[i]

        start = button.release(mouseX, mouseY)

        if start:
            app.game = None
            app.difficulty = difficulty
            app.lastScreen = 'splashScreen'
            setActiveScreen('gameScreen')


    help = app.splashHelpButton.release(mouseX, mouseY)

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
    
    for button in app.difficultyButtons:
        button.drawButton()

    app.splashHelpButton.drawButton()