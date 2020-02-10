from network import WLAN
wlan = WLAN(mode=WLAN.STA)
wlan.connect(ssid='ComunidadUIS', auth=(WLAN.WPA2_ENT, '2134283', 'parutajimenez'), identity='identity')