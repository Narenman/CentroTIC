import requests

def estado(IP, estado):
    pyload = {"activo": estado}
    url = IP+"/radioastronomia/estado/1"
    r = requests.put(url, pyload)
    print("HTTP {} actualizacion estado".format(r.status_code))
    r.close()

if __name__ == "__main__":
    IP ="http://127.0.0.1:8000"
    estado(IP, True)