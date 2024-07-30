from cmu_graphics import *

class Button():

    def __init__(self, text, x, y, w, h, colors):
        self.text = text
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.borderWidth = (w + h) / 40
        self.isPressed = False
        self.colors = colors

        self.font = 'monospace'

    def drawButton(self):
        borderColor = self.colors['borderColor']
        textColor = self.colors['textColor']

        if self.isPressed:
            fill = self.colors['pressedFill']
        else:
            fill = self.colors['fill']

        cx = self.x + self.width / 2
        cy = self.y + self.height / 2

        drawRect(self.x, self.y, self.width, self.height, fill=fill, 
                 border=borderColor, borderWidth=self.borderWidth)
        
        if len(str(self.text)) > 1:
            fontSize = min(self.width, self.height) * 2.5 / len(str(self.text))
        else:
            fontSize = min(self.width, self.height) / 1.5
        
        drawLabel(self.text, cx, cy, fill=textColor, size=fontSize, font=self.font, bold=True)

    def mouseInButton(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width and 
                self.y <= mouseY <= self.y + self.height)


    def checkIsPressed(self, mouseX, mouseY):
        if Button.mouseInButton(self, mouseX, mouseY):
            self.isPressed = not self.isPressed
        

    def release(self, mouseX, mouseY):
        if self.isPressed:
            self.isPressed = not self.isPressed

            if Button.mouseInButton(self, mouseX, mouseY):
                return True
            
            return False
        
    def updateDisplayArgs(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.borderWidth = (w + h) / 40

class Toggle(Button):
    
    def __init__(self, text, x, y, w, h, colors):
        super().__init__(text, x, y, w, h, colors)

    def release(self, mouseX, mouseY):

        if Button.mouseInButton(self, mouseX, mouseY):
            return True
        
        return False

    