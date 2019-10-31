SELECT radioastronomia_espectro.id,  radioastronomia_posicionantena.elevacion, radioastronomia_espectro.fecha
FROM radioastronomia_espectro
INNER JOIN radioastronomia_posicionantena
ON date_trunc('second',radioastronomia_espectro.fecha)=date_trunc('second',radioastronomia_posicionantena.fecha)
WHERE radioastronomia_posicionantena.azimut=0
AND radioastronomia_espectro.frec_central=70000000
AND radioastronomia_espectro.frec_muestreo = 16000000
AND radioastronomia_espectro.nfft = 1024
AND date_trunc('second', radioastronomia_espectro.fecha)>= to_date('2019-08-27', 'YYYY-MM-DD')
AND date_trunc('second', radioastronomia_espectro.fecha)<=to_date('2019-10-28', 'YYYY-MM-DD') 
AND radioastronomia_espectro.region_id = 17
ORDER BY radioastronomia_posicionantena.elevacion;
