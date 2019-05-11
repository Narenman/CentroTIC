import requests

"""
Este es el archivo del maestro, donde se ejecutaran 
las acciones importantes
AVAIL_SPECTRUM_REQ                                  
   +----------------------------------+-----------------+
   |deviceDesc:DeviceDescriptor       | see description |
   |location:GeoLocation              | see description |
   |owner:DeviceOwner                 | OPTIONAL        |
   |..................................|.................|
"""
#esta informacion deberia enviarla el esclavo a 
#traves de MQTT
AVAIL_SPECTRUM_REQ = {"serial_Number":"USRPE310",
                      "ruleset_Ids":"xxxxx",
                      "model_Id":"xxxx",
                      "manufacturer_Id":"xxxxx",
                      "dane_code":5266,
                      "contact": "mario",
                      "email":"luismiguel@radiogis.uis.edu.co"}

r = requests.post("http://127.0.0.1:8000/paws/avail-spectrum", data=AVAIL_SPECTRUM_REQ)
if r.status_code==200:
    print("HTTP status ok. {}".format(r.status_code))
    AVAIL_SPECTRUM_RESP = r.text
    print(AVAIL_SPECTRUM_RESP)
r.close()