import logging
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QToolBar, QInputDialog, QMessageBox
from random import SystemRandom, randint 
import sys

# Written in camel case in accordance with PyQt (C++) formatting

#Logs errors in format "[timestamp]: [roll result]"
logger = logging.getLogger(__name__)  
logging.basicConfig(filename='roll_history.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

def getRandomNum(low: int, high: int) -> int:
    """Generates a true random number using system

    Args:
        low (int): Lower bound (inclusive)
        high (int): Upper bound (inclusive)

    Returns:
        int: The random number
    """
    return SystemRandom().randint(low, high)

app = QApplication(sys.argv)

class Die(QAction):
    """Represents an n-sided die with random rolling functionality

    Methods:
        roll: Generates dice roll result and displays it on screen.
    """
    def __init__(self, parent, no_sides: int = 6) -> None:
        """_summary_

        Args:
            parent (MainWindow): Window to add dice to.
            no_sides (int, optional): Number of sides of die (upper bound of random gen). Defaults to 6.
        """
        super().__init__(parent)

        self.parent = parent
        self.low = 1
        self.high = no_sides
        self.result = None
        self.setStatusTip(f'Roll a {no_sides} sided die')
        self.setText(str(no_sides))
        self.setFont(QFont('Arial', 30))
        self.triggered.connect(self.roll)

    def roll(self) -> None:
        """Generates dice roll result (random number from 1 to number of sides) and displays it on screen."""
        rollResult = getRandomNum(self.low, self.high)
        self.result = rollResult
        self.parent.result.setText(str(rollResult))
        logger.info('%i sided die result: %i', self.high, self.result)

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        """Extends QMainWindow constructor to layout the main window"""
        super().__init__()

        self.setFixedSize(QSize(1000, 600))
        self.setWindowTitle("Hasbro Dice Roller")
            
        self.result = QLabel()
        self.result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result.setFont(QFont('Arial', 40))

        self.diceOptions = QToolBar('Dice')
        self.diceOptions.setIconSize(QSize(32,32))
        self.addToolBar(self.diceOptions)

        addDieBtn = QAction('+', self)
        addDieBtn.triggered.connect(self.addDie)
        addDieBtn.setFont(QFont('Arial', 30))

        self.diceOptions.addAction(addDieBtn)
        self.diceOptions.addAction(Die(self, no_sides=4))
        self.diceOptions.addAction(Die(self))
        self.diceOptions.addAction(Die(self, no_sides=10))

        self.setCentralWidget(self.result)
    def addDie(self):
        """Adds user-inputted die to the main window"""
        def input(self):
            errMsg = QMessageBox()
            errMsg.setText('Invalid input. Please enter an integer.')
            errMsg.accepted.connect(lambda: input(self))
            try: 
                sidesInp, isDone = QInputDialog.getText(self, 'Number of sides', 'Enter die number of sides: ')
                sides = int(sidesInp)
                if sides > 1 and sides < 1000:
                    if isDone:
                        self.diceOptions.addAction(Die(self, no_sides=sides))
                else:
                    raise ValueError
            except ValueError:
                errMsg.exec()
        input(self)

w = MainWindow()

w.show()

app.exec()