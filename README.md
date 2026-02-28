# PySortVisualizer

## Description
PySortVisualizer is a simple tool made in Python to visualize sorting algorithms.
The visualizer shows various extra information about the state of the algorithm,
like the visual time, sort time, and operation count. There is also support for
adding custom algorithms (see [Adding Algorihtms](#adding-algorithms)).

## Requirements
- Python 3.10 or newer  
  (Developed and tested with Python 3.13)

## How to Use

### Initial Setup
1. Create a Python virtual environment (venv): `python -m venv .venv`
2. Activate the venv:<br>
   - <b> macOS / Linux</b>: `source .venv/bin/activate`
   - <b>Windows (Command Prompt)</b>: `.\.venv\Scripts\activate.bat`
   - <b>Windows (PowerShell)</b>: `.\.venv\Scripts\Activate.ps1`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the program: `python main.py`

### Program Controls:
Press Q to exit.<br>
Press the Start button to start the sorting.<br>
More controls will be added later.

### Adding Algorithms:
To add an algorithm, add a python file to the algorithms folder.<br>
For examples of how to make an algorithm, look at the premade files.

### Changing the Color Theme:
To change the color theme, modify theme.cfg.<br>
<b><i>The format of theme.cfg is as follows:</b></i><br>
`elementName,r.g.b;`<br>
Where `elementName` is the element to change (ex. background, bars, text), `r`
is the ammount of red (0-255), `g` is green (0-255), and `b` is blue (0-255).

## Currenly Supported Algorithms:
### Exchange Sorts:
1. Exchange
2. Gnome
3. Bubble
4. Cocktail Shaker
5. Odd-Even
6. Comb
### Other/Unclassified Sorts:
1. Insertion
2. Shell
3. Selection
### Bogo sorts
1. Bogo
2. Optimized bogo

## Planned Features (in order):
1. More algorithms
  - Bitonic
  - Merge
  - Quicksort
  - Radix
  - Max Heap
2. Extra visual improvements
