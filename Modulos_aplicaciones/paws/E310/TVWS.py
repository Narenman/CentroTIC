#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Transmision simulando un TVWS
# Author: Mario Castaneda
# Description: Prueba piloto del protocolo PAWS
# Generated: Mon Jun 17 09:57:38 2019
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy
import time


class TVWS(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Transmision simulando un TVWS")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.freq = freq = 0

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_gain(50, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.digital_psk_mod_0 = digital.psk.psk_mod(
          constellation_points=2,
          mod_code="none",
          differential=False,
          samples_per_symbol=2,
          excess_bw=0.35,
          verbose=False,
          log=False,
          )
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 2, 1000)), True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.digital_psk_mod_0, 0))
        self.connect((self.digital_psk_mod_0, 0), (self.uhd_usrp_sink_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)


def main(top_block_cls=TVWS, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
