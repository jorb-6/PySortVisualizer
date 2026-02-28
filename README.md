# PySortVisualizer

## Description
PySortVisualizer is a simple tool made in Python to visualize sorting algorithms. The visualizer shows various extra information about the state of the algorithm, like the visual time, sort time, and operation count.

## Requirements
- Python 3.10 or newer  
  (Developed and tested with Python 3.13)

## How to Use

### Initial setup
1. Create a Python virtual environment (venv): `python -m venv .venv`
2. Activate the venv:<br>
   - <b> macOS / Linux</b>: `source .venv/bin/activate`
   - <b>Windows (Command Prompt)</b>: `.\.venv\Scripts\activate.bat`
   - <b>Windows (PowerShell)</b>: `.\.venv\Scripts\Activate.ps1`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the program: `python main.py`

## Program controls:
Press Q to exit.<br>
Press the Start button to start the sorting.<br>
More controls will be added later.

## Currenly supported algorithms:
### Exchange sorts:
1. Exchange
2. Gnome
3. Bubble
4. Cocktail Shaker
5. Comb
### Other/Unclassified sorts:
1. Insertion
2. Shell
3. Selection
### Bogo sorts
1. Bogo

## Planned features (in order):
1. More algorithms
  - Bitonic
  - Merge
  - Quicksort
  - Radix
  - Max Heap  
  - Optimized bogo
2. Extra visual improvements
