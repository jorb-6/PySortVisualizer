from drawtools import *
#import pygetwindow
import termcolor as tc
import colorama as cr
import addAlgorithms as sorts
import time
import random

# sort configuration
useCached = 0
listLength = 256
barScale = 2
stepsPerFrame = 25
fps = 60
sortType = 'bubble'
textAntiAlias = False

# manage config inputs
print(tc.colored('Input settings for the visualizer. Leave blank for default (in square brackets)', attrs=['bold', 'underline']))
prompts = [
    'Use cached config? (0: no, 1: yes) [0]: ',
    'List length [256]: ',
    'Bar scale (width & height, in pixels) [2]: ',
    'Steps per frame [25]: ',
    'Frames per second [60]: ',
    'Sorting algorithm (must be valid) [bubble]: ',
    'Antialias text (bool True or False, capitals matter) [False]: '
]
vars = ['useCached','listLength', 'barScale', 'stepsPerFrame', 'fps', 'sortType', 'textAntiAlias']
ints = [0,1,2,3,4]
bools = [6]
cache = []
for i in range(len(prompts)):
    value = input(prompts[i])
    if not value == '':
        if i in ints:
            value = int(value)
        if i in bools:
            value = bool(value)
        globals()[vars[i]] = value
        cache.append(str(value))
    else:
        cache.append(str(globals()[vars[i]]))
    if useCached == 1:
        break
cache = ','.join(cache[1:])

if useCached == 1:
    tc.cprint('Reading cached.cfg', 'yellow')
    cachedFile = open('cached.cfg')
    cachedRaw = cachedFile.read().split('\n')[0]
    cachedFile.close()

    tc.cprint('Parsing cached.cfg', 'magenta')
    cached = cachedRaw.split(',')

    tc.cprint('Loading config from cached.cfg', 'green')
    for i,v in enumerate(vars[1:]):
        tc.cprint(f' - {v}', 'cyan')
        value = cached[i]
        if not value == '':
            if i+1 in ints:
                value = int(value)
            if i+1 in bools:
                value = bool(value)
            globals()[v] = value
else:
    cachedFile = open('cached.cfg', 'w')
    cachedFile.write(cache)

# setup
tc.cprint('Starting setup', 'yellow')
screen, clock = setup(Fullscreen)
running = True
print('colorama: Fix windows console')
cr.just_fix_windows_console()

# add events
tc.cprint('Adding events', 'green')
tc.cprint(' - QUIT', 'cyan')
addEvent("QUIT", lambda: globals().__setitem__("running", False))
tc.cprint(' - key: q', 'cyan')
addKeyEvent("q", lambda: globals().__setitem__("running", False))

startTime = 0
currentTime = 0
tc.cprint('Defining functions', 'green')
tc.cprint(' - start', 'cyan')
def start():
    global sortStarted, startTime, currentTime
    sortStarted = True
    startTime = time.time()
    currentTime = startTime

tc.cprint(' - randomList', 'cyan')
def randomList(size):
    list = []
    for i in range(size):
        list.append(i+1)
    random.shuffle(list)
    return list

# sort setup
tc.cprint('Starting sort setup', 'yellow')
tc.cprint('Generating scrambled list', 'magenta')
numbers = randomList(listLength)
tc.cprint('Loading algorithm', 'magenta')
try:
    sort = getattr(sorts, sortType)(numbers)
except AttributeError as e:
    tc.cprint(f'Invalid algorithm name! Defaulting to bubble. Error: {e}',
              'black', 'on_red', ['bold'])
    tc.cprint(f'For a list of algorithms, see the output in blue above the warning about custom algorithms.',
              'green', attrs=['italic'])
    sort = getattr(sorts, 'bubble')(numbers)
sortStarted = False

areaSize = listLength*barScale

# theme setup
tc.cprint('Starting theme setup', 'yellow')
tc.cprint('Reading theme.cfg', 'yellow')
themeFile = open('theme.cfg')
themeRaw = themeFile.read()
themeFile.close()

tc.cprint('Parsing theme.cfg', 'magenta')
theme = themeRaw.replace('\n', '').split(';')
for i,v in enumerate(theme):
    theme[i] = v.split(',') # type: ignore

tc.cprint('Loading colors from theme.cfg', 'green')
colors = {}
for v in theme:
    if not v[0] == '':
        tc.cprint(f' - {v[0]}', 'cyan')
        colors[v[0]] = [int(vv) for vv in v[1].split('.')]

# visual elements
tc.cprint('Starting GUI setup', 'yellow')
tc.cprint('Setting window name', 'magenta')
pygame.display.set_caption('PySortVisualizer')
tc.cprint('Defining visual elements', 'green')
tc.cprint(' - bars', 'blue')
bars = [rect((0, barScale*i), (barScale, barScale), RGBA(colors['bars'])) for i in range(listLength)]
tc.cprint(' - startButton', 'blue')
startButton = button((round(areaSize/2)-63, round(areaSize/2)-23), (126, 45), start, RGBA(colors['button']))
tc.cprint(' - startButtonText', 'blue')
startButtonText = text((round(areaSize/2)-46, round(areaSize/2)-23), RGBA(colors['buttonText']), 'Start', font('Arial', 40, bold=True))
tc.cprint(' - whenSortedText', 'blue')
whenSortedText = text((round(areaSize/2)-63 ,round(areaSize/2)-23), RGBA(colors['whenSortedText']), 'Sorted', font('Arial', 40, bold=True))
tc.cprint(' - barsBackground', 'blue')
barsBackground = rect((0,0), (areaSize, areaSize), RGBA(colors['areaBackground']))
tc.cprint(' - sideTextHeader', 'blue')
sideTextHeader = text((areaSize+2, 5), RGBA(colors['sideHeaderText']), 'Extra sort information:', font('Arial', 24))
tc.cprint(' - sideText', 'blue')
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

tc.cprint('Starting main loop', 'black', 'on_green', ['bold'])
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
