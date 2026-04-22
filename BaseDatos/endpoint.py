from fastapi import FastAPI, Response

from Estadistica_Y_Graficas.estadisticas import (
    rendimiento_vs_media_posicion, ranking_goleadores,
    estadisticas_por_equipo, eficiencia_goleadora,
    distribucion_salarial_por_cargo, ranking_salarial,
    comparativa_salario_real_vs_base, antiguedad_media_por_cargo,
    distribucion_empleados_por_cargo,
    ranking_cantantes_por_actividad, distribucion_conciertos_por_continente,
    recintos_mas_demandados, ocupacion_media_por_cantante, rentabilidad_por_gira,
    rentabilidad_peliculas, generos_mas_rentables,
    directores_mas_taquilleros, peliculas_mayor_perdida, impacto_actores_en_recaudacion
)


from Estadistica_Y_Graficas.graficas import (
    grafico_rendimiento_posicion, grafico_ranking_goleadores,
    grafico_estadisticas_por_equipo, grafico_eficiencia_goleadora,
    grafico_distribucion_salarial, grafico_ranking_salarios,
    grafico_comparativa_vs_base, grafico_antiguedad_por_cargo,
    grafico_distribucion_empleados,
    grafico_ranking_cantantes, grafico_distribucion_por_continente,
    grafico_recintos_mas_demandados, grafico_ocupacion_por_cantante,
    grafico_rentabilidad_giras,
    grafico_rentabilidad_peliculas, grafico_generos_rentables,
    grafico_directores_taquilleros, grafico_peliculas_mayor_perdida,
    grafico_impacto_actores
)

app = FastAPI(title="PyBusiness Analytics API")

# FÚTBOL

@app.get("/futbol/rendimiento")
def get_rendimiento():
    return rendimiento_vs_media_posicion()

@app.get("/futbol/rendimiento/grafico")
def get_grafico_rendimiento():
    datos = rendimiento_vs_media_posicion()
    return Response(content=grafico_rendimiento_posicion(datos), media_type="image/png")

@app.get("/futbol/goleadores")
def get_goleadores():
    return ranking_goleadores()

@app.get("/futbol/goleadores/grafico")
def get_grafico_goleadores():
    datos = ranking_goleadores()
    return Response(content=grafico_ranking_goleadores(datos), media_type="image/png")

@app.get("/futbol/equipos")
def get_equipos():
    return estadisticas_por_equipo()

@app.get("/futbol/equipos/grafico")
def get_grafico_equipos():
    datos = estadisticas_por_equipo()
    return Response(content=grafico_estadisticas_por_equipo(datos), media_type="image/png")

@app.get("/futbol/eficiencia")
def get_eficiencia():
    return eficiencia_goleadora()

@app.get("/futbol/eficiencia/grafico")
def get_grafico_eficiencia():
    datos = eficiencia_goleadora()
    return Response(content=grafico_eficiencia_goleadora(datos), media_type="image/png")

# EMPLEADOS

@app.get("/empleados/distribucion")
def get_distribucion():
    return distribucion_salarial_por_cargo()

@app.get("/empleados/distribucion/grafico")
def get_grafico_distribucion():
    datos = distribucion_salarial_por_cargo()
    return Response(content=grafico_distribucion_salarial(datos), media_type="image/png")

@app.get("/empleados/ranking-salarial")
def get_ranking_salarial():
    return ranking_salarial()

@app.get("/empleados/ranking-salarial/grafico")
def get_grafico_ranking_salarial():
    datos = ranking_salarial()
    return Response(content=grafico_ranking_salarios(datos), media_type="image/png")

@app.get("/empleados/comparativa-base")
def get_comparativa():
    return comparativa_salario_real_vs_base()

@app.get("/empleados/comparativa-base/grafico")
def get_grafico_comparativa():
    datos = comparativa_salario_real_vs_base()
    return Response(content=grafico_comparativa_vs_base(datos), media_type="image/png")

