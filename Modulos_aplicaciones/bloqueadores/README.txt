Primero debe guardar en la base de datos:

* sudo su postgres

* psql centrotic

* copy bloqueadores_ciudad(id,nombre,departamento) FROM '/home/uis-e3t/back_centrotic/CentroTIC/Modulos_aplicaciones/bloqueadores/ciudad.csv' DELIMITER ',' CSV HEADER;

* copy bloqueadores_usuariosprimarios(id,frecuencia,nombre_emisora,clase_emisora,ciudad_id) FROM '/home/uis-e3t/back_centrotic/CentroTIC/Modulos_aplicaciones/bloqueadores/bloqueadores_usuariosprimarios.csv' DELIMITER ',' CSV HEADER;

* copy bloqueadores_dispositivos(id,modelo_id,ubicacion,ciudad_id) FROM '/home/uis-e3t/back_centrotic/CentroTIC/Modulos_aplicaciones/bloqueadores/bloqueadores_dispositivos.csv' DELIMITER ',' CSV HEADER;

* copy bloqueadores_espectro(id,espectro_iq, frec_central, dispositivo_id, samp_rate, fft_size) FROM '/home/uis-e3t/back_centrotic/CentroTIC/Modulos_aplicaciones/bloqueadores/bloqueadores_espectro.csv' DELIMITER ',' CSV HEADER;

