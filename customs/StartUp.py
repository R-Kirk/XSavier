import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QProgressBar
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer, QSize
import time
import icons_resource_file_rc


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Splash Screen Example")
        self.setFixedSize(1100, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0 
        self.n = 100

        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(40)


        self.frame.setStyleSheet("""
            
        #LabelTitle{
                      font-size: 60px;
                      color: #93deed;
                      }
        #LabelDesc{
                      font-size: 30px;
                      color: #c2c3d1;

                      }
        
        #LabelLoading{
                      
                      font-size: 30px;
                      color: rgb(220, 220, 220)
                      }              
        
        QFrame{
                      background-color: #2F4454;
                      color: rgb(220, 220, 220);
        }
                      
        QProgressBar{
                      background-color: #DA7B93;
                      color: rgb(220, 200, 200);
                      border-style: none;
                      border-radius: 10px;
                      text-align: center;
                      font-size: 30px;
        }

        QProgressbar::chunk{
                      border-radius:10px;
                      background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
        }            

                      """)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame  = QFrame()
        layout.addWidget(self.frame)

        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName("LabelTitle")

        #Center Labels
        


        self.labelTitle.resize(self.width()-10, 150)
        self.labelTitle.move(50, 40) #x, y
        self.labelTitle.setText("XSavier")
        self.labelTitle.setAlignment(Qt.AlignCenter)


        self.label_XSavierLogo = QLabel(self.frame)
        self.label_XSavierLogo.setMaximumSize(QSize(75, 75))
        self.label_XSavierLogo.setText("")
        self.label_XSavierLogo.move(400, 75)
        self.label_XSavierLogo.setPixmap(QtGui.QPixmap(":/Other_Icons/logo.jpg"))
        self.label_XSavierLogo.setScaledContents(True)
        self.label_XSavierLogo.setObjectName("label_XSavierLogo")

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width()-10, 50)
        self.labelDescription.move(0,self.labelTitle.height())
        self.labelDescription.setObjectName("LabelDesc")
        self.labelDescription.setText("<strong>Loading Database...</strong>")
        self.labelDescription.setAlignment(Qt.AlignCenter)


        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width()-200, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)


        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width()-10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText("loading...")

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n*.3):
            self.labelDescription.setText("<strong>Analyzing Database...</strong>")
        elif self.counter == int(self.n *.6):
            self.labelDescription.setText("<strong>Cleaning Database...</strong>")
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(1)

            return True

        self.counter += 1
        

#if __name__ == '__main__':
def StartUp():
    app = QApplication(sys.argv)
   
    splash = SplashScreen()
    splash.show()

    try:
        sys.exit(app.exec_())
    except:
        print("[SPLASH]...Closing Start Up Window...")