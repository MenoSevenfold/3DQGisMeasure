
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .resources import *
import os.path
from qgis.core import QgsMessageLog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QAction
from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.core import *
from .measure_3d_dialog import Measure3dDialog

import math

class Measure3d:


    def __init__(self, iface):

        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Measure3d_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        self.actions = []
        self.menu = self.tr(u'&Measure3d')
        self.toolbar = self.iface.addToolBar(u'Measure3d')
        self.toolbar.setObjectName(u'Measure3d')

    def tr(self, message):

        return QCoreApplication.translate('Measure3d', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
  
        self.dlg = Measure3dDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):

        icon_path = ':/plugins/measure3d/icon.png'

        self.add_action(
            icon_path,
            text=self.tr(u'Measure3d'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Measure3d'),
                action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar


    def run(self):

        self.dlg.show()

        result = self.dlg.exec_()
        if result:
            q_field = self.dlg.lineEdit.text()

            layer = self.iface.activeLayer()
            try:
                features = layer.selectedFeatures()
            except AttributeError:
                QMessageBox.information(self.iface.mainWindow(), "Error", "Select a layer")
                return

            if len(features)!=2:
                QMessageBox.information(self.iface.mainWindow(), "Error", "Select two points")
                return

            if self.dlg.checkBox.isChecked():
                try:
                    point1 = QgsPointV2()
                    point2 = QgsPointV2()
                    point1.fromWkt(features[0].geometry().exportToWkt())
                    point2.fromWkt(features[1].geometry().exportToWkt())
                    z1 = point1.z()
                    z2 = point2.z()
                except Exception as e:

                    QMessageBox.information(self.iface.mainWindow(), "Error", "I can't use geometry z value. Check your data.")
                    return
            else:


                if not q_field or q_field == '':
                        q_field = 'z'

                try:
                    t = float(features[1][q_field])
                except KeyError:
                    QMessageBox.information(self.iface.mainWindow(), "Error", "The field '%s' does not exists in your layer" % q_field)
                    return
                except ValueError:
                    QMessageBox.information(self.iface.mainWindow(), "Error", "I can't use the field '%s' as z value. Check your data." % q_field)
                    return
                z1 = float(features[0][q_field])
                z2 = float(features[1][q_field])

            point1 = features[0].geometry().asPoint()
            point2 = features[1].geometry().asPoint()

            res = math.sqrt( ( point1[0]-point2[0] )**2 +
                       ( point1[1]-point2[1] )**2 +
                       ( z1 - z2 )**2
                      )
            print(res)
            QMessageBox.information(self.iface.mainWindow(), "Distance", str(res) )
