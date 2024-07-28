from cmu_graphics import *
from Sudoku import *
from Button import *

def findBoardDisplayArgs(app):

    # Just initialize the size/shape of the board
    # Numbers are arbitrarilly tweaked
    boardX = app.width / 12
    boardY = app.height / 6
    boardWidth = app.width * (2/3)
    boardHeight = app.height * (2/3)
    padding = (app.width + app.height) / 300
    fontSize = (boardHeight + boardWidth) / 40

    boardDisplayArgs = {
        'boardX' : boardX,
        'boardY' : boardY,
        'boardWidth' : boardWidth,
        'boardHeight' : boardHeight,
        'padding' : padding,
        'fontSize' : fontSize,
        'font' : 'monospace'
    }

    return boardDisplayArgs

def findNumButtonDisplayList(app, boardDisplayArgs):

    padding = boardDisplayArgs['padding']
    boardX = boardDisplayArgs['boardX']
    boardY = boardDisplayArgs['boardY']
    boardWidth = boardDisplayArgs['boardWidth']
    boardHeight = boardDisplayArgs['boardHeight']

    buttonPadding = padding * 2

    # How below the board the buttons should be
    buttonDist = boardHeight / 20

    # Create the size of the buttons so the fit nicely
    # *8 because we dont care about padding after the 9 button
    buttonWidth = boardWidth
    buttonSize = (buttonWidth - (buttonPadding * 8)) / (app.game.gridSize ** 2)

    buttonsLeft = boardX
    buttonsY = boardY + boardHeight + buttonDist

    buttonDisplayList = [buttonsLeft, buttonsY, buttonSize]

    return buttonDisplayList

def findHelpButtonArgs(app):

    helpW = app.width / 6
    helpH = app.height / 12

    helpX = app.width - (helpW * (5/4))
    helpY = app.height / 60

    argList = [helpX, helpY, helpW, helpH]

    return argList

def gameScreen_onAppStart(app):

    boardDisplayArgs = findBoardDisplayArgs(app)

    colors = {
        'background' : rgb(20, 20, 20),
        'outerBorder' : rgb(220, 220, 220),
        'innerBorder' : rgb(160, 160, 160),
        'grid' : rgb(160, 160, 160),
        'initTile' : rgb(60, 60, 60),
        'tile' : rgb(40, 40, 40),
        'tileSelector' : rgb(200, 200, 200),
        'invalidTile' : rgb(200, 0, 0),
        'tileNum' : rgb(255, 255, 255),
        'notesNum' : rgb(200, 200, 200),
        'highlightTileNum' : rgb(0, 0, 0),
        'highlightNotesNum' : rgb(20, 20, 20)
    }
    app.game = Sudoku('easy', 'auto', boardDisplayArgs, colors) 

    NumDisplayList = findNumButtonDisplayList(app, boardDisplayArgs)
    buttonsLeft, buttonsY, buttonSize = NumDisplayList

    buttonColors = {
        'fill' : rgb(60, 60, 60),
        'pressedFill' : rgb(20, 20, 20),
        'borderColor' : rgb(240, 240, 240),
        'textColor' : rgb(240, 240, 240)
    }

    # Make an array to store the number buttons
    app.numButtons = []

    for num in range(1, 10):
        
        buttonPadding = buttonSize * 0.25
        buttonX = buttonsLeft + ((buttonSize + buttonPadding) * (num - 1))

        app.numButtons.append(Button(num, buttonX, buttonsY, buttonSize, 
                                     buttonSize, buttonColors))
        
    # Create help button
    helpX, helpY, helpW, helpH = findHelpButtonArgs(app)

    app.helpButton = Button('Help', helpX, helpY, helpW, helpH, buttonColors)

def gameScreen_onKeyPress(app, key):
        
    if key in ['up', 'down', 'left', 'right']:
        app.game.moveTileSelector(key=key)

    elif key.isdigit() and key != '0':
        app.game.placeNum(key)

    elif key == 'backspace':
        app.game.removeNum()

    elif key == 'm':
        app.game.toggleMode()

    elif key == 'n':
        app.game.toggleNotes()

def gameScreen_onMousePress(app, mouseX, mouseY):

    # Extract the display args so the variables are smaller
    boardX = app.game.displayArgs['boardX']
    boardY = app.game.displayArgs['boardY']
    boardWidth = app.game.displayArgs['boardWidth']
    boardHeight = app.game.displayArgs['boardHeight']

    # Check if the mouse is pressed in the board
    if (boardX <= mouseX <= boardX + boardWidth and
        boardY <= mouseY <= boardY + boardHeight):
        app.game.moveTileSelector(mouse=(mouseX, mouseY))

    # Check if any number buttons are pressed
    for button in app.numButtons:
        button.checkIsPressed(mouseX, mouseY)

    # Check if the help button is pressed
    app.helpButton.checkIsPressed(mouseX, mouseY)

def gameScreen_onMouseRelease(app, mouseX, mouseY):

    # Check if any of the buttons have been released
    for i in range(len(app.numButtons)):

        num = i + 1

        # Add that number to the board
        button = app.numButtons[i]
        action = button.release(mouseX, mouseY)

        if action:
            app.game.placeNum(num)

    # Check if the help button is released
    help = app.helpButton.release(mouseX, mouseY)

    if help:
        setActiveScreen('helpScreen')

def onResize(app):

    boardDisplayArgs = findBoardDisplayArgs(app)
    
    NumDisplayList = findNumButtonDisplayList(app, boardDisplayArgs)
    buttonsLeft, buttonsY, buttonSize, buttonBorderWidth = NumDisplayList

    app.game.updateDisplayArgs(boardDisplayArgs)

    for num in range(1, 10):

        button = app.numButtons[num - 1]
        
        buttonPadding = buttonBorderWidth * 4
        buttonX = buttonsLeft + ((buttonSize + buttonPadding) * (num - 1))

        button.updateDisplayArgs(buttonX, buttonsY, buttonSize, buttonSize,
                                 buttonBorderWidth)
        
    helpX, helpY, helpW, helpH, helpBorderW = findHelpButtonArgs(app)
    app.helpButton.updateDisplayArgs(helpX, helpY, helpW, helpH, helpBorderW)

def gameScreen_redrawAll(app):
    app.game.displayBoard(app)
    app.game.drawTileSelector(app)
    
    for button in app.numButtons:
        button.drawButton()

    app.helpButton.drawButton()
        
    drawLabel(f'Mode: {app.game.mode}', 300, 30, fill='white', size=30, font='monospace')
    drawLabel(f'Is notes mode: {app.game.isNotesMode}', 300, 70, fill='white', size=30)

