#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Adquisicion de datos del espectro
# Author: Luis Miguel Diaz
# Description: Este modulo se encarga de adquirir las senales del espectro
# Generated: Mon Jul  8 11:27:12 2019
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser


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
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate,
        	fft_size=nfft,
        	ref_scale=2,
        	frame_rate=30,
        	avg_alpha=1.0,
        	average=False,
        )
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*nfft, '/home/uis-e3t/back_centrotic/CentroTIC/Modulos_aplicaciones/radioastronomia/subsistema RFI/espectro', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 10000, 1, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, ganancia, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.logpwrfft_x_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_file_sink_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_nfft(self):
        return self.nfft

    def set_nfft(self, nfft):
        self.nfft = nfft

    def get_ganancia(self):
        return self.ganancia

    def set_ganancia(self, ganancia):
        self.ganancia = ganancia
        self.analog_noise_source_x_0.set_amplitude(self.ganancia)

    def get_frec_central(self):
        return self.frec_central

    def set_frec_central(self, frec_central):
        self.frec_central = frec_central


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
