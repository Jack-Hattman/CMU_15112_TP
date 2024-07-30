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

def findHelpAndQuitButtonArgs(app, boardDisplayArgs):

    buttonW = app.width / 6
    buttonH = app.height / 12

    buttonsY = app.height / 60

    helpX = app.width - (buttonW * (5/4))

    quitX = boardDisplayArgs['boardX']

    argList = [helpX, quitX, buttonsY, buttonW, buttonH]

    return argList

def findNotesAndHintButtonArgs(app, boardDisplayArgs):

    buttonWidths = app.width / 6
    buttonHeights = app.height / 12

    buttonsTop = boardDisplayArgs['boardY']

    buttonsX = app.width - (buttonWidths * (5/4))

    argList = [buttonsX, buttonsTop, buttonWidths, buttonHeights]

    return argList

def gameScreen_onScreenActivate(app):

    boardDisplayArgs = findBoardDisplayArgs(app)

    colors = {
        'background' : rgb(20, 20, 20),
        'outerBorder' : rgb(220, 220, 220),
        'innerBorder' : rgb(160, 160, 160),
        'grid' : rgb(160, 160, 160),
        'initTile' : rgb(60, 60, 60),
        'tile' : rgb(40, 40, 40),
        'tileSelector' : rgb(200, 200, 200),
        'invalidTile' : rgb(255, 0, 0),
        'tileNum' : rgb(255, 255, 255),
        'notesNum' : rgb(200, 200, 200),
        'highlightTileNum' : rgb(0, 0, 0),
        'highlightNotesNum' : rgb(20, 20, 20),
        'hintColor' : rgb(255, 150, 0)
    }

    app.game = Sudoku(app.difficulty, 'manual', boardDisplayArgs, colors) 

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
        
        buttonPadding = (boardDisplayArgs['boardWidth'] - 9 * buttonSize) / 8
        buttonX = buttonsLeft + ((buttonSize + buttonPadding) * (num - 1))

        app.numButtons.append(Button(num, buttonX, buttonsY, buttonSize, 
                                     buttonSize, buttonColors))
        
    # Create help and quit button
    helpX, quitX, buttonsY, buttonsW, buttonsH = findHelpAndQuitButtonArgs(app, boardDisplayArgs)

    app.helpButton = Button('Help', helpX, buttonsY, buttonsW, buttonsH, buttonColors)
    app.quitButton = Button('Quit', quitX, buttonsY, buttonsW, buttonsH, buttonColors)

    # Create the note and help Buttons
    notesAndHelpList = findNotesAndHintButtonArgs(app, boardDisplayArgs)
    buttonsX, buttonsTop, buttonWidths, buttonHeights = notesAndHelpList

    app.gameplayButtonPadding = 0.25 * (boardDisplayArgs['boardHeight'] - 5 * buttonHeights)

    notesY = buttonsTop + (app.gameplayButtonPadding + buttonHeights)
    hintY = buttonsTop + 2 * (app.gameplayButtonPadding + buttonHeights)
    deleteY = buttonsTop + 3 * (app.gameplayButtonPadding + buttonHeights)
    solveY = buttonsTop + 4 * (app.gameplayButtonPadding + buttonHeights)

    autoNotesToggle = Toggle('Auto Notes', buttonsX, buttonsTop, buttonWidths, buttonHeights, buttonColors)
    notesModeToggle = Toggle('Notes', buttonsX, notesY, buttonWidths, buttonHeights, buttonColors)
    hintButton = Button('Hint', buttonsX, hintY, buttonWidths, buttonHeights, buttonColors)
    deleteButton = Button('Delete', buttonsX, deleteY, buttonWidths, buttonHeights, buttonColors)
    solveButton = Button('Solve', buttonsX, solveY, buttonWidths, buttonHeights, buttonColors)

    app.gameplayButtons = [autoNotesToggle, notesModeToggle, hintButton, deleteButton, solveButton]

def gameScreen_onKeyPress(app, key):
        
    if key in ['up', 'down', 'left', 'right']:
        app.game.moveTileSelector(key=key)

    elif key.isdigit() and key != '0':
        app.game.placeNum(key)

    elif key == 'backspace':
        app.game.removeNum()

    elif key == 'm':
        app.game.toggleMode()

        # This is the index of the auto notes button
        notesModeButton = app.gameplayButtons[0]
        notesModeButton.isPressed = not notesModeButton.isPressed

    elif key == 'n':
        app.game.toggleNotes()

        # This is the index of the notes button
        notesButton = app.gameplayButtons[1]
        notesButton.isPressed = not notesButton.isPressed

    elif key == 'h':
        app.game.generateHint()

    elif key == 's':
        app.game.board = app.game.solvedBoard

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

    # Check if the help or quit button is pressed
    app.helpButton.checkIsPressed(mouseX, mouseY)
    app.quitButton.checkIsPressed(mouseX, mouseY)

    # Check if notes or hint was pressed
    for userInput in app.gameplayButtons:
        userInput.checkIsPressed(mouseX, mouseY)

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
    quit = app.quitButton.release(mouseX, mouseY)

    if help:
        app.lastScreen = 'gameScreen'
        setActiveScreen('helpScreen')

    if quit:
        setActiveScreen('splashScreen')

    # Check if notes or hint was pressed
    for i in range(len(app.gameplayButtons)):
        
        userInput = app.gameplayButtons[i]

        pressed = userInput.release(mouseX, mouseY)

        if pressed:
            if i == 0:
                app.game.toggleMode()
            elif i == 1:
                app.game.toggleNotes()
            elif i == 2:
                app.game.generateHint()
            elif i == 3:
                app.game.removeNum()
            elif i == 4:
                app.game.board = app.game.solvedBoard

def gameScreen_redrawAll(app):
    app.game.drawBoard(app)
    app.game.drawTileSelector(app)
    
    for button in app.numButtons:
        button.drawButton()

    app.helpButton.drawButton()
    app.quitButton.drawButton()

    # Check if notes or hint was pressed
    for userInput in app.gameplayButtons:
        userInput.drawButton()
        

