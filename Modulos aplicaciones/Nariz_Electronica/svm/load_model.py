from sklearn.externals import joblib
import pandas as pd
import os

data = [[-0.23681726856295066, 0.027414701954353554, 0.2775467786369569, 0.07892015261770202, 0.328938374675732, 0.14907935753041485, 0.20675583819642912, 0.14781325605633192, 0.4295455562083896, 0.11037998724006537,],]

#ruta donde se encuentra el proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVM_DIR = os.path.join(BASE_DIR,"svm")


datos = pd.DataFrame(data=data)
#apertura del modelo
clasificador = joblib.load(SVM_DIR+'/svm1_corr.pkl')
a = clasificador.predict(datos)
print(a)