@app.get("/empleados/antiguedad")
def get_antiguedad():
    return antiguedad_media_por_cargo()

@app.get("/empleados/antiguedad/grafico")
def get_grafico_antiguedad():
    datos = antiguedad_media_por_cargo()
    return Response(content=grafico_antiguedad_por_cargo(datos), media_type="image/png")

@app.get("/empleados/estructura-plantilla")
def get_estructura():
    return distribucion_empleados_por_cargo()

@app.get("/empleados/estructura-plantilla/grafico")
def get_grafico_estructura():
    datos = distribucion_empleados_por_cargo()
    return Response(content=grafico_distribucion_empleados(datos), media_type="image/png")

# CONCIERTOS

@app.get("/conciertos/actividad")
def get_actividad_cantantes():
    return ranking_cantantes_por_actividad()

@app.get("/conciertos/actividad/grafico")
def get_grafico_actividad():
    datos = ranking_cantantes_por_actividad()
    return Response(content=grafico_ranking_cantantes(datos), media_type="image/png")

@app.get("/conciertos/continentes")
def get_conciertos_continente():
    return distribucion_conciertos_por_continente()

@app.get("/conciertos/continentes/grafico")
def get_grafico_continentes():
    datos = distribucion_conciertos_por_continente()
    return Response(content=grafico_distribucion_por_continente(datos), media_type="image/png")

@app.get("/conciertos/recintos-top")
def get_recintos():
    return recintos_mas_demandados()

@app.get("/conciertos/recintos-top/grafico")
def get_grafico_recintos():
    datos = recintos_mas_demandados()
    return Response(content=grafico_recintos_mas_demandados(datos), media_type="image/png")

@app.get("/conciertos/ocupacion")
def get_ocupacion():
    return ocupacion_media_por_cantante()

@app.get("/conciertos/ocupacion/grafico")
def get_grafico_ocupacion():
    datos = ocupacion_media_por_cantante()
    return Response(content=grafico_ocupacion_por_cantante(datos), media_type="image/png")

@app.get("/conciertos/rentabilidad-giras")
def get_rentabilidad_giras():
    return rentabilidad_por_gira()

@app.get("/conciertos/rentabilidad-giras/grafico")
def get_grafico_rentabilidad_giras():
    datos = rentabilidad_por_gira()
    return Response(content=grafico_rentabilidad_giras(datos), media_type="image/png")

# PELÍCULAS

@app.get("/peliculas/rentabilidad")
def get_rentabilidad():
    return rentabilidad_peliculas()

@app.get("/peliculas/rentabilidad/grafico")
def get_grafico_rentabilidad_pelis():
    datos = rentabilidad_peliculas()
    return Response(content=grafico_rentabilidad_peliculas(datos), media_type="image/png")

@app.get("/peliculas/generos")
def get_generos():
    return generos_mas_rentables()

@app.get("/peliculas/generos/grafico")
def get_grafico_generos():
    datos = generos_mas_rentables()
    return Response(content=grafico_generos_rentables(datos), media_type="image/png")

@app.get("/peliculas/directores")
def get_directores():
    return directores_mas_taquilleros()

@app.get("/peliculas/directores/grafico")
def get_grafico_directores():
    datos = directores_mas_taquilleros()
    return Response(content=grafico_directores_taquilleros(datos), media_type="image/png")

@app.get("/peliculas/perdidas")
def get_perdidas():
    return peliculas_mayor_perdida()

@app.get("/peliculas/perdidas/grafico")
def get_grafico_perdidas():
    datos = peliculas_mayor_perdida()
    return Response(content=grafico_peliculas_mayor_perdida(datos), media_type="image/png")

@app.get("/peliculas/impacto-actores")
def get_actores():
    return impacto_actores_en_recaudacion()

@app.get("/peliculas/impacto-actores/grafico")
def get_grafico_actores():
    datos = impacto_actores_en_recaudacion()
    return Response(content=grafico_impacto_actores(datos), media_type="image/png")