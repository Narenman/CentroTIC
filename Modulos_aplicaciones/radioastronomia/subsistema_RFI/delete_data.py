import psycopg2
"""Este script se encarga de borrar los datos registrados en la base de datos
correspondientes a las regiones """
conn = psycopg2.connect(database="centrotic", user="postgres",
                      password="raspberry", host="127.0.0.1",
                      port="5432")
cur = conn.cursor()
cur.execute("SELECT id, zona FROM radioastronomia_regioncampana;")
zonas = cur.fetchall()

ids = []
print("Zonas registradas en la base de datos")
if len(zonas)>=1:
    for z in zonas:
        print("Region: {}\t id: {}".format(z[1], z[0]))
        ids.append(z[0])

    id = input("\nIngrese el id de la zona que desear eliminar:\t")
    id = int(id)

    while id not in ids:
        print("{} id no es correcto, vuelva a ingresarlo".format(id))
        id = input("Ingrese id de la zona que desea eliminar \t")
        id = int(id)

    # caracteristicas del espectro
    query1 = "SELECT id FROM radioastronomia_espectro WHERE region_id = %s;"
    cur.execute(query1,[id])
    ids_espectro = cur.fetchall()
    ids_espectro = tuple(map(lambda ids_espectro: ids_espectro[0], ids_espectro))

    query2 = "DELETE FROM radioastronomia_caracteristicasespectro WHERE espectro_id IN "+str(ids_espectro)+";"
    cur.execute(query2)
    print("Caracteristicas espectro eliminadas de la region {}...".format(id))

    query3 = "DELETE FROM radioastronomia_espectro WHERE id IN "+str(ids_espectro)+";"
    cur.execute(query3)
    print("Espectro eliminado de la region {}...".format(id))

    query4 = "DELETE FROM radioastronomia_albumimagenes WHERE region_id = %s;"
    cur.execute(query4, [id])
    print("Videos de la region {} han sido eliminados ...")

    query5 = "DELETE FROM radioastronomia_estacionambiental WHERE region_id = %s;"
    cur.execute(query5, [id])
    print("Datos de la estacion ambiental de la region {} han sido eliminados ...".format(id))

    query6 = "DELETE FROM radioastronomia_posicionantena WHERE region_id = %s;"
    cur.execute(query6, [id])
    print("Datos de la posicion de la antena han sido borrados ...")

    query7 = "DELETE FROM radioastronomia_regioncampana WHERE id = %s;"
    cur.execute(query7, [id])
    print("Finalizado... region {} ha sido borrada... 100%".format(id))

    conn.commit()
    conn.close()

else:
    print("No hay zonas ni datos registrados en la plataforma ...")