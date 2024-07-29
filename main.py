from cmu_graphics import *
from Sudoku import *
from gameScreen import *
from helpScreen import *
from splashScreen import *

def onResize(app):

    # Update the game screen on resize

    # Learned has attribut from stack overflow
    #https://stackoverflow.com/questions/610883/how-to-check-if-an-object-has-an-attribute

    if hasattr(app, 'game'):

        boardDisplayArgs = findBoardDisplayArgs(app)
        
        NumDisplayList = findNumButtonDisplayList(app, boardDisplayArgs)
        buttonsLeft, buttonsY, buttonSize = NumDisplayList

        app.game.updateDisplayArgs(boardDisplayArgs)

        for num in range(1, 10):

            button = app.numButtons[num - 1]
            
            buttonPadding = (boardDisplayArgs['boardWidth'] - 9 * buttonSize) / 8
            buttonX = buttonsLeft + ((buttonSize + buttonPadding) * (num - 1))

            button.updateDisplayArgs(buttonX, buttonsY, buttonSize, buttonSize)
            
        helpX, quitX, buttonsY, buttonsW, buttonsH = findHelpAndQuitButtonArgs(app, boardDisplayArgs)

        app.helpButton.updateDisplayArgs(helpX, buttonsY, buttonsW, buttonsH)
        app.quitButton.updateDisplayArgs(quitX, buttonsY, buttonsW, buttonsH)

        notesAndHelpList = findNotesAndHintButtonArgs(app, boardDisplayArgs)
        buttonsX, buttonsTop, buttonWidths, buttonHeights = notesAndHelpList

        notesY = buttonsTop + 2 * buttonHeights

        for i in range(len(app.gameplayButtons)):
            
            if i == 0:
                y = buttonsTop
            elif i == 1:
                y = notesY

            userInput = app.gameplayButtons[i]

            userInput.updateDisplayArgs(buttonsX, y, buttonWidths, buttonHeights)



    # Update the splash screen on resize

    diffLeft, diffY, buttonWidths, buttonHeights = getDiffButtonPositions(app)
    helpX, helpY, helpW, helpH = getHelpButtonPosition(app)
    
    for i in range(len(app.difficultyButtons)):

        button = app.difficultyButtons[i]

        # 1.25 adds the padding
        diffX = diffLeft + (i * buttonWidths * 1.25)

        button.updateDisplayArgs(diffX, diffY, buttonWidths, buttonHeights)
    
    app.splashHelpButton.updateDisplayArgs(helpX, helpY, helpW, helpH)


    # Update the help screen on resize

    backX, backY, backWidth, backHeight = getButtonPosition(app)
    
    app.backButton.updateDisplayArgs(backX, backY, backWidth, backHeight)


def main():
    runAppWithScreens(initialScreen='splashScreen', width=600, height=600)

main()
