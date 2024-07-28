from cmu_graphics import *
from Sudoku import *
from gameScreen import *
from helpScreen import *
from splashScreen import *

def onResize(app):

    # Update the game screen on resize

    boardDisplayArgs = findBoardDisplayArgs(app)
    
    NumDisplayList = findNumButtonDisplayList(app, boardDisplayArgs)
    buttonsLeft, buttonsY, buttonSize = NumDisplayList

    app.game.updateDisplayArgs(boardDisplayArgs)

    for num in range(1, 10):

        button = app.numButtons[num - 1]
        
        buttonPadding = (boardDisplayArgs['boardWidth'] - 9 * buttonSize) / 8
        buttonX = buttonsLeft + ((buttonSize + buttonPadding) * (num - 1))

        button.updateDisplayArgs(buttonX, buttonsY, buttonSize, buttonSize)
        
    helpX, helpY, helpW, helpH = findHelpButtonArgs(app)
    app.helpButton.updateDisplayArgs(helpX, helpY, helpW, helpH)


    # Update the splash screen on resize

    startX, helpX, buttonsY, buttonWidths, buttonHeights = getButtonPositions(app)
    
    app.splashStartButton.updateDisplayArgs(startX, buttonsY, buttonWidths, buttonHeights)
    
    app.splashHelpButton.updateDisplayArgs(helpX, buttonsY, buttonWidths, buttonHeights)


    # Update the help screen on resize

    backX, backY, backWidth, backHeight = getButtonPosition(app)
    
    app.backButton.updateDisplayArgs(backX, backY, backWidth, backHeight)


def main():
    runAppWithScreens(initialScreen='splashScreen', width=600, height=600)

main()
