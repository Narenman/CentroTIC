import requests
import json

def init_req(serial_Number, model_Id, manufacturer_Id,dane_code,):
    """ este metodo es para iniciar la comunicacion donde la base de datos
    retorna el init resp
    """
    URL = "http://127.0.0.1:8080/paws/init-req"
    INIT_REQ = {"serial_Number": serial_Number,
                            "model_Id": model_Id,
                            "manufacturer_Id": manufacturer_Id,
                            "dane_code": dane_code}

    r = requests.post(URL, data=INIT_REQ)
    if r.status_code==200:
        print("HTTP status ok. {}".format(r.status_code))
        INIT_RESP = r.text
        INIT_RESP = json.loads(INIT_RESP)
        INIT_RESP = INIT_RESP["ruleset_info"]
        INIT_RESP =INIT_RESP[0]["rulsetId"]
        print(INIT_RESP)
        r.close()
        return INIT_RESP
    else:
        return None

serial_Number = "e310-f5ab-ao0x"
model_Id = "USRP E310"
manufacturer_Id = "Ettus Research"
dane_code = 68001
init_req(serial_Number, model_Id, manufacturer_Id, dane_code)