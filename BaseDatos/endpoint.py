from fastapi import FastAPI, Response, HTTPException, UploadFile, File, Depends
from sqlalchemy import text
import hashlib

from Estadistica_Y_Graficas.estadisticas import *
from Estadistica_Y_Graficas.graficas import *
from Estadistica_Y_Graficas.importar import *
from BaseDatos import engine


app = FastAPI(title="PyBusiness Analytics API")

#OBTENER ADMINISTRADOR ACTUAL (FALTA POR IMPLEMENTAR)
def get_admin():
    return 1

#CREACION DE USUARIOS (ADMINISTRADOR Y BASE)
@app.post("/usuarios/crear-empleado")
def crear_usuario_admin(username: str, contraseña: str):
    contraseña_hash=hashlib.sha256(contraseña.encode()).hexdigest()

    try:
        with engine.connect() as conn:
            conn.execute(text("""
                    INSERT INTO Administrador (usuario, contrasena)
                    VALUES (:usuario, :contraseña)
                """), {
                "usuario": username,
                "contraseña": contraseña_hash
            })
            conn.commit()

        return {"msg": f"Nuevo administrador creado: {username}"}, 201

    except Exception as e:
            raise HTTPException(status_code=400, detail="Error: El usuario ya existe.")

@app.post("/usuarios/crear-empleado")
def crear_usuario(username: str, contraseña: str, id_admin: int = Depends(get_admin)):
    contraseña_hash=hashlib.sha256(contraseña.encode()).hexdigest()

    try:
        with engine.connect() as conn:
            conn.execute(text("""
                    INSERT INTO Usuario (id_admin, usuario, contrasena)
                    VALUES (:id_admin, :usuario, :contraseña)
                """), {
                "id_admin": id_admin,
                "usuario": username,
                "contraseña": contraseña_hash
            })
            conn.commit()

        return {"msg": f"Nuevo usuario creado: {username} por el administrador: {id_admin}"}

    except Exception as e:
            raise HTTPException(status_code=400, detail="Error: El usuario ya existe.")

#SUBIR ARCHIVOS
@app.post("/subir-archivo")
async def importar_ficheros(file: UploadFile = File(...),
    id_admin: int = Depends(get_admin)):
    try:
        contenido = await file.read()

        df = importar_fichero(file.filename, contenido)

        columnas = [c.lower() for c in df.columns]
        if 'goles' in columnas or 'posicion' in columnas:
            tabla = "Futbol"
        elif 'salario_base' in columnas or 'fecha_contratacion' in columnas:
            tabla = "Empleados"
        elif 'entradas_vendidas' in columnas or 'recinto' in columnas:
            tabla = "Conciertos"
        elif 'recaudacion' in columnas or 'director' in columnas:
            tabla = "Cine"
        else:
            raise ValueError("La estructura del archivo no coincide con ninguna tabla conocida.")

        df['id_admin'] = id_admin

        df.to_sql(tabla, con=engine, if_exists="append", index=False)

        return {
            "nombre_archivo": file.filename,
            "num_filas": len(df),
            "columnas": df.columns,
            "datos": df.to_dict(orient="records")
        }


    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





# FÚTBOL
@app.get("/futbol/rendimiento")
def get_rendimiento(id_admin: int = Depends(get_admin)):
    return rendimiento_vs_media_posicion(id_admin)

@app.get("/futbol/rendimiento/grafico")
def get_grafico_rendimiento(id_admin: int = Depends(get_admin)):
    datos = rendimiento_vs_media_posicion(id_admin)
    return Response(content=grafico_rendimiento_posicion(datos), media_type="image/png")

@app.get("/futbol/goleadores")
def get_goleadores(id_admin: int = Depends(get_admin)):
    return ranking_goleadores(id_admin)

@app.get("/futbol/goleadores/grafico")
def get_grafico_goleadores(id_admin: int = Depends(get_admin)):
    datos = ranking_goleadores(id_admin)
    return Response(content=grafico_ranking_goleadores(datos), media_type="image/png")

@app.get("/futbol/equipos")
def get_equipos(id_admin: int = Depends(get_admin)):
    return estadisticas_por_equipo(id_admin)

@app.get("/futbol/equipos/grafico")
def get_grafico_equipos(id_admin: int = Depends(get_admin)):
    datos = estadisticas_por_equipo(id_admin)
    return Response(content=grafico_estadisticas_por_equipo(datos), media_type="image/png")

@app.get("/futbol/eficiencia")
def get_eficiencia(id_admin: int = Depends(get_admin)):
    return eficiencia_goleadora(id_admin)

@app.get("/futbol/eficiencia/grafico")
def get_grafico_eficiencia(id_admin: int = Depends(get_admin)):
    datos = eficiencia_goleadora(id_admin)
    return Response(content=grafico_eficiencia_goleadora(datos), media_type="image/png")

# EMPLEADOS
@app.get("/empleados/distribucion")
def get_distribucion(id_admin: int = Depends(get_admin)):
    return distribucion_salarial_por_cargo(id_admin)

@app.get("/empleados/distribucion/grafico")
def get_grafico_distribucion(id_admin: int = Depends(get_admin)):
    datos = distribucion_salarial_por_cargo(id_admin)
    return Response(content=grafico_distribucion_salarial(datos), media_type="image/png")

@app.get("/empleados/ranking-salarial")
def get_ranking_salarial(id_admin: int = Depends(get_admin)):
    return ranking_salarial(id_admin)

@app.get("/empleados/ranking-salarial/grafico")
def get_grafico_ranking_salarial(id_admin: int = Depends(get_admin)):
    datos = ranking_salarial(id_admin)
    return Response(content=grafico_ranking_salarios(datos), media_type="image/png")

