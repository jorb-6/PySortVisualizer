from drawtools import *
import sorting
import time

# setup
screen, clock = setup(Fullscreen)
running = True

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

# sort configuration
listLength = 512
barScale = 2
stepsPerFrame = 100
fps = 60
textAntiAlias = False

# sort setup
numbers = sorting.randomList(listLength)
sort = sorting.bubble(numbers)
sortStarted = False

areaSize = listLength*barScale

# visual elements
bars = [rect((0, barScale*i), (barScale, barScale), RGBA('White')) for i in range(listLength)]
startButton = button((round(areaSize/2)-63, round(areaSize/2)-23), (126, 45), start, RGBA('Purple'))
startButtonText = text((round(areaSize/2)-46, round(areaSize/2)-23), RGBA('White'), 'Start', font('Arial', 40, bold=True))
whenSortedText = text((round(areaSize/2)-63 ,round(areaSize/2)-23), RGBA('Really Green'), 'Sorted', font('Arial', 40, bold=True))
barsBackground = rect((0,0), (areaSize, areaSize), RGBA("#3F003C"))
sideTextHeader = text((areaSize+2, 5), RGBA('White'), 'Extra sort information:', font('Arial', 24))
sideText = [text((areaSize+2, 30+i*18), RGBA('White'), t, font('Arial', 16)) for i,t in enumerate([
    f'Sort type: {sort.type}',
    f'Numbers to sort: {listLength}',
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

# main loop
while running:
    handleEvents()
    
    screen.fill("#1F001D")

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
    if not sorting.isSorted(sort.list):
        currentTime = time.time()
    clock.tick(fps)

quit()
