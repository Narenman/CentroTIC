#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Monitoreo del espectro
# Generated: Tue Sep 10 09:52:37 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sip
import sys
import time
from gnuradio import qtgui


class Monitoreo_GUI(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Monitoreo del espectro")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Monitoreo del espectro")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Monitoreo_GUI")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate_GUI = samp_rate_GUI = 500000
        self.samp_rate = samp_rate = 16e6
        self.nfft = nfft = 2048
        self.frec_central = frec_central = 470e6

        ##################################################
        # Blocks
        ##################################################
        self._samp_rate_GUI_options = (500000, 8000000, 16000000, )
        self._samp_rate_GUI_labels = ('500kS/s', '8MS/s', '16MS/s', )
        self._samp_rate_GUI_tool_bar = Qt.QToolBar(self)
        self._samp_rate_GUI_tool_bar.addWidget(Qt.QLabel('sample rate'+": "))
        self._samp_rate_GUI_combo_box = Qt.QComboBox()
        self._samp_rate_GUI_tool_bar.addWidget(self._samp_rate_GUI_combo_box)
        for label in self._samp_rate_GUI_labels: self._samp_rate_GUI_combo_box.addItem(label)
        self._samp_rate_GUI_callback = lambda i: Qt.QMetaObject.invokeMethod(self._samp_rate_GUI_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._samp_rate_GUI_options.index(i)))
        self._samp_rate_GUI_callback(self.samp_rate_GUI)
        self._samp_rate_GUI_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_samp_rate_GUI(self._samp_rate_GUI_options[i]))
        self.top_grid_layout.addWidget(self._samp_rate_GUI_tool_bar)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(frec_central, 0)
        self.uhd_usrp_source_0.set_gain(50, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_GUI, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(True)






        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Monitoreo_GUI")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate_GUI(self):
        return self.samp_rate_GUI

    def set_samp_rate_GUI(self, samp_rate_GUI):
        self.samp_rate_GUI = samp_rate_GUI
        self._samp_rate_GUI_callback(self.samp_rate_GUI)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate_GUI)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_nfft(self):
        return self.nfft

    def set_nfft(self, nfft):
        self.nfft = nfft

    def get_frec_central(self):
        return self.frec_central

    def set_frec_central(self, frec_central):
        self.frec_central = frec_central
        self.uhd_usrp_source_0.set_center_freq(self.frec_central, 0)


def main(top_block_cls=Monitoreo_GUI, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
