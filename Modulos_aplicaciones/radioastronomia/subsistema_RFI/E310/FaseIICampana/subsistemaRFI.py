#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Adquisicion de datos del espectro
# Author: Luis Miguel Diaz
# Description: Este modulo se encarga de adquirir las senales del espectro
# Generated: Wed Aug 14 07:37:38 2019
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser
import time


class subsistemaRFI(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Adquisicion de datos del espectro")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.nfft = nfft = 1024
        self.ganancia = ganancia = 0.2
        self.frec_central = frec_central = 0

        ##################################################
        # Blocks
        ##################################################
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
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate,
        	fft_size=nfft,
        	ref_scale=2,
        	frame_rate=30,
        	avg_alpha=0.3,
        	average=True,
        )
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*nfft, '/home/root/radioastronomia/espectro', False)
        self.blocks_file_sink_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.logpwrfft_x_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)

    def get_nfft(self):
        return self.nfft

    def set_nfft(self, nfft):
        self.nfft = nfft

    def get_ganancia(self):
        return self.ganancia

    def set_ganancia(self, ganancia):
        self.ganancia = ganancia

    def get_frec_central(self):
        return self.frec_central

    def set_frec_central(self, frec_central):
        self.frec_central = frec_central
        self.uhd_usrp_source_0.set_center_freq(self.frec_central, 0)


def main(top_block_cls=subsistemaRFI, options=None):

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
