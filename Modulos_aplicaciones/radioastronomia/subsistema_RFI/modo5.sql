SELECT radioastronomia_espectro.id, radioastronomia_espectro.frec_central
FROM radioastronomia_posicionantena INNER JOIN radioastronomia_espectro
ON date_trunc('minute',radioastronomia_espectro.fecha)=date_trunc('minute', radioastronomia_posicionantena.fecha)
WHERE (radioastronomia_posicionantena.azimut = 0 AND radioastronomia_posicionantena.elevacion=0 AND radioastronomia_espectro.region_id = 32)
ORDER BY radioastronomia_espectro.frec_central;