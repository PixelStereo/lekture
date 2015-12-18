from PyQt5.QtCore import QSettings, QPoint

settings = QSettings('foo', 'foo')

settings.setValue('int_value', 42)
settings.setValue('point_value', [10, 12])

quit()
# This will write the setting to the platform specific storage.
del settings

settings = QSettings('foo', 'foo')

int_value = settings.value('int_value', type=int)
print("int_value: %s" % repr(int_value))

point_value = settings.value('point_value', type=QPoint)
print("point_value: %s" % repr(point_value))