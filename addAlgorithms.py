import os
import termcolor as tc
import colorama as cr

algorithmFiles = os.listdir('algorithms/')

algorithms = []
for name in algorithmFiles:
    tc.cprint('Reading algorithms/'+name, 'yellow')
    f = open(f'algorithms/{name}')
    algorithms.append(f.read())
    f.close()

for i,v in enumerate(algorithms):
    tc.cprint('Parsing algorithms/'+algorithmFiles[i], 'magenta')
    algorithms[i] = v.split('class ')
    for ii, vv in enumerate(algorithms[i]):
        if not algorithms[i][ii][:6] == 'import':
            algorithms[i][ii] = 'class '+vv

for i,v in enumerate(algorithms):
    tc.cprint('Loading classes from algorithms/'+algorithmFiles[i], 'green')
    for ii,vv in enumerate(v):
        if vv[:5] == 'class':
            tc.cprint(' - '+vv.split(':')[0][6:], 'blue')
        exec(vv)

tc.cprint('Warning: Using custom algorithms involves calling exec() to load the' \
' algorithms! This means that any python code can be executed. Only use algorithms' \
' that you know to be safe!', 'red', 'on_yellow', ['bold'])
