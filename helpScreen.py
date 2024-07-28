from cmu_graphics import *

def helpScreen_onAppStart(app):
    print('helpScreen')

def helpScree_onActiveScreen(app):
    print('yo')

def helpScreen_redrawAll(app):
    drawRect(200, 200, 100, 100, fill='red')