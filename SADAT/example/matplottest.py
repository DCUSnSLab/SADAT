import sys
import time
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MyApp(QMainWindow):

  def __init__(self):
      super().__init__()

      self.main_widget = QWidget()
      self.setCentralWidget(self.main_widget)

      canvas = FigureCanvas(Figure(figsize=(4, 3)))
      vbox = QVBoxLayout(self.main_widget)
      vbox.addWidget(canvas)

      self.addToolBar(NavigationToolbar(canvas, self))

      self.ax = canvas.figure.subplots()
      self.ax.plot([0, 1, 2], [1, 5, 3], '-')

      dynamic_canvas = FigureCanvas(Figure(figsize=(4, 3)))
      vbox.addWidget(dynamic_canvas)

      self.dynamic_ax = dynamic_canvas.figure.subplots()
      self.timer = dynamic_canvas.new_timer(
          10, [(self.update_canvas, (), {})])
      self.timer.start()

      self.setWindowTitle('Matplotlib in PyQt5')
      self.setGeometry(300, 100, 600, 600)
      self.show()

  def update_canvas(self):
      self.dynamic_ax.clear()
      t = np.linspace(0, 2 * np.pi, 101)
      self.dynamic_ax.plot(t, np.sin(t + time.time()), color='deeppink')
      self.dynamic_ax.figure.canvas.draw()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())