# Test vehicle with TCP
import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer, QTime
import math

import socket
from datetime import datetime
import struct
import json

class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Speed:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Size:
    def __init__(self, x=5, y=10):
        self.x = x
        self.y = y

class Vehicle:
    def __init__(self):
        self._position = Position()
        self._speed = Speed()
        self._size = Size()

    def setPosition(self, position):
        self._position = position

    def getPosition(self):
        return self._position

    def setSpeed(self, speed):
        self._speed = speed

    def getSpeed(self):
        return self._speed

    def setSize(self, size):
        self._size = size

    def getSize(self):
        return self._size

    def moveNext(self):
        self._position.x += self._speed.x
        self._position.y += self._speed.y
        if self._position.x > 600:
            self._position.x = 0

class Example(QWidget):
    def __init__(self, vehicles_N, vehicles_W, vehicles_E, sendData):
        super().__init__()
        self.vehicles_N = vehicles_N
        self.vehicles_W = vehicles_W
        self.vehicles_E = vehicles_E
        self.sendData = sendData
        self.my_result = 0

        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000/60)#一秒間隔で更新

        self.t = QTime()
        self.t.start()
        self.show()

    def initUI(self):
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle("Koku's Simulation")

        self.ti = 0
        self.beze_t = []
        self.r = []
        self.up_left_x = []
        self.up_left_y = []
        self.down_left_x = []
        self.down_left_y = []
        self.up_right_x = []
        self.up_right_y = []
        self.down_right_x = []
        self.down_right_y = []

        for i in range(10):
            self.beze_t.append(0)
            self.r.append(0)
            self.up_left_x.append(0)
            self.up_left_y.append(0)
            self.down_left_x.append(0)
            self.down_left_y.append(0)
            self.up_right_x.append(0)
            self.up_right_y.append(0)
            self.down_right_x.append(0)
            self.down_right_y.append(0)

        self.single_0_0 = True
        self.single_0_1 = True

        self.collision_check = []
        self.collision_check_N = []
        self.collision_check_S = []
        self.collision_check_W = []
        self.collision_check_E = []


        self.grid = {}

        for i in range(270, 330, 10):
            for j in range(270, 330, 10):
                self.grid[(i, j)] = True

    def paintEvent(self, e):
        #print("!")
        qp = QPainter(self)

        self.drawLines(qp)
        self.drawSignals_0(qp)
        self.drawVehicles(qp)

    def drawLines(self, qp):

        # print(self.t.elapsed())

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        pen_dash = QPen(Qt.black, 2, Qt.DotLine)

        # Vertical
        qp.setPen(pen)
        qp.drawLine(270, 0, 270, 600)

        # with grids ##################
        # qp.drawLine(280, 0, 280, 600)
        # qp.drawLine(290, 0, 290, 600)
        # qp.drawLine(300, 0, 300, 600)
        # qp.drawLine(310, 0, 310, 600)
        # qp.drawLine(320, 0, 320, 600)
        # with grids ##################

        qp.drawLine(330, 0, 330, 600)
        qp.drawLine(300, 0, 300, 270)
        qp.drawLine(300, 330, 300, 600)

        qp.setPen(pen_dash)
        qp.drawLine(280, 330, 280, 600)
        qp.drawLine(290, 330, 290, 600)
        qp.drawLine(310, 330, 310, 600)
        qp.drawLine(320, 330, 320, 600)

        qp.drawLine(280, 0, 280, 270)
        qp.drawLine(290, 0, 290, 270)
        qp.drawLine(310, 0, 310, 270)
        qp.drawLine(320, 0, 320, 270)

        # Tropical
        qp.setPen(pen)
        qp.drawLine(0, 270, 600, 270)

        # with grids ##################
        # qp.drawLine(0, 280, 600, 280)
        # qp.drawLine(0, 290, 600, 290)
        # qp.drawLine(0, 300, 600, 300)
        # qp.drawLine(0, 310, 600, 310)
        # qp.drawLine(0, 320, 600, 320)
        # with grids ##################

        qp.drawLine(0, 330, 600, 330)
        qp.drawLine(0, 300, 270, 300)

        qp.drawLine(330, 300, 600, 300)

        qp.setPen(pen_dash)
        qp.drawLine(0, 280, 270, 280)
        qp.drawLine(0, 290, 270, 290)
        qp.drawLine(0, 310, 270, 310)
        qp.drawLine(0, 320, 270, 320)

        qp.drawLine(330, 280, 600, 280)
        qp.drawLine(330, 290, 600, 290)
        qp.drawLine(330, 310, 600, 310)
        qp.drawLine(330, 320, 600, 320)


    def drawSignals_0(self, qp):
        #print(self.t.elapsed())

        if 1000 < self.t.elapsed() < 2000:
            qp.setPen(Qt.black)
            qp.setBrush(Qt.red)

            qp.drawEllipse(272, 262, 6, 6)
            qp.drawEllipse(282, 262, 6, 6)
            qp.drawEllipse(292, 262, 6, 6)

            qp.setBrush(Qt.green)
            qp.drawEllipse(332, 272, 6, 6)
            qp.drawEllipse(332, 282, 6, 6)
            qp.drawEllipse(332, 292, 6, 6)

            qp.setBrush(Qt.red)
            qp.drawEllipse(302, 332, 6, 6)
            qp.drawEllipse(312, 332, 6, 6)
            qp.drawEllipse(322, 332, 6, 6)

            qp.setBrush(Qt.green)
            qp.drawEllipse(262, 302, 6, 6)
            qp.drawEllipse(262, 312, 6, 6)
            qp.drawEllipse(262, 322, 6, 6)

            self.single_0_0 = False
            self.single_0_1 = True

        else:
            qp.setPen(Qt.black)
            qp.setBrush(Qt.green)

            qp.drawEllipse(272, 262, 6, 6)
            qp.drawEllipse(282, 262, 6, 6)
            qp.drawEllipse(292, 262, 6, 6)

            qp.setBrush(Qt.red)
            qp.drawEllipse(332, 272, 6, 6)
            qp.drawEllipse(332, 282, 6, 6)
            qp.drawEllipse(332, 292, 6, 6)

            qp.setBrush(Qt.green)
            qp.drawEllipse(302, 332, 6, 6)
            qp.drawEllipse(312, 332, 6, 6)
            qp.drawEllipse(322, 332, 6, 6)

            qp.setBrush(Qt.red)
            qp.drawEllipse(262, 302, 6, 6)
            qp.drawEllipse(262, 312, 6, 6)
            qp.drawEllipse(262, 322, 6, 6)

            self.single_0_0 = True
            self.single_0_1 = False

    def coordinate_up_left_x(self, po_x, r):
        return po_x - 5 * math.cos(math.radians(r))

    def coordinate_up_left_y(self, po_y):
        return po_y

    def coordinate_up_right_x(self, po_x, r):
        return po_x + 10 * math.cos(math.radians(r))

    def coordinate_up_right_y(self, po_y):
        return po_y

    def coordinate_down_left_x(self, po_x, r):
        return po_x - 5 * math.cos(math.radians(r))

    def coordinate_down_left_y(self, po_y, r):
        return po_y + 5 * math.sin(math.radians(r)) + 10 * math.cos(math.radians(r))

    def coordinate_down_right_x(self, po_x, r):
        return po_x + 10 * math.cos(math.radians(r))

    def coordinate_down_right_y(self, po_y, r):
        return po_y + 10 * math.sin(math.radians(r)) + 5 * math.cos(math.radians(r))

    def propose(self, veh_id):
        server_address = ('localhost', 6789)
        max_size = 4096

        print('Starting the client at', datetime.now())

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mes = bytes(json.dumps(self.sendData[veh_id]), encoding='utf-8')

        client.sendto(mes, server_address)
        data, server = client.recvfrom(max_size)

        data = data.decode('utf-8')
        recData = json.loads(data)
        print('At', datetime.now(), server, 'said', recData)
        client.close()
        print('!!!!!!!', recData['result'])
        self.my_result = recData['result']

        return self.my_result

    def aaa(self, veh_id):
        if veh_id > 5:
            return 1
        else:
            return 0

    def drawVehicles(self, qp):

        qp.setPen(Qt.black)
        qp.setBrush(Qt.green)

        qp.drawRect(310, 310, 5, 10)

        for i in range(10):
            if self.propose(i):
                print('?????????????')
                #qp.drawRect(300, 300, 5, 10)
            else:
                print('!!!!!!!!!!!!!')
                #qp.drawRect(400, 400, 5, 10)

        # # Vehicles from North
        # for i, veh in enumerate(vehicles_N):
        #     if (veh.getPosition().x + veh.getSpeed().x, veh.getPosition().y + veh.getSpeed().y) in self.collision_check_N:
        #         qp.drawRect(veh.getPosition().x, veh.getPosition().y, veh.getSize().x, veh.getSize().y)
        #         for i in range(11):
        #             self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y - i))
        #     else:
        #         if veh.getPosition().y + veh.getSpeed().y > 260 and veh.getPosition().y <= 260:
        #             if self.single_0_1:
        #                 qp.drawRect(veh.getPosition().x, veh.getPosition().y, veh.getSize().x, veh.getSize().y)
        #                 for i in range(11):
        #                     self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y - i))
        #             else:
        #                 if veh.getPosition().y <= 270:
        #                     if self.grid[((veh.getPosition().x + veh.getSpeed().x) // 10 * 10,
        #                                   (veh.getPosition().y + veh.getSpeed().y + veh.getSize().y) // 10 * 10)] and \
        #                             self.grid[((veh.getPosition().x + veh.getSpeed().x + veh.getSize().x) // 10 * 10,
        #                                        (veh.getPosition().y + veh.getSpeed().y + veh.getSize().y) // 10 * 10)]:
        #
        #                         veh.getPosition().y += veh.getSpeed().y
        #                         qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
        #                         for i in range(11):
        #                             self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y - i))
        #                         self.grid[(veh.getPosition().x // 10 * 10, (veh.getPosition().y + veh.getSize().y) // 10 * 10)] = False
        #                         self.grid[((veh.getPosition().x + veh.getSize().x) // 10 * 10, (veh.getPosition().y + veh.getSize().y) // 10 * 10)] = False
        #                 else:
        #                     try:
        #                         if self.grid[((veh.getPosition().x + veh.getSpeed().x) // 10 * 10,
        #                                       (veh.getPosition().y + veh.getSpeed().y) // 10 * 10)] and \
        #                                 self.grid[((veh.getPosition().x + veh.getSpeed().x + veh.getSize().x) // 10 * 10,
        #                                            (veh.getPosition().y + veh.getSpeed().y) // 10 * 10)] and \
        #                                 self.grid[((veh.getPosition().x + veh.getSpeed().x) // 10 * 10,
        #                                            (veh.getPosition().y + veh.getSpeed().y + veh.getSize().y) // 10 * 10)] and \
        #                                 self.grid[((veh.getPosition().x + veh.getSpeed().x + veh.getSize().x) // 10 * 10,
        #                                            (veh.getPosition().y + veh.getSpeed().y + veh.getSize().y) // 10 * 10)]:
        #
        #                             self.vehicles_N[i].getPosition().y += veh.getSpeed().y
        #
        #                             self.grid[((veh.getPosition().x + veh.getSpeed().x) // 10 * 10,
        #                                        (veh.getPosition().y + veh.getSpeed().y) // 10 * 10)] = False
        #                             self.grid[((veh.getPosition().x + veh.getSpeed().x + veh.getSize().x) // 10 * 10,
        #                                        (veh.getPosition().y + veh.getSpeed().y) // 10 * 10)] = False
        #                             self.grid[((veh.getPosition().x + veh.getSpeed().x) // 10 * 10,
        #                                        (veh.getPosition().y + veh.getSpeed().y + veh.getSize().y) // 10 * 10)] = False
        #                             self.grid[((veh.getPosition().x + veh.getSpeed().x + veh.getSize().x) // 10 * 10,
        #                                        (veh.getPosition().y + veh.getSpeed().y + veh.getSize().y) // 10 * 10)] = False
        #
        #                             if self.vehicles_N[i].getPosition().y > 600:
        #                                 self.vehicles_N[i].getPosition().y = 0
        #                                 qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
        #                                 for i in range(11):
        #                                     self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y - i))
        #
        #                     except KeyError:
        #                         self.vehicles_N[i].getPosition().y += veh.getSpeed().y
        #
        #                         if self.vehicles_N[i].getPosition().y > 600:
        #                             self.vehicles_N[i].getPosition().y = 0
        #
        #                         qp.drawRect(self.vehicles_N[i].getPosition().x, self.vehicles_N[i].getPosition().y, 5, 10)
        #
        #         else:
        #             # print(self.single_0_1)
        #             veh.getPosition().y += veh.getSpeed().y
        #             if veh.getPosition().y > 600:
        #                 veh.getPosition().y = 0
        #                 # print(self.t.elapsed())
        #             qp.drawRect(veh.getPosition().x, veh.getPosition().y, 5, 10)
        #             for i in range(11):
        #                 self.collision_check_N.append((veh.getPosition().x, veh.getPosition().y - i))
        #
        #     #print(self.collision_check)
        #
        #
        #
        # # Vehicles from West
        # for i, veh in enumerate(vehicles_W):
        #     # Check if there are vehicles ahead. If true, stop
        #     if (veh.getPosition().x + veh.getSpeed().x, veh.getPosition().y + veh.getSpeed().y) in self.collision_check_W:
        #         qp.drawRect(veh.getPosition().x, veh.getPosition().y, veh.getSize().x, veh.getSize().y)
        #         # Make the room not available for other vehicles
        #         for j in range(11):
        #             self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
        #     # Move forward
        #     else:
        #         # Just before the intersection
        #         if veh.getPosition().x + 10 + 2 > 270 and veh.getPosition().x <= 270 - 10:
        #             # Check traffic signal. True, then stop before entering.
        #             if self.single_0_0:
        #                 qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
        #                 for j in range(11):
        #                     self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
        #             # Enter intersection
        #             else:
        #                 veh.getPosition().x += 2
        #                 qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
        #                 for j in range(11):
        #                     self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
        #
        #                 # Light up the grids in the intersection
        #                 # Up left
        #                 if (veh.getPosition().x // 10 * 10, veh.getPosition().y // 10 * 10) in self.grid:
        #                     self.grid[(veh.getPosition().x // 10 * 10, veh.getPosition().y // 10 * 10)] = False
        #                     #print('success, x:', veh.getPosition().x)
        #
        #                 # Up right
        #                 if ((veh.getPosition().x + 10) // 10 * 10, veh.getPosition().y // 10 * 10) in self.grid:
        #                     self.grid[((veh.getPosition().x + 10) // 10 * 10, veh.getPosition().y // 10 * 10)] = False
        #                     #print('success, x:', veh.getPosition().x)
        #
        #                 # Down left
        #                 if (veh.getPosition().x // 10 * 10, (veh.getPosition().y) // 10 * 10) in self.grid:
        #                     self.grid[(veh.getPosition().x // 10 * 10, (veh.getPosition().y + 5) // 10 * 10)] = False
        #                     #print('success, x:', veh.getPosition().x)
        #
        #                 # Down right
        #                 if ((veh.getPosition().x + 10) // 10 * 10, (veh.getPosition().y) // 10 * 10) in self.grid:
        #                     self.grid[((veh.getPosition().x + 10) // 10 * 10, (veh.getPosition().y + 5) // 10 * 10)] = False
        #                     #print('success, x:', veh.getPosition().x)
        #
        #         # Already in the intersection
        #         else:
        #             if 270 < veh.getPosition().x < 328 and veh.getPosition().y < 330:
        #                 qp.save()
        #                 qp.translate(veh.getPosition().x, veh.getPosition().y)
        #
        #                 # Calculate rotation angle
        #                 if (((veh.getPosition().x - 270 + 3) / 60) * 90 > 15):
        #                     self.r[i] = ((veh.getPosition().x - 270 + 3) / 60) * 90
        #                     qp.rotate(self.r[i])
        #                 else:
        #                     self.r[i] = 0
        #                     qp.rotate(self.r[i])
        #                 qp.translate(-veh.getPosition().x, -veh.getPosition().y)
        #
        #                 # Calculate trajectory by using Bezier Curve
        #                 x = pow(1 - (self.beze_t[i] / 60), 2) * 273 + 2 * (self.beze_t[i] / 60) * (
        #                 1 - self.beze_t[i] / 60) * 332 + pow(
        #                     self.beze_t[i] / 60, 2) * 332
        #                 y = pow(1 - (self.beze_t[i] / 60), 2) * 273 + 2 * (self.beze_t[i] / 60) * (
        #                 1 - self.beze_t[i] / 60) * 273 + pow(
        #                     self.beze_t[i] / 60, 2) * 332
        #                 veh.setPosition(Position(x, y))
        #
        #                 self.beze_t[i] += 2
        #                 qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
        #                 for j in range(11):
        #                     self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
        #                 qp.restore()
        #
        #                 # Calculate the big Square's coordinate
        #                 self.up_left_x[i] = self.coordinate_up_left_x(veh.getPosition().x, self.r[i])
        #                 self.up_left_y[i] = self.coordinate_up_left_y(veh.getPosition().y)
        #                 self.down_left_x[i] = self.coordinate_down_left_x(veh.getPosition().x, self.r[i])
        #                 self.down_left_y[i] = self.coordinate_down_left_y(veh.getPosition().y, self.r[i])
        #                 self.up_right_x[i] = self.coordinate_up_right_x(veh.getPosition().x, self.r[i])
        #                 self.up_right_y[i] = self.coordinate_up_right_y(veh.getPosition().y)
        #                 self.down_right_x[i] = self.coordinate_down_right_x(veh.getPosition().x, self.r[i])
        #                 self.down_right_y[i] = self.coordinate_down_right_y(veh.getPosition().y, self.r[i])
        #
        #                 # Up left
        #                 if (self.up_left_x[i] // 10 * 10, self.up_left_y[i] // 10 * 10) in self.grid:
        #                     self.grid[(self.up_left_x[i] // 10 * 10, self.up_left_y[i] // 10 * 10)] = False
        #                     # print('success')
        #
        #                 # Up right
        #                 if ((self.up_right_x[i]) // 10 * 10, self.up_right_y[i] // 10 * 10) in self.grid:
        #                     self.grid[((self.up_right_x[i]) // 10 * 10, self.up_right_y[i] // 10 * 10)] = False
        #                     # print('success')
        #
        #                 # Down left
        #                 if (self.down_left_x[i] // 10 * 10, (self.down_left_y[i]) // 10 * 10) in self.grid:
        #                     self.grid[(self.down_left_x[i] // 10 * 10, (self.down_left_y[i]) // 10 * 10)] = False
        #                     # print('success')
        #
        #                 # Down right
        #                 if ((self.down_right_x[i]) // 10 * 10, (self.down_right_y[i]) // 10 * 10) in self.grid:
        #                     self.grid[((self.down_right_x[i]) // 10 * 10, (self.down_right_y[i]) // 10 * 10)] = False
        #                     # print('success')
        #
        #             # Already left intersection
        #             elif 328 <= veh.getPosition().x and veh.getPosition().y < 600:
        #                 qp.save()
        #                 qp.translate(veh.getPosition().x, veh.getPosition().y)
        #                 qp.rotate(90)
        #                 qp.translate(-veh.getPosition().x, -veh.getPosition().y)
        #                 veh.getPosition().y += 2
        #                 qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
        #                 for j in range(11):
        #                     self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y - j))
        #                 qp.restore()
        #
        #             # Already left screen
        #             elif veh.getPosition().y >= 600:
        #                 veh.getPosition().x = 0
        #                 veh.getPosition().y = 273
        #                 self.beze_t[i] = 0
        #                 qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
        #                 for j in range(11):
        #                     self.collision_check_W.append((veh.getPosition().x, veh.getPosition().y - j))
        #
        #             # Move horizontal direction(across X_axis)
        #             else:
        #                 veh.getPosition().x += 2
        #                 qp.drawRect(veh.getPosition().x, veh.getPosition().y, 10, 5)
        #                 for j in range(11):
        #                     self.collision_check_W.append((veh.getPosition().x - j, veh.getPosition().y))
        #
        # # Vehicle2
        # # if self.single_0_0:
        # #     qp.drawRect(self.vehicles_E[0].getPosition().x, self.vehicles_E[0].getPosition().y, 10, 5)
        # # else:
        # try:
        #     if self.grid[((self.vehicles_E[0].getPosition().x - 5) // 10 * 10, self.vehicles_E[0].getPosition().y // 10 * 10)] and \
        #             self.grid[((self.vehicles_E[0].getPosition().x + 10 - 5) // 10 * 10, self.vehicles_E[0].getPosition().y // 10 * 10)] and \
        #             self.grid[((self.vehicles_E[0].getPosition().x - 5) // 10 * 10, (self.vehicles_E[0].getPosition().y + 5) // 10 * 10)] and \
        #             self.grid[((self.vehicles_E[0].getPosition().x + 10 - 5) // 10 * 10, (self.vehicles_E[0].getPosition().y + 5) // 10 * 10)]:
        #
        #         self.vehicles_E[0].getPosition().x -= 3
        #
        #         if self.vehicles_E[0].getPosition().x < 0:
        #             self.vehicles_E[0].getPosition().x = 600
        #
        #         qp.drawPoint(self.vehicles_E[0].getPosition().x + 1, self.vehicles_E[0].getPosition().y - 1)
        #         qp.drawRect(self.vehicles_E[0].getPosition().x, self.vehicles_E[0].getPosition().y, 10, 5)
        #
        #     else:
        #         qp.drawPoint(self.vehicles_E[0].getPosition().x + 1, self.vehicles_E[0].getPosition().y - 1)
        #         qp.drawRect(self.vehicles_E[0].getPosition().x, self.vehicles_E[0].getPosition().y, 10, 5)
        #
        # except KeyError:
        #     self.vehicles_E[0].getPosition().x -= 3
        #
        #     if self.vehicles_E[0].getPosition().x < 0:
        #         self.vehicles_E[0].getPosition().x = 600
        #
        #     qp.drawPoint(self.vehicles_E[0].getPosition().x + 1, self.vehicles_E[0].getPosition().y - 1)
        #     qp.drawRect(self.vehicles_E[0].getPosition().x, self.vehicles_E[0].getPosition().y, 10, 5)
        #
        # self.collision_check = []
        # self.collision_check_N = []
        # self.collision_check_S = []
        # self.collision_check_W = []
        # self.collision_check_E = []
        #
        #
        # for i in range(270, 330, 10):
        #     for j in range(270, 330, 10):
        #         self.grid[(i, j)] = True
        #
        #
        self.ti += 10
        if self.ti > 700:
            self.ti = 0
            # print(self.t.elapsed())
            self.t.restart()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Vehicles from North
    vehicles_N = []
    for i in range(5):
        v = Vehicle()
        v.setPosition(Position(313, 0 - i * 10))
        v.setSpeed(Speed(0, 2))
        v.setSize(Size(5, 10))
        vehicles_N.append(v)

    # Vehicles from West
    vehicles_W = []
    for i in range(9):
        v = Vehicle()
        v.setPosition(Position(0 - i * 10, 273))
        v.setSpeed(Speed(2, 0))
        v.setSize(Size(10, 5))
        vehicles_W.append(v)


    # Vehicles from East
    vehicles_E = []
    v = Vehicle()
    v.setPosition(Position(600, 280))
    v.setSpeed(Speed(2, 0))
    v.setSize(Size(10, 5))
    vehicles_E.append(v)

    sendData = [{
            "Veh_id": 0,
            "arrival_time": 1,
            "arrival_lane": 1
        }, {
            "Veh_id": 1,
            "arrival_time": 2,
            "arrival_lane": 1
        }, {
            "Veh_id": 2,
            "arrival_time": 3,
            "arrival_lane": 1
        }, {
            "Veh_id": 3,
            "arrival_time": 4,
            "arrival_lane": 1
        }, {
            "Veh_id": 4,
            "arrival_time": 5,
            "arrival_lane": 1
        }, {
            "Veh_id": 5,
            "arrival_time": 6,
            "arrival_lane": 1
        }, {
            "Veh_id": 6,
            "arrival_time": 7,
            "arrival_lane": 1
        }, {
            "Veh_id": 7,
            "arrival_time": 8,
            "arrival_lane": 1
        }, {
            "Veh_id": 8,
            "arrival_time": 9,
            "arrival_lane": 1
        }, {
            "Veh_id": 9,
            "arrival_time": 10,
            "arrival_lane": 1}]

    ex = Example(vehicles_N, vehicles_W, vehicles_E, sendData)

    sys.exit(app.exec_())