# from pythonwifi.iwlibs import Wireless

# wifi = Wireless('wlan0')
# print(wifi.getEssid())

from wifi import Cell, Scheme

a = Cell.all('wlan0')
print(a.ssid())