from PyQt5.QtCore import QPropertyAnimation, QEasingCurve


animation = QPropertyAnimation()
animation.setTargetObject()
animation.setStartValue(0)
animation.setEndValue(1000)
animation.setDuration(1000)
animation.setEasingCurve(QEasingCurve.InOutQuad)

animation.start()