from cmu_graphics import *

class Button():

    def __init__(self, text, x, y, w, h, borderWidth, colors):
        self.text = text
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.borderWidth = borderWidth
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
        
        fontSize = min(self.width, self.height) / 2
        
        drawLabel(self.text, cx, cy, fill=textColor, size=fontSize, font=self.font, bold=True)

    def mouseInButton(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width and 
                self.y <= mouseY <= self.y + self.height)


    def checkIsPressed(self, mouseX, mouseY):
        if Button.mouseInButton(self, mouseX, mouseY):
            self.isPressed = not self.isPressed
        

    def release(self, mouseX, mouseY):
        if self.isPressed:
            self.isPressed = False

            if Button.mouseInButton(self, mouseX, mouseY):
                return True
            
            return False
        
    def updateDisplayArgs(self, x, y, w, h, borderWidth):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.borderWidth = borderWidth

class Toggle(Button):
    
    def __init__(self, text, x, y, w, h, colors):
        super().__init__(text, x, y, w, h, colors)

    def release(self, mouseX, mouseY):
        # This is the simplest way i can think to overide the 
        # inherited release function
        pass

    