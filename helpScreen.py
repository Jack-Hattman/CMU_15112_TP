from cmu_graphics import *
from Button import *

def getTextArgs(app):

    textTop = app.height / 6
    fontSize = min(app.width, app.height) / 70

    return textTop, fontSize

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
    
    bButton = Button('Back', backX, backY, backWidth, backHeight, buttonColors)
    app.backButton = bButton

    # From NYT Sudoku rules
    app.helpMessage = '''\
        How to play Sudoku/T

        Fill each 3 x 3 set with numbers 1–9./S

            Tap a cell in any set, then select a number./b
            Fill cells until the board is complete. Numbers in blocks,/b
            rows or columns cannot repeat./b
            Note: Each number can only appear on the board 9 times./b

        Play modes and tips/T

            Normal mode: Press the number button or key to place that number/b

            Notes mode: Press the Notes button or 'n' to toggle whether you/b
            can take notes. In notes mode you can add or remove note numbers./b

            Auto Notes: Press the Auto Notes button or 'm' to toggle whether/b
            the board automatically takes notes for you./b

            Hints: press the hint button or 'h' to highlight a cell with a clear/b
            move. Press the button again to automatically make the move./b'''
    
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

    textArgs = {
        '/T' : 4,
        '/S' : 2.5,
        '/b' : 1.5
    }

    # This is a way to make it resize properly
    # Im not putting it in the resize function in main because its so small
    curY, fontSize = getTextArgs(app)
    center = app.width / 2

    for line in app.helpMessage.splitlines():

        if len(line) > 2:
            line = line.strip()

            modifier = line[-2:]

            if modifier == '/T':
                lineFontSize = fontSize * textArgs['/T']
                bold = True
            elif modifier == '/S':
                lineFontSize = fontSize * textArgs['/S']
                bold = True
            elif modifier == '/b':
                lineFontSize = fontSize * textArgs['/b']
                bold = True

            curY += lineFontSize / 1.25

            drawLabel(line[:-2], center, curY, size=lineFontSize, fill='white', 
                      bold=bold, font='monospace')

            curY += lineFontSize / 1.25
    
    app.backButton.drawButton()