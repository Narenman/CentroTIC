# This Python file uses the following encoding: utf-8
import os, sys
import mraa
import time

def dsensors():
	spi=mraa.Spi(0) #Bus comunication
	spi.mode(mraa.SPI_MODE0) #Comunication MODE0
	spi.frequency(4100000) #Frequency of 4.1MHz
	spi.lsbmode(False) #Format data MSB

	ss=mraa.Gpio(9) #wire CS1
	ss.dir(mraa.DIR_OUT)
	ss.write(1)

	sc=mraa.Gpio(8) #wire CS2
	sc.dir(mraa.DIR_OUT)
	sc.write(1)

	def readadc(pinaleer,ss):
		dieccionaleer=0x0c #Input c=1100 so Output data length 16bits,  MSB first, Unipolar
		pinaleer=int(hex(pinaleer),16) #address bits (4)
		dieccionaleer = dieccionaleer | (pinaleer<<4) #Put address bit in the 4th bits
		#Comunication        
		ss.write(0)  #CS=0 <-- Enables the device
		esc=spi.writeByte(dieccionaleer) #First byte with input info
		esc2=spi.writeByte(0x00) #Complete the 16bits --> Clock
		ss.write(1) #CS=1 <--- Disables the device
		time.sleep(0.00020) #Wait more time than 10us= time conversion AD
		ss.write(0) #CS=0 <-- Enables the device
		primerbyte=spi.writeByte(0x00) #First byte with 8bit of information
		segundobyte=spi.writeByte(0x00) #Second byte with 4bit (MSB) information , 8+4=12bits
		ss.write(1) #CS=1 <--- Disables the device

		salida1=0x0000
		salida1=salida1 | (primerbyte << 8)
		salida1=salida1 | (segundobyte)
		salida = (salida1>>4)+1 #Output 12bits
		   
		return salida

	dato1 = readadc(0,ss)
	dato2 = readadc(1,ss)
	dato3 = readadc(2,ss)
	dato4 = readadc(3,ss)
	dato5 = readadc(4,ss)
	dato6 = readadc(5,ss)
	dato7 = readadc(6,ss)
	dato8 = readadc(7,ss)
	#dato9 = readadc(9,ss)
	#dato10= readadc(10,ss)
	#dato11= readadc(11,ss) #pin Test (Vref+ - Vref-) /2    =~ 2048
	#dato12= readadc(12,ss) #pin Test Vref-  0000
	#dato13= readadc(13,ss) #pin Test Vref+  4096

	dato14 = readadc(0,sc)
	dato15 = readadc(1,sc)
	dato16 = readadc(2,sc)
	dato17 = readadc(3,sc)
	dato18 = readadc(4,sc)
	dato19 = readadc(5,sc)
	dato20 = readadc(6,sc)
	dato21 = readadc(7,sc)
	#dato22 = readadc(9,sc)
	#dato23 = readadc(10,sc)
	#dato24 = readadc(11,sc) #pin Test (Vref+ - Vref-) /2    =~ 2048
	#dato25 = readadc(12,sc) #pin Test Vref-  0000
	#dato26 = readadc(13,sc) #pin Test Vref+  4096

	#print ("Datos 1 ADCp8 Azul")
	values=[dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, dato14, dato15, dato16, dato17, dato18, dato19, dato20, dato21]#, dato9, dato10, dato11, dato12, dato13, 0, dato14, dato15, dato16, dato17, dato18, dato19, dato20, dato21, dato22, dato23, dato24, dato25, dato26]
	dates=time.strftime("%Y-%m-%d %H:%M:%S")
	
	# return [dates,values]
	return [values]

