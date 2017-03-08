"""Main class for settings managment."""
import numpy as np

from PyQt4.QtGui import *


__all__ = ['uiSettings']


class uiSettings(object):
    """Main class for settings managment."""

    def __init__(self):
        """Init."""
        # =====================================================================
        # MENU & FILES
        # =====================================================================

        # ------------------------------- FILE -------------------------------
        # Screenshot :
        screenshot = QAction("Screenshot", self)
        screenshot.setShortcut("Ctrl+N")
        screenshot.triggered.connect(self._screenshot)
        self.menuFiles.addAction(screenshot)

        # Save :
        save = QAction("Save", self)
        save.setShortcut("Ctrl+S")
        save.triggered.connect(self.saveFile)
        self.menuFiles.addAction(save)

        # Load :
        openm = QAction("Load", self)
        openm.setShortcut("Ctrl+O")
        openm.triggered.connect(self.openFile)
        self.menuFiles.addAction(openm)

        # Quit :
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        self.menuFiles.addAction(exitAction)

        # =====================================================================
        # SETTINGS PANEL
        # =====================================================================
        # Quick settings panel :
        self.actionQuick_settings.triggered.connect(self._toggle_settings)
        self.q_widget.setVisible(True)

        # =====================================================================
        # SLIDER
        # =====================================================================
        self._slFrame.setMaximumHeight(100)
        # Function applied when the slider move :
        self._slOnStart = False
        self._fcn_sliderSettings()
        self._SlVal.valueChanged.connect(self._fcn_sliderMove)
        # Function applied when slider's settings changed :
        self._SigWin.valueChanged.connect(self._fcn_sliderSettings)
        self._SigWin.setKeyboardTracking(False)
        self._SigSlStep.valueChanged.connect(self._fcn_sliderSettings)
        self._SigSlStep.setKeyboardTracking(False)
        # Spin box for window selection :
        self._SlWin.valueChanged.connect(self._fcn_sliderWinSelection)
        self._SlWin.setKeyboardTracking(False)
        # Unit conversion :
        self._slRules.currentIndexChanged.connect(self._fcn_sliderMove)
        # Grid toggle :
        self._slGrid.clicked.connect(self._fcn_gridToggle)

        # =====================================================================
        # ZOOMING
        # =====================================================================
        self._PanHypZoom.clicked.connect(self._fcn_Zooming)
        self._PanSpecZoom.clicked.connect(self._fcn_Zooming)
        self._PanTimeZoom.clicked.connect(self._fcn_Zooming)

    # =====================================================================
    # MENU & FILE MANAGMENT
    # =====================================================================
    def saveFile(self):
        """
        """
        raise ValueError("NOT CONFIGURED")
        # filename = QFileDialog.getSaveFileName(self, 'Save File',
        #                                        os.getenv('HOME'))
        # f = open(filename, 'w')
        # filedata = self.text.toPlainText()
        # f.write(filedata)
        # f.close()

    def openFile(self):
        """
        """
        raise ValueError("NOT CONFIGURED")
        # filename = QFileDialog.getSaveFileName(self, 'Open File',
        #                                        os.getenv('HOME'))
        # f = open(filename, 'w')
        # filedata = self.text.toPlainText()
        # f.write(filedata)
        # f.close()

    def _fcn_panSettingsViz(self):
        """
        """
        pass

    def _fcn_CanVisToggle(self):
        """Toggle the different panel."""
        self._NdVizPanel.setVisible(self._CanVisNd.isChecked())
        self._1dVizPanel.setVisible(self._CanVis1d.isChecked())
        # self._ImVizPanel.setVisible(self._CanVis1d.isChecked())

    def _fcn_QuickTabSelec(self):
        """On Quick settings tab selection.

        Triggered function when the user select a tab from the QuickSettings
        Tab widget.
        """
        pass
        # if self.QuickSettings.currentIndex() == 1:
        #     self._fcn_ndAxis_update()
        # if self.QuickSettings.currentIndex() == 2:
        #     self._fcn_1dAxis_update()
        # elif self.QuickSettings.currentIndex() == 3:
        #     self._fcn_imAxis_update()
        # pass

    def _fcn_1dPltTabSelect(self):
        """On Inspect tab selection.

        Triggered function when the user select a tab from the Inspect
        Tab widget.
        """
        if self._1dPltTab.currentIndex() == 0:
            self._fcn_1dAxis_update()
        elif self._1dPltTab.currentIndex() == 1:
            self._fcn_imAxis_update()

    # =====================================================================
    # GUI
    # =====================================================================
    def _screenshot(self):
        """Screenshot using the GUI.

        This function need that a savename is already defined (otherwise, a
        window appeared so that the user specify the path/name). Then, it needs
        an extension (png) and a boolean parameter (self.cb['export']) to
        specify if the colorbar has to be exported.
        """
        pass

    def _toggle_settings(self):
        """Toggle method for display / hide the settings panel."""
        self.q_widget.setVisible(not self.q_widget.isVisible())

    # =====================================================================
    # SLIDER
    # =====================================================================
    def _fcn_sliderMove(self):
        """Function applied when the slider move."""
        # ================= INDEX =================
        # Get slider variables :
        val = self._SlVal.value()
        step = self._SigSlStep.value()
        win = self._SigWin.value()
        xlim = (val*step, val*step+win)
        specZoom = self._PanSpecZoom.isChecked()
        hypZoom = self._PanHypZoom.isChecked()
        timeZoom = self._PanTimeZoom.isChecked()

        # Find closest time index :
        t = [0, 0]
        t[0] = round(np.abs(self._time - xlim[0]).argmin())
        t[1] = round(np.abs(self._time - xlim[1]).argmin())

        # ================= MESH UPDATES =================
        # ---------------------------------------
        # Update display signal :
        sl = slice(t[0], t[1])
        self._chan.set_data(self._sf, self._data, self._time, sl=sl,
                            ylim=self._ylims)

        # ---------------------------------------
        # Update spectrogram indicator :
        if self._PanSpecIndic.isEnabled() and not specZoom:
            ylim = (self._PanSpecFstart.value(), self._PanSpecFend.value())
            self._specInd.set_data(xlim=xlim, ylim=ylim)

        # ---------------------------------------
        # Update hypnogram indicator :
        if self._PanHypIndic.isEnabled() and not hypZoom:
            self._hypInd.set_data(xlim=xlim, ylim=(-6., 2.))

        # ---------------------------------------
        # Update Time indicator :
        if self._PanTimeIndic.isEnabled():
            self._TimeAxis.set_data(xlim[0], win, self._time,
                                    unit=self._slRules.currentText())

        # ================= GUI =================
        # Update Go to :
        self._SlWin.setValue(val*step)

        # ================= ZOOMING =================
        # Histogram :
        if hypZoom:
            self._hypcam.rect = (xlim[0], -5, xlim[1]-xlim[0], 7.)

        # Spectrogram :
        if specZoom:
            self._speccam.rect = (xlim[0], self._spec.freq[0], xlim[1]-xlim[0],
                                  self._spec.freq[-1] - self._spec.freq[0])

        # Time axis :
        if timeZoom:
            self._TimeAxis.set_data(xlim[0], win, np.array([xlim[0], xlim[1]]),
                                    unit='seconds')
            self._timecam.rect = (xlim[0], 0., win, 1.)

    def _fcn_sliderSettings(self):
        """Function applied to change slider settings."""
        # Set minimum :
        self._SlVal.setMinimum(self._time.min())
        # Set maximum :
        step = self._SigSlStep.value()
        self._SlVal.setMaximum((self._time.max()-self._SigWin.value())/step)
        self._SlVal.setTickInterval(step)
        self._SlVal.setSingleStep(step)
        self._SlWin.setMaximum((self._time.max()-self._SigWin.value()))

        if self._slOnStart:
            self._fcn_sliderMove()
        else:
            self._slOnStart = True

    def _fcn_sliderWinSelection(self):
        """Move slider using window spin."""
        self._SlVal.setValue(self._SlWin.value() / self._SigSlStep.value())

    def _fcn_gridToggle(self):
        """Toggle grid visibility."""
        viz = self._slGrid.isChecked()
        # Toggle hypno grid :
        self._hyp.grid.visible = viz
        # Toggle grid for each channel :
        for k in self._chan.grid:
            k.visible = viz

    def _get_factFromUnit(self):
        """Get factor conversion from current selected unit."""
        unit = self._slRules.currentText()
        if unit == 'seconds':
            fact = 1.
        elif unit == 'minutes':
            fact = 60.
        elif unit == 'hours':
            fact = 3600.
        return fact

    def _fcn_Zooming(self):
        """Apply dynamic zoom on hypnogram."""
        # Hypnogram :
        if self._PanHypZoom.isChecked():
            self._PanHypIndic.setEnabled(False)
            self._hypInd.mesh.visible = False
        else:
            self._PanHypIndic.setEnabled(True)
            self._hypcam.rect = (self._time.min(), -5.,
                                 self._time.max() - self._time.min(), 7.)
            self._hypInd.mesh.visible = self._PanHypIndic.isChecked()

        # Spectrogram :
        if self._PanSpecZoom.isChecked():
            self._PanSpecIndic.setEnabled(False)
            self._specInd.mesh.visible = False
        else:
            self._PanSpecIndic.setEnabled(True)
            self._speccam.rect = (self._time.min(), self._spec.freq[0],
                                  self._time.max() - self._time.min(),
                                  self._spec.freq[-1] - self._spec.freq[0])
            self._specInd.mesh.visible = self._PanSpecIndic.isChecked()
        # Time axis :
        if self._PanTimeZoom.isChecked():
            # self._PanTimeIndic.setChecked(False)
            self._PanTimeIndic.setEnabled(False)
            self._TimeAxis.mesh.visible = False
        else:
            self._PanTimeIndic.setEnabled(True)
            self._timecam.rect = (self._time.min(), 0.,
                                  self._time.max() - self._time.min(), 1.)
            self._TimeAxis.mesh.visible = self._PanTimeIndic.isChecked()

        self._fcn_sliderMove()

    def on_mouse_wheel(self, event):
        """Executed function on mouse wheel."""
        self._SlVal.setValue(self._SlVal.value() + event.delta[1])
