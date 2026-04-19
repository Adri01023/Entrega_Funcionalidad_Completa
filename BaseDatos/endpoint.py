from fastapi import FastAPI
from fastapi.responses import Response


from Estadistica_Y_Graficas.estadisticas import (
    rendimiento_vs_media_posicion,
    distribucion_salarial_por_cargo,
    ranking_salarial,
    comparativa_salario_real_vs_base
)

from Estadistica_Y_Graficas.graficas import (
    grafico_rendimiento_posicion,
    grafico_distribucion_salarial,
    grafico_ranking_salarios,
    grafico_comparativa_vs_base
)


app = FastAPI(title="PyBusiness Analytics API")

# FUTBOL
@app.get("/futbol/rendimiento")
def get_rendimiento():
    return rendimiento_vs_media_posicion()


@app.get("/futbol/grafico")
def get_grafico_futbol():
    datos = rendimiento_vs_media_posicion()
    imagen = grafico_rendimiento_posicion(datos)
    return Response(content=imagen, media_type="image/png")

# EMPLEADOS
@app.get("/empleados/distribucion")
def get_distribucion():
    return distribucion_salarial_por_cargo()


@app.get("/empleados/distribucion/grafico")
def get_grafico_distribucion():
    datos = distribucion_salarial_por_cargo()
    imagen = grafico_distribucion_salarial(datos)
    return Response(content=imagen, media_type="image/png")


@app.get("/empleados/ranking")
def get_ranking():
    return ranking_salarial()


@app.get("/empleados/ranking/grafico")
def get_grafico_ranking():
    datos = ranking_salarial()
    imagen = grafico_ranking_salarios(datos)
    return Response(content=imagen, media_type="image/png")


@app.get("/empleados/comparativa")
def get_comparativa():
    return comparativa_salario_real_vs_base()


@app.get("/empleados/comparativa/grafico")
def get_grafico_comparativa():
    datos = comparativa_salario_real_vs_base()
    imagen = grafico_comparativa_vs_base(datos)
    return Response(content=imagen, media_type="image/png")