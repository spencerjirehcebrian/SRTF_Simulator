import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import pandas as pd

from random import *

import copy

import time

processArrayGlobal = [[1, 0, 2, 2, 0, 0], [2, 1, 8, 8, 0, 0], [3, 2, 3, 3, 0, 0], [4, 3, 1, 1, 0, 0], [5, 4, 5, 5, 0, 0]]

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(
        self,
        section,
        orientation,
        role,
    ):

        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.processArray = copy.deepcopy(processArrayGlobal)
        self.algo_active = False

        self.setWindowTitle("Cebrian's 5 Job SRTF Simulator for Assignment2.2")

        self.sceneReady = QGraphicsScene(0, 0, 100, 100)

        self.sceneGannt = QGraphicsScene(0, 0, 100, 100)

        self.penG = QPen(Qt.GlobalColor.black)
        self.penG.setWidth(1)

        #### Fonts
        outFont = QFont("Sans Serif", 9, 6)
        outFont.setBold(1)

        titleFont = QFont("Helvetica [Cronyx]",  12)
        titleFont.setBold(1)

        titleFontMain = QFont("Helvetica [Cronyx]",  16)
        titleFontMain.setBold(1)

        #
        self.buttonReset = QPushButton("Reset")
        self.buttonReset.clicked.connect(self.reset_clicked)
        self.buttonStart = QPushButton("Start Simulation")
        self.buttonStart.clicked.connect(self.start_STRF_algo_clicked)
        self.buttonNew = QPushButton("New Randomized Data")
        self.buttonNew.clicked.connect(self.new_data_clicked)
        self.buttonFinish = QPushButton("Finish")
        self.buttonFinish.clicked.connect(self.finish_clicked)
        self.buttonPause = QPushButton("Pause")
        self.buttonPause.clicked.connect(self.pause_clicked)
        self.buttonPlay = QPushButton("Play/Resume")
        self.buttonPlay.clicked.connect(self.play_clicked)
        self.buttonAssign = QPushButton("Use Cebrian_Assignment_2.1 Data")
        self.buttonAssign.clicked.connect(self.cebrian_assign2_1_clicked)

        self.buttonStart.setEnabled(True)
        self.buttonPlay.setEnabled(False)
        self.buttonPause.setEnabled(False)
        self.buttonFinish.setEnabled(False)
        self.buttonReset.setEnabled(False)
        self.buttonNew.setEnabled(True)

        self.labelHeader = QLabel("5 Job Shortest-Remaining-Time-First Scheduling Algorithm")
        self.labelHeader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelHeader.setFont(titleFontMain)
        self.labelControls = QLabel("Simulation Controls")
        self.labelControls.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelControls.setFont(titleFont)
        self.labelReadyQueue = QLabel("Ready Queue")
        self.labelReadyQueue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelReadyQueue.setFont(titleFont)
        self.labelGanttChart = QLabel("Gantt Chart")
        self.labelGanttChart.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelGanttChart.setFont(titleFont)
        self.labelJob = QLabel("Job Pool")
        self.labelJob.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelJob.setFont(titleFont)


        self.labelSpeed = QLabel("Simulation Speed:")
        self.labelSpeed.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.labelCPU = QLabel("CPU")
        self.labelCPU.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelCPU.setFont(titleFont)
        self.labelCurrentJob = QLabel("Current Job")
        self.labelCurrentJob.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelCurrentTime = QLabel("Current Time")
        self.labelCurrentTime.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.labelCPUOut = QLabel("CPU")
        self.labelCPUOut.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelCurrentJobOut = QLabel("--")
        self.labelCurrentJobOut.setFont(outFont)
        self.labelCurrentJobOut.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelCurrentTimeOut = QLabel("--")
        self.labelCurrentTimeOut.setFont(outFont)
        self.labelCurrentTimeOut.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.labelAverageWaitingTime = QLabel("Average Waiting Time")
        self.labelAverageWaitingTime.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelAverageWaitingTimeOut = QLabel("--")
        self.labelAverageWaitingTimeOut.setFont(outFont)
        self.labelAverageWaitingTimeOut.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.labelAverageTurnaroundTime = QLabel("Average Turnaround Time")
        self.labelAverageTurnaroundTime.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelAverageTurnaroundTimeOut = QLabel("--")
        self.labelAverageTurnaroundTimeOut.setFont(outFont)
        self.labelAverageTurnaroundTimeOut.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.combo_box = QComboBox(self)
        geek_list = ["2", "1.5", "1", "0.7", "0.5", "0.3", "0.1"]
        self.combo_box.addItems(geek_list)
        item = "0.5"
        self.combo_box.setCurrentText(item)


        #table
        self.table = QtWidgets.QTableView()

        data = pd.DataFrame(
            self.processArray,
            columns=["Process", "Arrival Time", "Burst Time", "Remaining Burst Time", "Waiting Time", "Turnaround Time"],
            index=["Job", "Job", "Job", "Job", "Job"],
        )

        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.table.setColumnWidth(0,150)
        self.table.setColumnWidth(1,150)
        self.table.setColumnWidth(2,150)
        self.table.setColumnWidth(3,150)
        self.table.setColumnWidth(4,150)
        self.table.setColumnWidth(5,150)

        # Place elements into layout

        self.viewReady = QGraphicsView(self.sceneReady)
        self.viewReady.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.viewGannt = QGraphicsView(self.sceneGannt)
        self.viewGannt.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.setFixedSize(QSize(1300, 700))
        layout = QGridLayout()
        layout.addWidget(self.labelHeader, 0, 0, 1, 6)
        layout.addWidget(self.labelCPU, 1,0,1,2)

        layout.addWidget(self.labelCurrentJob, 2, 0, 1, 1)
        layout.addWidget(self.labelCurrentJobOut, 3,0, 1, 1)

        layout.addWidget(self.labelCurrentTime, 2, 1, 1, 1)
        layout.addWidget(self.labelCurrentTimeOut, 3, 1, 1, 1)

        layout.addWidget(self.labelAverageWaitingTime, 4, 0, 1, 1)
        layout.addWidget(self.labelAverageWaitingTimeOut, 5,0, 1, 1)

        layout.addWidget(self.labelAverageTurnaroundTime, 4, 1, 1, 1)
        layout.addWidget(self.labelAverageTurnaroundTimeOut, 5, 1, 1, 1)

        layout.addWidget(self.labelReadyQueue, 1, 3, 1, 1)
        layout.addWidget(self.viewReady, 2, 3, 6, 3)
        layout.addWidget(self.labelGanttChart, 7, 0, 1, 1)
        layout.addWidget(self.viewGannt, 8, 0, 1, 6)
        layout.addWidget(self.labelJob, 9, 0, 1, 1)
        layout.addWidget(self.table, 10, 0, 1, 6)

        layout.addWidget(self.labelControls, 11,3,1,3)
        layout.addWidget(self.buttonReset, 12, 4, 1, 1)
        layout.addWidget(self.buttonStart, 12, 3, 1, 1)
        layout.addWidget(self.buttonNew, 12, 5, 1, 1)

        layout.addWidget(self.combo_box, 14, 5, 1, 1)
        layout.addWidget(self.labelSpeed, 14, 4, 1, 1)
        layout.addWidget(self.buttonAssign, 14, 3, 1, 1)

        layout.addWidget(self.buttonFinish, 13, 3, 1, 1)
        layout.addWidget(self.buttonPause, 13, 5, 1, 1)
        layout.addWidget(self.buttonPlay, 13, 4, 1, 1)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def new_data_clicked(self):
        try:
            self.buttonStart.setEnabled(True)
            self.sceneReady.clear()
            self.sceneGannt.clear()
            QApplication.processEvents()
            newArray = []
            num2Guard = [11]
            ctr1 = 1
            while ctr1 <= len(self.processArray):
                num2 = randrange(10)
                num3 = randrange(0, 9)
                newArrayGen = [ctr1, num2, num3, num3, 0, 0]

                if num2 in num2Guard:
                    print("Chirp")
                else:
                    newArray.append(newArrayGen)
                    ctr1 += 1
                    num2Guard.append(num2)

            global processArrayGlobal
            self.processArray = copy.deepcopy(newArray)
            processArrayGlobal = copy.deepcopy(newArray)
            print(self.processArray)
            data = pd.DataFrame(
                self.processArray,
                columns=["Process", "Arrival Time", "Burst Time", "Remaining Burst Time", "Waiting Time", "Turnaround Time"],
                index=["Job", "Job", "Job", "Job", "Job"],
            )
            self.model = TableModel(data)
            self.table.setModel(self.model)
            self.table.update()
        except Exception as e:

            print(e)

    def reset_clicked(self):

        self.sceneReady.clear()
        self.sceneGannt.clear()
        self.buttonStart.setEnabled(True)
        self.buttonFinish.setEnabled(False)
        self.buttonReset.setEnabled(True)
        self.buttonNew.setEnabled(True)

        self.labelCurrentJobOut.setText("Idle")
        self.labelCurrentTimeOut.setText("0")
        self.labelAverageTurnaroundTimeOut.setText("--")
        self.labelAverageWaitingTimeOut.setText("--")

        self.processArray = copy.deepcopy(processArrayGlobal)
        data = pd.DataFrame(
            self.processArray,
            columns=["Process", "Arrival Time", "Burst Time", "Remaining Burst Time", "Waiting Time", "Turnaround Time"],
            index=["Job", "Job", "Job", "Job", "Job"],
        )
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.table.update()

    def start_STRF_algo_clicked(self):
        try:
            self.itemTime = float(self.combo_box.currentText())
            self.sceneReady.clear()
            self.sceneGannt.clear()
            self.algo_active = True
            QApplication.processEvents()

            timeInstance = 0
            waitingQueue = []
            completedProcessCtr = 0

            executedTime = 0
            processToExecIndex = 0

            xPos = -580
            xPosText = -579

            while completedProcessCtr < len(self.processArray):
                if (self.algo_active == True):
                    self.buttonStart.setEnabled(False)
                    self.buttonPlay.setEnabled(False)
                    self.buttonPause.setEnabled(True)
                    self.buttonFinish.setEnabled(True)
                    self.buttonReset.setEnabled(False)
                    self.buttonNew.setEnabled(False)
                    self.combo_box.setEnabled(False)
                    self.buttonAssign.setEnabled(False)
                    xPosRed = -260
                    xPosTextRed = -259
                    for job in self.processArray:
                        burstTime = job[3]
                        processNum = job[0]
                        if job[1] == timeInstance:
                            processArrivedArray = [processNum, burstTime]
                            waitingQueue.append(processArrivedArray)
                            #print(waitingQueue)
                        if waitingQueue:
                            for process in waitingQueue:
                                if burstTime != 0 and processNum == process[0]:
                                    self.processArray[processNum - 1][5] += 1

                    completedProcessCtr = 0
                    minExecTime = 999999999
                    processIndexCtr = 0
                    processToExec = 0
                    for process in waitingQueue:
                        if process[1] == 0:
                            completedProcessCtr += 1
                        elif process[1] < minExecTime:
                            minExecTime = process[1]
                            processToExec = process[0]
                            processToExecIndex = processIndexCtr
                            executedTime = minExecTime - 1

                        processIndexCtr += 1

                    if waitingQueue:
                        waitingQueue[processToExecIndex][1] = executedTime
                        self.processArray[processToExec - 1][3] = executedTime


                    timeInstance += 1
                    executedTime = 0

                    data = pd.DataFrame(
                        self.processArray,
                        columns=["Process", "Arrival Time", "Burst Time", "Remaining Burst Time", "Waiting Time", "Turnaround Time"],
                        index=["Job", "Job", "Job", "Job", "Job"],
                    )
                    self.model = TableModel(data)
                    self.table.setModel(self.model)
                    self.table.update()

                    self.sceneReady.clear()
                    sort_waitingQueue = sorted(waitingQueue, key=lambda x: x[1])
                    for waited in sort_waitingQueue:
                        searchIndex = waited[0]
                        if (
                            self.processArray[searchIndex - 1][3] != 0
                            and processToExec != searchIndex
                        ):
                            if searchIndex == 0:
                                self.brushG = QBrush(Qt.GlobalColor.red)
                            elif searchIndex == 1:
                                self.brushG = QBrush(Qt.GlobalColor.green)
                            elif searchIndex == 2:
                                self.brushG = QBrush(Qt.GlobalColor.blue)
                            elif searchIndex == 3:
                                self.brushG = QBrush(Qt.GlobalColor.cyan)
                            elif searchIndex == 4:
                                self.brushG = QBrush(Qt.GlobalColor.magenta)
                            elif searchIndex == 5:
                                self.brushG = QBrush(Qt.GlobalColor.yellow)
                            else:
                                self.brushG = QBrush(Qt.GlobalColor.white)

                            self.sceneReady.addRect(
                                xPosRed,
                                5,
                                20,
                                90,
                                self.penG,
                                self.brushG,
                            )
                            fontMod = QFont("Helvetica [Cronyx]",  12)
                            textitem = self.sceneReady.addText(str(searchIndex), fontMod)
                            self.processArray[searchIndex - 1][4] +=1
                            textitem.setPos(xPosTextRed, 35)
                            self.sceneReady.addItem(textitem)
                            QApplication.processEvents()
                            xPosRed += 25
                            xPosTextRed += 25

                    if processToExec == 0:
                        self.brushG = QBrush(Qt.GlobalColor.red)
                    elif processToExec == 1:
                        self.brushG = QBrush(Qt.GlobalColor.green)
                    elif processToExec == 2:
                        self.brushG = QBrush(Qt.GlobalColor.blue)
                    elif processToExec == 3:
                        self.brushG = QBrush(Qt.GlobalColor.cyan)
                    elif processToExec == 4:
                        self.brushG = QBrush(Qt.GlobalColor.magenta)
                    elif processToExec == 5:
                        self.brushG = QBrush(Qt.GlobalColor.yellow)
                    else:
                        self.brushG = QBrush(Qt.GlobalColor.white)

                    if completedProcessCtr < len(self.processArray) and processToExec > 0:
                        self.sceneGannt.addRect(
                            xPos,
                            -30,
                            20,
                            160,
                            self.penG,
                            self.brushG,
                        )

                        self.labelCurrentJobOut.setText("Job " + str(processToExec))
                        self.labelCurrentTimeOut.setText(str(timeInstance))

                        fontMod = QFont("Helvetica [Cronyx]",  12)
                        textitem = self.sceneGannt.addText(str(processToExec), fontMod)
                        textitem.setPos(xPosText, 35)
                        self.sceneGannt.addItem(textitem)

                        QApplication.processEvents()
                        xPos += 25
                        xPosText += 25
                    else:
                        self.labelCurrentJobOut.setText("Idle")
                        self.labelCurrentTimeOut.setText(str(timeInstance))

                QApplication.processEvents()
                time.sleep(self.itemTime)
                QApplication.processEvents()

                sumWaitTime = 0
                sumTurnTime = 0
                for job in self.processArray:
                    waitTime = job[4]
                    sumWaitTime += waitTime
                    averageWaitTime = str(sumWaitTime/5) + " sec"
                    self.labelAverageWaitingTimeOut.setText(averageWaitTime)

                    turnTime = job[5]
                    sumTurnTime += turnTime
                    averageTurnTime = str(sumTurnTime/5) + " sec"
                    self.labelAverageTurnaroundTimeOut.setText(averageTurnTime)

                #print (timeInstance, completedProcessCtr, processToExec, self.processArray[processToExec - 1][3])

            self.buttonStart.setEnabled(False)
            self.buttonReset.setEnabled(True)
            self.buttonPlay.setEnabled(False)
            self.buttonFinish.setEnabled(False)
            self.buttonPause.setEnabled(False)
            self.combo_box.setEnabled(True)
            self.buttonAssign.setEnabled(True)
            self.buttonNew.setEnabled(True)
            self.itemTime = float(self.combo_box.currentText())

            self.labelCurrentJobOut.setText("Idle")
            self.labelCurrentTimeOut.setText(str(timeInstance - 1))
        except Exception as e:
            print(e)

    def finish_clicked(self):
        #print("finish")
        self.itemTime = 0
        self.algo_active = True

    def pause_clicked(self):
        #print("pause")
        self.algo_active = False
        self.buttonPlay.setEnabled(True)
        self.buttonPause.setEnabled(False)

    def play_clicked(self):
        #print("play")
        self.algo_active = True
        self.buttonPlay.setEnabled(False)
        self.buttonPause.setEnabled(True)

    def next_clicked(self):
        print("next")

    def cebrian_assign2_1_clicked(self):
        try:
            self.buttonStart.setEnabled(True)
            self.sceneReady.clear()
            self.sceneGannt.clear()
            QApplication.processEvents()
            newArray = [[1, 0, 2, 2, 0, 0], [2, 1, 8, 8, 0, 0], [3, 2, 3, 3, 0, 0], [4, 3, 1, 1, 0, 0], [5, 4, 5, 5, 0, 0]]

            global processArrayGlobal
            self.processArray = copy.deepcopy(newArray)
            processArrayGlobal = copy.deepcopy(newArray)
            print(self.processArray)
            data = pd.DataFrame(
                self.processArray,
                columns=["Process", "Arrival Time", "Burst Time", "Remaining Burst Time", "Waiting Time", "Turnaround Time"],
                index=["Job", "Job", "Job", "Job", "Job"],
            )
            self.model = TableModel(data)
            self.table.setModel(self.model)
            self.table.update()
        except Exception as e:

            print(e)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
