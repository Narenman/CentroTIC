import requests
import json

def send_API(URL, s1, s2, s3, s4):
	""" este metodo es para iniciar la comunicacion donde la base de
	datos retorna el init resp """
	data = {"s1": s1,
	"s2": s2,
	"s3": s3,
	"s4": s4}
	myToken = 'cbb69e3554e416aa4b39b3ddfee04dfd6f7dcd38'
	##headers={"Authorization":"cbb69e3554e416aa4b39b3ddfee04dfd6f7dcd38"}
	headers = {'Authorization': 'token {}'.format(myToken)}
	print(headers)
	print(data)
	r = requests.post(URL, data=data, headers=headers)
	if r.status_code==200 | r.status_code==201:
		print("HTTP status ok. {}".format(r.status_code))
		r.close()
	else:
		print(r.status_code)

if __name__ == "__main__":
	URL = "http://10.14.51.225:8080/nariz_electronicaV2/mq"
	s1 = 100
	s2 = 90
	s3 = 60
	s4 = 200
	send_API(URL, s1, s2, s3, s4)