@app.get("/empleados/comparativa-base")
def get_comparativa(id_admin: int = Depends(get_admin)):
    return comparativa_salario_real_vs_base(id_admin)

@app.get("/empleados/comparativa-base/grafico")
def get_grafico_comparativa(id_admin: int = Depends(get_admin)):
    datos = comparativa_salario_real_vs_base(id_admin)
    return Response(content=grafico_comparativa_vs_base(datos), media_type="image/png")

@app.get("/empleados/antiguedad")
def get_antiguedad(id_admin: int = Depends(get_admin)):
    return antiguedad_media_por_cargo(id_admin)

@app.get("/empleados/antiguedad/grafico")
def get_grafico_antiguedad(id_admin: int = Depends(get_admin)):
    datos = antiguedad_media_por_cargo(id_admin)
    return Response(content=grafico_antiguedad_por_cargo(datos), media_type="image/png")

@app.get("/empleados/estructura-plantilla")
def get_estructura(id_admin: int = Depends(get_admin)):
    return distribucion_empleados_por_cargo(id_admin)

@app.get("/empleados/estructura-plantilla/grafico")
def get_grafico_estructura(id_admin: int = Depends(get_admin)):
    datos = distribucion_empleados_por_cargo(id_admin)
    return Response(content=grafico_distribucion_empleados(datos), media_type="image/png")

# CONCIERTOS
@app.get("/conciertos/actividad")
def get_actividad_cantantes(id_admin: int = Depends(get_admin)):
    return ranking_cantantes_por_actividad(id_admin)

@app.get("/conciertos/actividad/grafico")
def get_grafico_actividad(id_admin: int = Depends(get_admin)):
    datos = ranking_cantantes_por_actividad(id_admin)
    return Response(content=grafico_ranking_cantantes(datos), media_type="image/png")

@app.get("/conciertos/continentes")
def get_conciertos_continente(id_admin: int = Depends(get_admin)):
    return distribucion_conciertos_por_continente(id_admin)

@app.get("/conciertos/continentes/grafico")
def get_grafico_continentes(id_admin: int = Depends(get_admin)):
    datos = distribucion_conciertos_por_continente(id_admin)
    return Response(content=grafico_distribucion_por_continente(datos), media_type="image/png")

@app.get("/conciertos/recintos-top")
def get_recintos(id_admin: int = Depends(get_admin)):
    return recintos_mas_demandados(id_admin)

@app.get("/conciertos/recintos-top/grafico")
def get_grafico_recintos(id_admin: int = Depends(get_admin)):
    datos = recintos_mas_demandados(id_admin)
    return Response(content=grafico_recintos_mas_demandados(datos), media_type="image/png")

@app.get("/conciertos/ocupacion")
def get_ocupacion(id_admin: int = Depends(get_admin)):
    return ocupacion_media_por_cantante(id_admin)

@app.get("/conciertos/ocupacion/grafico")
def get_grafico_ocupacion(id_admin: int = Depends(get_admin)):
    datos = ocupacion_media_por_cantante(id_admin)
    return Response(content=grafico_ocupacion_por_cantante(datos), media_type="image/png")

@app.get("/conciertos/rentabilidad-giras")
def get_rentabilidad_giras(id_admin: int = Depends(get_admin)):
    return rentabilidad_por_gira(id_admin)

@app.get("/conciertos/rentabilidad-giras/grafico")
def get_grafico_rentabilidad_giras(id_admin: int = Depends(get_admin)):
    datos = rentabilidad_por_gira(id_admin)
    return Response(content=grafico_rentabilidad_giras(datos), media_type="image/png")

# PELÍCULAS
@app.get("/peliculas/rentabilidad")
def get_rentabilidad(id_admin: int = Depends(get_admin)):
    return rentabilidad_peliculas(id_admin)

@app.get("/peliculas/rentabilidad/grafico")
def get_grafico_rentabilidad_pelis(id_admin: int = Depends(get_admin)):
    datos = rentabilidad_peliculas(id_admin)
    return Response(content=grafico_rentabilidad_peliculas(datos), media_type="image/png")

@app.get("/peliculas/generos")
def get_generos(id_admin: int = Depends(get_admin)):
    return generos_mas_rentables(id_admin)

@app.get("/peliculas/generos/grafico")
def get_grafico_generos(id_admin: int = Depends(get_admin)):
    datos = generos_mas_rentables(id_admin)
    return Response(content=grafico_generos_rentables(datos), media_type="image/png")

@app.get("/peliculas/directores")
def get_directores(id_admin: int = Depends(get_admin)):
    return directores_mas_taquilleros(id_admin)

@app.get("/peliculas/directores/grafico")
def get_grafico_directores(id_admin: int = Depends(get_admin)):
    datos = directores_mas_taquilleros(id_admin)
    return Response(content=grafico_directores_taquilleros(datos), media_type="image/png")

@app.get("/peliculas/perdidas")
def get_perdidas(id_admin: int = Depends(get_admin)):
    return peliculas_mayor_perdida(id_admin)

@app.get("/peliculas/perdidas/grafico")
def get_grafico_perdidas(id_admin: int = Depends(get_admin)):
    datos = peliculas_mayor_perdida(id_admin)
    return Response(content=grafico_peliculas_mayor_perdida(datos), media_type="image/png")

@app.get("/peliculas/impacto-actores")
def get_actores(id_admin: int = Depends(get_admin)):
    return impacto_actores_en_recaudacion(id_admin)

@app.get("/peliculas/impacto-actores/grafico")
def get_grafico_actores(id_admin: int = Depends(get_admin)):
    datos = impacto_actores_en_recaudacion(id_admin)
    return Response(content=grafico_impacto_actores(datos), media_type="image/png")

