from sqlalchemy import create_engine, text
from datetime import date
import random


# Crear base de datos combinada
engine = create_engine("sqlite:///baseDatos.db")

with engine.connect() as conn:

    # Activar claves foráneas
    conn.execute(text("PRAGMA foreign_keys = ON"))

    # TABLAS DE EMPRESA
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Cargo (
        id_cargo INTEGER PRIMARY KEY,
        nombre_cargo TEXT,
        salario_base INTEGER
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Empleado (
        id_empleado INTEGER PRIMARY KEY,
        nombre TEXT,
        apellido TEXT,
        fecha_contratacion DATE,
        id_cargo INTEGER,
        FOREIGN KEY (id_cargo) REFERENCES Cargo(id_cargo)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS SalarioEmpleado (
        id INTEGER PRIMARY KEY,
        id_empleado INTEGER,
        salario_real INTEGER,
        fecha DATE,
        FOREIGN KEY (id_empleado) REFERENCES Empleado(id_empleado)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    # TABLAS DE FUTBOL
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Temporada (
        id_temporada INTEGER PRIMARY KEY,
        anio_inicio INTEGER,
        anio_fin INTEGER
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Equipo (
        id_equipo INTEGER PRIMARY KEY,
        nombre TEXT,
        ciudad TEXT,
        estadio TEXT
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Jugador (
        id_jugador INTEGER PRIMARY KEY,
        nombre TEXT,
        fecha_nacimiento DATE,
        nacionalidad TEXT,
        posicion TEXT
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS EstadisticasJugador (
        id INTEGER PRIMARY KEY,
        id_jugador INTEGER,
        id_equipo INTEGER,
        id_temporada INTEGER,
        partidos_jugados INTEGER,
        goles INTEGER,
        asistencias INTEGER,
        tarjetas_amarillas INTEGER,
        tarjetas_rojas INTEGER,
        FOREIGN KEY (id_jugador) REFERENCES Jugador(id_jugador)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (id_temporada) REFERENCES Temporada(id_temporada)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    # TABLAS DE CONCIERTOS
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Pais (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        continente TEXT
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Cantante (
        id_cantante INTEGER PRIMARY KEY,
        nombre TEXT,
        id_pais_nacimiento INTEGER,
        fecha_nac DATE,
        FOREIGN KEY (id_pais_nacimiento) REFERENCES Pais(id)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Gira (
        id_gira INTEGER PRIMARY KEY,
        nombre_gira TEXT,
        id_cantante INTEGER,
        num_canciones INTEGER,
        duracion INTEGER,
        FOREIGN KEY (id_cantante) REFERENCES Cantante(id_cantante)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Recinto (
        id_recinto INTEGER PRIMARY KEY,
        nombre TEXT,
        id_pais INTEGER,
        FOREIGN KEY (id_pais) REFERENCES Pais(id)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Conciertos (
        id_concierto INTEGER PRIMARY KEY,
        id_gira INTEGER,
        id_cantante INTEGER,
        id_recinto INTEGER,
        FOREIGN KEY (id_gira) REFERENCES Gira(id_gira)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (id_cantante) REFERENCES Cantante(id_cantante)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (id_recinto) REFERENCES Recinto(id_recinto)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    # TABLAS DE CINE
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Persona (
        id_persona INTEGER PRIMARY KEY,
        nombre TEXT,
        nacionalidad TEXT,
        fecha_nacimiento DATE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Actor (
        id_persona INTEGER PRIMARY KEY,
        FOREIGN KEY (id_persona) REFERENCES Persona(id_persona)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Director (
        id_persona INTEGER PRIMARY KEY,
        FOREIGN KEY (id_persona) REFERENCES Persona(id_persona)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Pelicula (
        id_pelicula INTEGER PRIMARY KEY,
        titulo TEXT,
        duracion INTEGER,
        recaudacion INTEGER,
        presupuesto INTEGER
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Genero (
        id_genero INTEGER PRIMARY KEY,
        nombre TEXT
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Reparto (
        id_pelicula INTEGER,
        id_persona INTEGER,
        personaje TEXT,
        PRIMARY KEY (id_pelicula, id_persona),
        FOREIGN KEY (id_pelicula) REFERENCES Pelicula(id_pelicula)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (id_persona) REFERENCES Actor(id_persona)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Pelicula_Genero (
        id_pelicula INTEGER,
        id_genero INTEGER,
        PRIMARY KEY (id_pelicula, id_genero),
        FOREIGN KEY (id_pelicula) REFERENCES Pelicula(id_pelicula)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (id_genero) REFERENCES Genero(id_genero)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Pelicula_Director (
        id_pelicula INTEGER,
        id_persona INTEGER,
        PRIMARY KEY (id_pelicula, id_persona),
        FOREIGN KEY (id_pelicula) REFERENCES Pelicula(id_pelicula)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (id_persona) REFERENCES Director(id_persona)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    # INSERTAR DATOS DE EMPRESA
    cargos = [
        (1, "Gerente", 5000),
        (2, "Analista", 3000),
        (3, "Desarrollador", 3500),
        (4, "Diseñador", 2800),
        (5, "Soporte", 2500)
    ]
    for c in cargos:
        conn.execute(text("""
        INSERT OR IGNORE INTO Cargo (id_cargo, nombre_cargo, salario_base)
        VALUES (:id, :nombre, :salario)
        """), {"id": c[0], "nombre": c[1], "salario": c[2]})

    nombres_emp = ["Juan","Ana","Luis","Marta","Carlos","Lucia","Pedro","Sofia","Jorge","Elena",
                   "Raul","Carmen","Diego","Laura","Andres","Paula","Fernando","Sara","Miguel","Claudia"]
    apellidos_emp = ["Gomez","Perez","Lopez","Martinez","Sanchez","Ramirez","Torres","Flores",
                     "Vargas","Castro","Ortega","Rojas","Navarro","Molina","Delgado","Suarez",
                     "Morales","Romero","Herrera","Medina"]
    for i in range(20):
        id_emp = i+1
        nombre = nombres_emp[i]
        apellido = apellidos_emp[i]
        fecha = f"2020-{(i%12)+1:02d}-15"
        id_cargo = random.randint(1,5)

        conn.execute(text("""
        INSERT OR IGNORE INTO Empleado (id_empleado, nombre, apellido, fecha_contratacion, id_cargo)
        VALUES (:id, :nombre, :apellido, :fecha, :cargo)
        """), {"id": id_emp, "nombre": nombre, "apellido": apellido, "fecha": fecha, "cargo": id_cargo})

        salario_base = next(c[2] for c in cargos if c[0] == id_cargo)
        salario_real = salario_base + random.randint(-500, 1000)

        conn.execute(text("""
        INSERT OR IGNORE INTO SalarioEmpleado (id, id_empleado, salario_real, fecha)
        VALUES (:id, :id_emp, :salario, :fecha)
        """), {"id": id_emp, "id_emp": id_emp, "salario": salario_real, "fecha": date.today()})

    import random
    from sqlalchemy import text

    # Datos de ejemplo
    temporadas = [(1, 2022, 2023), (2, 2023, 2024), (3, 2024, 2025)]
    for t in temporadas:
        conn.execute(text("INSERT OR IGNORE INTO Temporada VALUES (:id, :inicio, :fin)"),
                     {"id": t[0], "inicio": t[1], "fin": t[2]})

    equipos = [
        (1, "Real Madrid", "Madrid", "Santiago Bernabéu"),
        (2, "Barcelona", "Barcelona", "Camp Nou"),
        (3, "Atletico Madrid", "Madrid", "Metropolitano"),
        (4, "Sevilla", "Sevilla", "Ramón Sánchez-Pizjuán"),
        (5, "Valencia", "Valencia", "Mestalla")
    ]
    for e in equipos:
        conn.execute(text("INSERT OR IGNORE INTO Equipo VALUES (:id, :nombre, :ciudad, :estadio)"),
                     {"id": e[0], "nombre": e[1], "ciudad": e[2], "estadio": e[3]})

    nombres_jug = [
        "Juan Perez", "Carlos Lopez", "Luis Garcia", "Pedro Sanchez", "Miguel Torres",
        "Andres Gomez", "Javier Ruiz", "Fernando Diaz", "Sergio Ramos", "Alberto Castro",
        "Diego Herrera", "Pablo Medina", "Raul Ortega", "Mario Navarro", "David Molina",
        "Jose Delgado", "Victor Suarez", "Adrian Morales", "Ivan Romero", "Hugo Vargas"
    ]
    posiciones = ["Delantero", "Centrocampista", "Defensa", "Portero"]

    for i in range(20):
        pos = random.choice(posiciones)
        conn.execute(text("""
            INSERT OR IGNORE INTO Jugador VALUES (:id, :nombre, :fecha, :nacionalidad, :posicion)
        """), {
            "id": i + 1,
            "nombre": nombres_jug[i],
            "fecha": f"199{random.randint(0, 9)}-0{random.randint(1, 9)}-15",
            "nacionalidad": "España",
            "posicion": pos
        })

        # Estadísticas realistas según posición
        if pos == "Portero":
            goles = 0
            asis = random.randint(0, 2)
        elif pos == "Defensa":
            goles = random.randint(0, 5)
            asis = random.randint(0, 5)
        elif pos == "Centrocampista":
            goles = random.randint(0, 15)
            asis = random.randint(0, 15)
        else:  # Delantero
            goles = random.randint(5, 25)
            asis = random.randint(2, 15)

        conn.execute(text("""
            INSERT OR IGNORE INTO EstadisticasJugador VALUES (:id, :jugador, :equipo, :temporada, :pj, :goles, :asis, :ta, :tr)
        """), {
            "id": i + 1,
            "jugador": i + 1,
            "equipo": random.randint(1, 5),
            "temporada": random.randint(1, 3),
            "pj": random.randint(10, 38),
            "goles": goles,
            "asis": asis,
            "ta": random.randint(0, 10),
            "tr": random.randint(0, 3)
        })

    # INSERTAR DATOS DE CONCIERTOS
    paises = [
        (1, "Estados Unidos", "América"),
        (2, "Reino Unido", "Europa")
    ]
    for p in paises:
        conn.execute(text("""
        INSERT OR IGNORE INTO Pais (id, nombre, continente)
        VALUES (:id, :nombre, :continente)
        """), {"id": p[0], "nombre": p[1], "continente": p[2]})

    cantantes = [
        (1, "Taylor Swift", 1, "1989-12-13"),
        (2, "Lady Gaga", 1, "1986-03-28"),
        (3, "Ariana Grande", 1, "1993-06-26"),
        (4, "Harry Styles", 2, "1994-02-01"),
        (5, "Conan Gray", 1, "1998-07-06")
    ]
    for c in cantantes:
        conn.execute(text("""
        INSERT OR IGNORE INTO Cantante (id_cantante, nombre, id_pais_nacimiento, fecha_nac)
        VALUES (:id, :nombre, :pais, :fecha)
        """), {"id": c[0], "nombre": c[1], "pais": c[2], "fecha": c[3]})

    giras = [
        # Taylor Swift
        (1, 'Fearless Tour', 1, 20, 120),
        (2, 'Speak Now World Tour', 1, 22, 130),
        (3, 'Red Tour', 1, 23, 140),
        (4, 'The 1989 World Tour', 1, 25, 150),
        (5, 'Reputation Stadium Tour', 1, 24, 145),
        (6, 'The Eras Tour', 1, 30, 180),
        # Ariana Grande
        (7, 'The Honeymoon Tour', 3, 18, 100),
        (8, 'Dangerous Woman Tour', 3, 19, 105),
        (9, 'Sweetener World Tour', 3, 22, 125),
        (10, 'The Eternal Sunshine Tour', 3, 24, 130),
        # Harry Styles
        (11, 'Harry Styles: Live on Tour', 4, 20, 115),
        (12, 'Love On Tour', 4, 26, 150),
        # Lady Gaga
        (13, 'The Fame Ball Tour', 2, 15, 90),
        (14, 'The Monster Ball Tour', 2, 25, 140),
        (15, 'Born This Way Ball Tour', 2, 28, 150),
        (16, 'artRAVE: The ARTPOP Ball Tour', 2, 20, 110),
        (17, 'Joanne World Tour', 2, 22, 120),
        (18, 'The Chromatica Ball', 2, 18, 100),
        (19, 'The Mayhem Ball', 2, 30, 180),
        # Conan Gray
        (20, 'The Magician Tour', 5, 18, 110)
    ]
    for g in giras:
        conn.execute(text("""
        INSERT OR IGNORE INTO Gira (id_gira, nombre_gira, id_cantante, num_canciones, duracion)
        VALUES (:id, :nombre, :cantante, :num, :dur)
        """), {"id": g[0], "nombre": g[1], "cantante": g[2], "num": g[3], "dur": g[4]})

    recintos = [
        (1, 'Madison Square Garden', 1),
        (2, 'Staples Center', 1),
        (3, 'Wembley Stadium', 2),
        (4, 'O2 Arena', 2),
        (5, 'Hollywood Bowl', 1),
        (6, 'Barclaycard Arena', 2),
        (7, 'Roberts Stadium', 1),
        (8, 'ASU Convocation Center', 1),
        (9, 'Scottrade Center', 1),
        (10, 'Event Center', 1),
        (11, 'BMO Harris Bradley Center', 1),
        (12, 'Xcel Energy Center', 1),
        (13, 'Merkur Spiel-Arena', 2),
        (14, 'PGE Narodowy', 2),
        (15, 'Deutsche Bank Park', 2),
        (16, 'T-Mobile Arena', 1),
        (17, 'Scotiabank Arena', 1),
        (18, 'United Center', 1)
    ]
    for r in recintos:
        conn.execute(text("""
        INSERT OR IGNORE INTO Recinto (id_recinto, nombre, id_pais)
        VALUES (:id, :nombre, :pais)
        """), {"id": r[0], "nombre": r[1], "pais": r[2]})

    conciertos = [
        # Taylor Swift
        (1001, 1, 1, 7), (1002, 1, 1, 8), (1003, 1, 1, 9), (1004, 2, 1, 1),
        (1005, 2, 1, 2), (1006, 2, 1, 5), (1007, 3, 1, 1), (1008, 3, 1, 10),
        (1009, 3, 1, 11), (1010, 4, 1, 1), (1011, 4, 1, 12), (1012, 4, 1, 5),
        (1013, 5, 1, 1), (1014, 5, 1, 2), (1015, 5, 1, 9), (1016, 6, 1, 1),
        (1017, 6, 1, 12), (1018, 6, 1, 5),
        # Ariana Grande
        (2001, 7, 3, 10), (2002, 7, 3, 11), (2003, 7, 3, 12), (2004, 8, 3, 1),
        (2005, 8, 3, 2), (2006, 8, 3, 5), (2007, 9, 3, 1), (2008, 9, 3, 10),
        (2009, 9, 3, 11), (2010, 10, 3, 10), (2011, 10, 3, 12), (2012, 10, 3, 1),
        # Harry Styles
        (3001, 11, 4, 13), (3002, 11, 4, 14), (3003, 11, 4, 15),
        (3004, 12, 4, 13), (3005, 12, 4, 4), (3006, 12, 4, 6),
        # Lady Gaga
        (4001, 13, 2, 1), (4002, 13, 2, 2), (4003, 13, 2, 5), (4004, 14, 2, 1),
        (4005, 14, 2, 2), (4006, 14, 2, 5), (4007, 15, 2, 1), (4008, 15, 2, 10),
        (4009, 15, 2, 11), (4010, 16, 2, 1), (4011, 16, 2, 2), (4012, 16, 2, 5),
        (4013, 17, 2, 1), (4014, 17, 2, 2), (4015, 17, 2, 5), (4016, 18, 2, 1),
        (4017, 18, 2, 2), (4018, 18, 2, 5), (4019, 19, 2, 16), (4020, 19, 2, 17),
        (4021, 19, 2, 18),
        # Conan Gray
        (5001, 20, 5, 5), (5002, 20, 5, 1), (5003, 20, 5, 2)
    ]
    for c in conciertos:
        conn.execute(text("""
        INSERT OR IGNORE INTO Conciertos (id_concierto, id_gira, id_cantante, id_recinto)
        VALUES (:id, :gira, :cantante, :recinto)
        """), {"id": c[0], "gira": c[1], "cantante": c[2], "recinto": c[3]})

    conn.commit()
    print("Base de datos creada")