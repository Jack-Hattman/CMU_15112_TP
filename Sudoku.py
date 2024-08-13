from cmu_graphics import *
import random
import copy

class Sudoku():

    def __init__(self, difficulty, mode, displayArgs, colorTheme):

        # Store the mode, auto vs manual
        self.mode = mode
        self.isNotesMode = False

        # Initialize the board, and solved board variables
        self.board = Sudoku.getBoard(difficulty)
        self.solvedBoard = Sudoku.solve(self)

        # Keep track of the initial cells
        self.initCells = Sudoku.findInitCells(self.board)

        # Generate the notes board for manual and auto
        self.manualNotes = Sudoku.generateManualNotes(self)
        self.legalNums = Sudoku.generateAutoNotes(self)

        # Keep track of useful varibles in the instance
        self.gridSize = int(len(self.board) ** 0.5)
        self.selectedTile = (0, 0)

        # Store the display varibles in dictionarys so its not to big
        self.displayArgs = displayArgs
        self.colorTheme = colorTheme

        # Keep track of any cells with hints
        self.hint = set()

        # Store a variable for if the board is solved
        self.isSolved = False

    ################################
    ##                            ##
    ##       LOGIC SECTION        ##
    ##                            ##
    ################################

    # A large portion of this logic is from homework

    def getBoard(difficulty):
        # Create a map based on how many board of each diff there are
        diffDict = {'easy' : 50, 'medium' : 50, 'hard' : 50, 
                    'expert' : 25, 'evil' : 25}
        
        # Get a random board of the desired difficulty
        boardNum = str(random.randint(1, diffDict[difficulty]))

        if len(boardNum) == 1:
            boardNum = '0' + boardNum

        # Create the proper file name
        fileName = 'boards\\' + difficulty + '-' + str(boardNum) + '.png.txt'

        # Reads the file and puts it into the contents variable
        # Taken from the syllabus instructions
        with open(fileName, "rt") as f:
            contents = f.read()

        # Initialize the board variable
        board = []

        # Add each line to the board
        # Nested loop is needed because numbers are strings rn
        for line in contents.splitlines():
            curLine = []
            for num in line.split(' '):
                curLine.append(int(num))

            board.append(curLine)

        return board
    
    def getPotentialNums(board, row, col):

        # Create a set containing all numbers 1 - boardSize
        potNums = set(range(1, len(board) + 1))

        # Initialize variables for the block check
        blockSize = int(len(board) ** 0.5)
        blockRow, blockCol = row // blockSize, col // blockSize


        rowNums = set(board[row])
        colNums = set()
        blockNums = set(Sudoku.flatten(Sudoku.extractBlock(board, blockRow, blockCol)))

        for i in range(len(board)):
            colNums.add(board[i][col])

        potNums -= (colNums | rowNums)
        potNums -= blockNums

        return potNums
    
    def generateAutoNotes(self):

        autoNotes = [[] for _ in range(len(self.board))]
        
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):

                # Dont add notes to the initial tiles
                if (i, j) in self.initCells:
                    autoNotes[i].append(set())
                else:
                    # Create a list of all potential values for each tile
                    autoNotes[i].append(Sudoku.getPotentialNums(self.board, i, j))

        return autoNotes
    
    def generateManualNotes(self):

        # Initialize both boards
        manualNotes = [[] for _ in range(len(self.board))]

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                
                # Just initialize each tile to be an empty set of notes
                manualNotes[i].append(set())

        return manualNotes

    def flatten(L):
        flattenedList = []

        for row in L:
            flattenedList += row

        return flattenedList

    def findEmptyCells(board):
        emptyCells = []

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    emptyCells.append((i, j))

        return emptyCells
    
    def findInitCells(board):
        initCells = set()

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != 0:
                    initCells.add((i, j))

        return initCells

    def areValidNums(L, maxNum):
        numSet = set()

        # Just make sure no number appears more than once
        # and that all the numbers are below the max number
        for i in range(len(L)):
            if L[i] == 0:
                continue

            if L[i] in numSet or L[i] > maxNum:
                return False

            numSet.add(L[i])

        return True

    def isLegalCol(board, colIndx):
        numSet = set()

        for i in range(len(board)):
            if board[i][colIndx] == 0:
                continue

            if board[i][colIndx] in numSet or board[i][colIndx] > len(board):
                return False

            numSet.add(board[i][colIndx])

        return True

    def isLegalRow(board, rowIndx):
        row = board[rowIndx]

        return Sudoku.areValidNums(row, len(board))

    def isLegalBlock(block):
        maxVal = len(block) ** 2
        flattenedList = Sudoku.flatten(block)

        return Sudoku.areValidNums(flattenedList, maxVal)

    def extractBlock(board, brow, bcol):

        # Use list slicing to isolate the desired block
        bsize = int(len(board) ** 0.5)
        startRow, stopRow = bsize * brow, bsize * (brow + 1)
        startCol, stopCol = bsize * bcol, bsize * (bcol + 1)

        bFullRow = board[startRow:stopRow]

        block = [row[startCol:stopCol] for row in bFullRow]

        return block

    def areBlocksLegal(board):
        bsize = int(len(board) ** 0.5)

        for i in range(bsize):
            for j in range(bsize):
                block = Sudoku.extractBlock(board, i, j)
                if not Sudoku.isLegalBlock(block):
                    return False

        return True

    def areRowsLegal(board):
        for i in range(len(board)):
            if not Sudoku.isLegalRow(board, i):
                return False

        return True

    def areColsLegal(board):
        for j in range(len(board[0])):
            if not Sudoku.isLegalCol(board, j):
                return False

        return True

    def isLegalBoard(board):
        if (Sudoku.areRowsLegal(board) and Sudoku.areColsLegal(board)
             and Sudoku.areBlocksLegal(board)):
            return True

        return False

    def isSolvedBoard(board):
        return (Sudoku.isLegalBoard(board) and 
                len(Sudoku.findEmptyCells(board)) == 0)

    def solve(self):
        emptyCells = Sudoku.findEmptyCells(self.board)
        board = copy.deepcopy(self.board)
        return Sudoku.solveHelper(board, emptyCells)

    def solveHelper(board, emptyCells):
        if emptyCells == []:
            return board

        else:
            
            leastLegals = 10
            pos = None

            # Find the cell with the least legal values
            for i in range(len(emptyCells)):
                potRow, potCol = emptyCells[i]
                curLegals = Sudoku.getPotentialNums(board, potRow, potCol)
                if len(curLegals) < leastLegals:
                    leastLegals = len(curLegals)
                    row, col = potRow, potCol
                    pos = i

            empty = emptyCells.pop(pos)

            potNums = Sudoku.getPotentialNums(board, row, col)

            # Backtracking Loop
            for num in potNums:

                board[row][col] = num

                sol = Sudoku.solveHelper(board, emptyCells)
                if sol != None:
                    return sol

                board[row][col] = 0

            emptyCells.insert(pos, empty)

        return None
    
    def toggleMode(self):
        if self.mode == 'auto':
            self.mode = 'manual'
        else:
            self.mode = 'auto'

    def toggleNotes(self):
        self.isNotesMode = not self.isNotesMode

    def moveTileSelector(self, key=None, mouse=None):

        # Handle the case of arrowkeys
        if key != None:
            row, col = self.selectedTile
            if key == 'up' and row > 0:
                self.selectedTile = (row-1, col)
            elif key == 'down' and row < len(self.board) - 1:
                self.selectedTile = (row+1, col)
            elif key == 'left' and col > 0:
                self.selectedTile = (row, col-1)
            elif key == 'right' and col < len(self.board[0]) - 1:
                self.selectedTile = (row, col+1)

        elif mouse != None:

            mX, mY = mouse
            
            # Extract the display args so the variables are smaller
            boardX = self.displayArgs['boardX']
            boardY = self.displayArgs['boardY']
            boardWidth = self.displayArgs['boardWidth']
            boardHeight = self.displayArgs['boardHeight']
            padding = self.displayArgs['padding']

            # This just makes the board scale with 2x2 and 3x3
            paddingLayers = self.gridSize + 1

            boxHeight = (boardHeight - (paddingLayers * padding)) / self.gridSize
            boxWidth = (boardWidth - (paddingLayers * padding)) / self.gridSize

            # Find the row and col the mouse pressed on
            boxRow = int((mY - boardY) // (boxHeight + padding))
            totPadding = (boxRow + 1) * padding
            row = int((mY - boardY - totPadding) // (boxHeight / 3))

            boxCol = int((mX - boardX) // (boxWidth + padding))
            totPadding = (boxCol + 1) * padding
            col = int((mX - boardX - totPadding) // (boxWidth / 3))

            self.selectedTile = (row,col)

    def placeNum(self, val):
        row, col = self.selectedTile

        # Exit if user is trying to place on an initial cell
        if (row, col) in self.initCells:
            return

        # Check if notes mode is activated
        if self.isNotesMode:
            if self.mode == 'manual':
                if int(val) in self.manualNotes[row][col]:
                    self.manualNotes[row][col].remove(int(val))
                else:
                    self.manualNotes[row][col].add(int(val))

        else:
            self.board[row][col] = int(val)

            if (self.hint != set() and (row, col) in self.hint and 
                self.solvedBoard[row][col] == self.board[row][col]):
                self.hint.remove((row, col))
                self.legalNums = Sudoku.generateAutoNotes(self)

            if self.mode == 'auto':
                self.legalNums = Sudoku.generateAutoNotes(self)

            self.isSolved = Sudoku.isSolvedBoard(self.board)

    def removeNum(self):
        row, col = self.selectedTile

        if (row, col) not in self.initCells:
            self.board[row][col] = 0

            if self.mode == 'auto':
                self.legalNums = Sudoku.generateAutoNotes(self)

    def isValidTile(self, row, col):
        if (row, col) in self.initCells:
            return True
        
        elif self.board[row][col] == 0:
            return True
        
        elif self.board[row][col] == self.solvedBoard[row][col]:
            return True
    
        return False
    
    def generateHint(self):

        if self.hint != set():
            for (row, col) in self.hint:
                self.board[row][col] = self.solvedBoard[row][col]

            self.hint = set()
            self.legalNums = Sudoku.generateAutoNotes(self)

        else:
            # Go through the board of legal nums
            for i in range(len(self.legalNums)):
                for j in range(len(self.legalNums[i])):
                    if (len(self.legalNums[i][j]) == 1 and 
                        self.board[i][j] != self.solvedBoard[i][j]):
                        self.hint = {(i, j)}

    ################################
    ##                            ##
    ##      DISPLAY SECTION       ##
    ##                            ##
    ################################

    def getTilePosAndSize(self, app, row, col):

        # Extract the display args so the variables are smaller
        boardX = self.displayArgs['boardX']
        boardY = self.displayArgs['boardY']
        boardWidth = self.displayArgs['boardWidth']
        boardHeight = self.displayArgs['boardHeight']
        padding = self.displayArgs['padding']

        # This just makes the board scale with 2x2 and 3x3
        paddingLayers = self.gridSize + 1

        boxHeight = (boardHeight - (paddingLayers * padding)) / self.gridSize
        boxWidth = (boardWidth - (paddingLayers * padding)) / self.gridSize

        tileHeight = boxHeight / self.gridSize
        tileWidth = boxWidth / self.gridSize

        # This just makes sure the tiles respect the larger grid boundaries
        blockCol = col // self.gridSize
        blockRow = row // self.gridSize

        x = boardX + padding + (col * tileWidth) + (padding * blockCol)
        y = boardY + padding + (row * tileHeight) + (padding * blockRow)

        return x, y, tileWidth, tileHeight

    def drawGrid(app, x, y, w, h, rows, cols, borderCol='black', 
                 borderWidth='0', fill=None):

        boxHeight = h / rows
        boxWidth = w / cols

        for row in range(rows):
            for col in range(cols):
                tileX = x + col * boxWidth
                tileY = y + row * boxHeight

                drawRect(tileX, tileY, boxWidth, boxHeight, border=borderCol, 
                        borderWidth=borderWidth, fill=fill)
                
    def drawNotes(self, app, row, col):

        # Get the font
        font=self.displayArgs['font']

        if self.board[row][col] != 0:
            return

        if self.mode == 'auto':
            curNotes = self.legalNums
        else:
            curNotes = self.manualNotes

        fontSize = self.displayArgs['fontSize'] / 1.5

        # Change the color if the tile is highlighted
        if (row, col) == self.selectedTile:
            textColor = self.colorTheme['highlightNotesNum']
        else:
            textColor = self.colorTheme['notesNum']

        # Get the variables appropriate to the tile
        x, y, w, h = Sudoku.getTilePosAndSize(self, app, row, col)
        cx = x + w / 2
        cy = y + h / 2

        # This just hardcodes where each number goes in the notes
        dirMap = {1 : (-1, -1), 2 : (0, -1), 3 : (1, -1), 4 : (-1, 0), 5 : (0, 0),
                   6 : (1, 0), 7 : (-1, 1), 8 : (0, 1), 9 : (1, 1)}
        
        for num in curNotes[row][col]:
            dx, dy = dirMap[num]
            dx *= w / 3
            dy *= h / 3

            noteX = cx + dx
            noteY = cy + dy

            drawLabel(num, noteX, noteY, fill=textColor, size=fontSize, font=font, bold=True)

    def highlightCell(self, app, row, col, color):

        x, y, w, h = Sudoku.getTilePosAndSize(self, app, row, col)
        borderWidth = self.displayArgs['padding'] / 1.25


        # CMU graphics is weird with no fill and colored border
        drawRect(x, y, borderWidth, h, fill=color)
        drawRect(x, y, w, borderWidth, fill=color)
        drawRect(x + w - borderWidth, y, borderWidth, h, fill=color)
        drawRect(x, y + h - borderWidth, w, borderWidth, fill=color)

    def drawTile(self, app, row, col, num, tileFill='default', borderWidth=0):

        # Get the font
        font=self.displayArgs['font']

        x, y, w, h = Sudoku.getTilePosAndSize(self, app, row, col)

        # Handle the case of the highlight being on an empty cell
        if num == 0:
            tileFill = None if tileFill == 'default' else tileFill
            text = ''
        else:
            text = num

        # This ensures set tiles have a different background than userplaced tiles
        if tileFill == 'default': 
            if (row, col) in self.initCells:
                tileFill = self.colorTheme['initTile']
            else:
                tileFill = self.colorTheme['tile']
            textCol = self.colorTheme['tileNum']
        else:
            textCol = self.colorTheme['highlightTileNum']

        fontSize = self.displayArgs['fontSize']
        borderCol = self.colorTheme['grid']

        drawRect(x, y, w, h, fill=tileFill, border=borderCol, borderWidth=borderWidth)
        drawLabel(text, x + w/2, y + h/2, size=fontSize, fill=textCol, font=font, bold=True)      

        # Add a red border if the tile is wrong
        # Checks if a tile has the wrong value in auto mode
        if not Sudoku.isValidTile(self, row, col):
            invalidBorderCol = self.colorTheme['invalidTile']
            Sudoku.highlightCell(self, app, row, col, invalidBorderCol)

        # Add a yellow border if the tile is part of a hint
        elif self.hint != set() and (row, col) in self.hint:
            hintColor = self.colorTheme['hintColor']
            Sudoku.highlightCell(self, app, row, col, hintColor) 

        Sudoku.drawNotes(self, app, row, col)


    def drawBoard(self, app):

        # Extract the display args so the variables are smaller
        boardX = self.displayArgs['boardX']
        boardY = self.displayArgs['boardY']
        boardWidth = self.displayArgs['boardWidth']
        boardHeight = self.displayArgs['boardHeight']
        padding = self.displayArgs['padding']

        # Draw the background color
        drawRect(0, 0, app.width, app.height, fill=self.colorTheme['background'])

        # Draw big grid
        x = boardX + padding / 2
        y = boardY + padding / 2
        w = boardWidth - padding
        h = boardHeight - padding
        IBcolor = self.colorTheme['innerBorder']

        Sudoku.drawGrid(app, x, y, w, h, self.gridSize, self.gridSize, 
                        borderCol=IBcolor, borderWidth=padding / 2)

        # Draw the tiles
        for row in range(self.gridSize ** 2):
            for col in range(self.gridSize ** 2):

                Sudoku.drawTile(self, app, row, col, self.board[row][col], 
                                borderWidth=padding / 8)

        # Draw the final frame
        frameCol = self.colorTheme['outerBorder']
        drawRect(boardX, boardY, boardWidth, boardHeight, fill=None, 
                 borderWidth=padding, border=frameCol)

    def drawTileSelector(self, app):
        
        # Find the current row and col and draw a background at that tile
        row, col = self.selectedTile

        fill = self.colorTheme['tileSelector']
        Sudoku.drawTile(self, app, row, col, self.board[row][col], tileFill=fill)

    def updateDisplayArgs(self, displayArgs):
        self.displayArgs = displayArgs