# Typing-Speed-Test-App

A simple Python typing speed test application built with Tkinter. Users can test their typing speed, see their highscore, and view a history of recent scores.

Features

Generates random words for typing practice.

Start and finish tests using buttons or the Enter key.

Displays typing speed in WPM (words per minute).

Tracks highscore and last 5 scores.

Marks completed words in green as you type.

Saves scores in a JSON file (score.json) for persistence.

Requirements

Python 3.7+

Tkinter (usually included with Python)

dictionary.py file containing a list of words: TEST_DICT = [...]

Installation

Clone or download this repository.

Ensure dictionary.py exists with a TEST_DICT list.

Install any dependencies if needed (mostly standard library).

python typing_speed.py

Usage

Click New Words to generate a new set of words.

Press Enter or the Start button to begin typing.

Type the words in the input box; correctly typed words turn green.

Press Enter or the Finish button to stop the test.

The typing speed will display, and scores will update automatically.

File Structure
typing_speed.py     # Main application script
dictionary.py       # List of words for typing tests
score.json          # Stores highscore and recent scores
README.md           # Project documentation

Notes

The JSON file score.json stores scores persistently.

Maximum of 5 recent scores are saved.

Highscore updates automatically if a new WPM exceeds the previous.