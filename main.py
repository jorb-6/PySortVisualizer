from drawtools import *
#import pygetwindow
import termcolor as tc
import colorama as cr
import addAlgorithms as sorts
import time
import random

# sort configuration
listLength = 256
barScale = 2
stepsPerFrame = 25
fps = 60
sortType = 'bubble'
textAntiAlias = False

# manage config inputs
print(tc.colored('Input settings for the visualizer. Leave blank for default (in square brackets)', attrs=['bold', 'underline']))
prompts = [
    'List length [256]: ',
    'Bar scale (width & height, in pixels) [2]: ',
    'Steps per frame [25]: ',
    'Frames per second [60]: ',
    'Sorting algorithm (all lowercase, must be valid) [bubble]: ',
    'Antialias text (bool True or False, capitals matter) [False]: '
]
vars = ['listLength', 'barScale', 'stepsPerFrame', 'fps', 'sortType', 'textAntiAlias']
ints = [0,1,2,3]
bools = [5]
for i in range(len(prompts)):
    value = input(prompts[i])
    if not value == '':
        if i in ints:
            value = int(value)
        if i in bools:
            value = bool(value)
        globals()[vars[i]] = value

# setup
screen, clock = setup(Fullscreen)
running = True
cr.just_fix_windows_console()

# add events
addEvent("QUIT", lambda: globals().__setitem__("running", False))
addKeyEvent("q", lambda: globals().__setitem__("running", False))

startTime = 0
currentTime = 0
def start():
    global sortStarted, startTime, currentTime
    sortStarted = True
    startTime = time.time()
    currentTime = startTime

def randomList(size):
    list = []
    for i in range(size):
        list.append(i+1)
    random.shuffle(list)
    return list

# sort setup
numbers = randomList(listLength)
sort = getattr(sorts, sortType)(numbers)
sortStarted = False

areaSize = listLength*barScale

# theme setup
themeFile = open('theme.cfg')
themeRaw = themeFile.read()
themeFile.close()

theme = themeRaw.replace('\n', '').split(';')
for i,v in enumerate(theme):
    theme[i] = v.split(',') # type: ignore

colors = {}
for v in theme:
    if not v[0] == '':
        colors[v[0]] = [int(vv) for vv in v[1].split('.')]

# visual elements
pygame.display.set_caption('PySortVisualizer')
bars = [rect((0, barScale*i), (barScale, barScale), RGBA(colors['bars'])) for i in range(listLength)]
startButton = button((round(areaSize/2)-63, round(areaSize/2)-23), (126, 45), start, RGBA(colors['button']))
startButtonText = text((round(areaSize/2)-46, round(areaSize/2)-23), RGBA(colors['buttonText']), 'Start', font('Arial', 40, bold=True))
whenSortedText = text((round(areaSize/2)-63 ,round(areaSize/2)-23), RGBA(colors['whenSortedText']), 'Sorted', font('Arial', 40, bold=True))
barsBackground = rect((0,0), (areaSize, areaSize), RGBA(colors['areaBackground']))
sideTextHeader = text((areaSize+2, 5), RGBA(colors['sideHeaderText']), 'Extra sort information:', font('Arial', 24))
sideText = [text((areaSize+2, 30+i*18), RGBA(colors['text']), t, font('Arial', 16)) for i,t in enumerate([
    f'Sort type: {sort.type}',
    f'Numbers to sort: {len(sort.list)}',
    f'Sorting steps per frame: {stepsPerFrame}',
    f'Frames per second: {fps}',
    '',
    'Visual time: 0s',
    'Sort time: 0ms',
    '',
    'Total operations: 0',
    'Swaps: 0',
    'Comparisons: 0',
    '',
    'Press Q to quit.'
])]

#try:
#    windows = pygetwindow.getWindowsWithTitle('PySortVisualizer')
#    if windows:
#        target = windows[0]
#        target.activate()
#    else:
#        print('Visualizer window not found..?')
#except Exception as e:
#    print(f'Error occurred while focusing visualizer window: {e}')

# main loop
while running:
    handleEvents()
    
    screen.fill(colors['background'])

    # display sorted text and step sort
    if not sort.finished and sortStarted:
        sort.step(stepsPerFrame)
    
    # update side text info
    sideText[5].text = f'Visual time: {round((currentTime - startTime)*100)/100}s'
    sideText[6].text = f'Sort time: {round(sort.time/10000)/100}ms'
    sideText[8].text = f'Total operations: {sort.swaps + sort.comparisons}'
    sideText[9].text = f'Swaps: {sort.swaps}'
    sideText[10].text = f'Comparisons: {sort.comparisons}'

    # change bar sizes and colors
    for i,v in enumerate(sort.list):
        bars[i].size = (barScale*v, barScale)
        if sort.pointer == i:
            bars[i].color = RGBA('Really Red')
        else:
            bars[i].color = RGBA('White')
        
        try:
            if sort.pointer1 == i: # type: ignore
                bars[i].color = RGBA('Orange')
        except AttributeError:
            pass
        
        try:
            if sort.pointer2 == i: # type: ignore
                bars[i].color = RGBA('Yellow')
        except AttributeError:
            pass
    
    # draw bars and background
    barsBackground.draw(screen)
    for bar in bars:
        bar.draw(screen)
    
    if sort.finished:
        whenSortedText.draw(screen, textAntiAlias)
    
    sideTextHeader.draw(screen, textAntiAlias)
    for text in sideText:
        text.draw(screen, textAntiAlias)

    if not sortStarted:
        startButton.draw(screen)
        startButton.update()
        startButtonText.draw(screen, textAntiAlias)

    blit()

    # time keeping
    if not sort.finished:
        currentTime = time.time()
    clock.tick(fps)

quit()
cr.deinit()
