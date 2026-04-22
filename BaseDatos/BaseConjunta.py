from sqlalchemy import create_engine, text


# Crear base de datos combinada
engine = create_engine("sqlite:///baseConjunta.db")

with engine.connect() as conn:


    conn.execute(text("PRAGMA foreign_keys = ON"))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Administrador (
        id_admi INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        contrasena TEXT
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Usuario (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        id_admi INTEGER,
        usuario TEXT,
        contrasena TEXT,
        FOREIGN KEY (id_admi) REFERENCES Administrador(id_admi)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Futbol (
        id_jugador INTEGER PRIMARY KEY AUTOINCREMENT,
        equipo TEXT,
        jugador TEXT,
        posicion TEXT,
        partidos_jugados INTEGER,
        asistencias INTEGER,
        goles INTEGER,
        tarjetas_amarillas INTEGER,
        tarjetas_rojas INTEGER,
        id_admin INTEGER,
        FOREIGN KEY (id_admin) REFERENCES Administrador(id_admi)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Empleados (
        id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado TEXT,
        departamento TEXT,
        cargo TEXT,
        salario_base INTEGER,
        salario_real INTEGER,
        fecha_contratacion DATE,
        id_admin INTEGER,
        FOREIGN KEY (id_admin) REFERENCES Administrador(id_admi)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Conciertos (
        id_concierto INTEGER PRIMARY KEY AUTOINCREMENT,
        cantante TEXT,
        nacionalidad TEXT,
        fecha_nac DATE,
        concierto TEXT,
        num_canciones INTEGER,
        duracion INTEGER,
        recinto TEXT,
        pais TEXT,
        continente TEXT,
        max_entradas INTEGER,
        entradas_vendidas INTEGER,
        id_admin INTEGER,
        FOREIGN KEY (id_admin) REFERENCES Administrador(id_admi)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Cine (
        id_pelicula INTEGER PRIMARY KEY AUTOINCREMENT,
        pelicula TEXT,
        genero TEXT,
        duracion INTEGER,
        presupuesto INTEGER,
        recaudacion INTEGER,
        director TEXT,
        fecha_nac_director DATE,
        actor_protagonista TEXT,
        fecha_nac_prota DATE,
        id_admin INTEGER,
        FOREIGN KEY (id_admin) REFERENCES Administrador(id_admi)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """))



#--------------------------DATOS DE PRUEBA--------------------------------------------------------------------------------------------
    conn.execute(text("""
    INSERT OR IGNORE INTO Administrador (usuario, contrasena)
    VALUES ('ADMINISTRADOR','1234ASDF')"""))

    conn.execute(text("""
    INSERT INTO Conciertos 
    (cantante, nacionalidad, fecha_nac, concierto, num_canciones, duracion, recinto, pais, continente, max_entradas, entradas_vendidas, id_admin)
    VALUES
    ('Taylor Swift','Estadounidense','1989-12-13','The Eras Tour: Dublin N1',44,180,'Aviva Stadium','Irlanda','Europa',52000,52000,1),
    ('Taylor Swift','Estadounidense','1989-12-13','The Eras Tour: Dublin N2',44,180,'Aviva Stadium','Irlanda','Europa',52000,52000,1),
    ('Taylor Swift','Estadounidense','1989-12-13','The Eras Tour: Dublin N3',44,180,'Aviva Stadium','Irlanda','Europa',52000,52000,1),
    ('Harry Styles','Británica','1994-02-01','Love On Tour: London N6',25,120,'Wembley Stadium','UK','Europa',90000,90000,1),
    ('Dua Lipa','Británica','1995-08-22','Radical Optimism Tour: Singapore N4',24,105,'Indoor Stadium','Singapur','Asia',12000,12000,1),
    ('Ariana Grande','Estadounidense','1993-06-26','Sweetener World Tour: London N5',28,115,'The O2 Arena','UK','Europa',20000,20000,1),
    ('Olivia Rodrigo','Estadounidense','2003-02-20','GUTS World Tour: Dublin N2',22,95,'3Arena','Irlanda','Europa',13000,13000,1),
    ('Lady Gaga','Estadounidense','1986-03-28','The Chromatica Ball: Miami N3',20,110,'Hard Rock Stadium','USA','Norteamérica',65000,65000,1),
    ('Imagine Dragons','Estadounidense','2008-06-15','Mercury World Tour: Lyon N3',26,130,'Groupama Stadium','Francia','Europa',59000,59000,1),
    ('Twenty One Pilots','Estadounidense','2009-12-29','Clancy World Tour: Hamburg N2',24,120,'Barclays Arena','Alemania','Europa',15000,15000,1),
    ('Sabrina Carpenter','Estadounidense','1999-05-11','Short n'' Sweet Tour: Amsterdam N4',23,100,'Ziggo Dome','Países Bajos','Europa',17000,17000,1),
    ('Conan Gray','Estadounidense','1998-12-05','Found Heaven On Tour: Tokyo N3',21,100,'Garden Theatre','Japón','Asia',8000,8000,1),
    ('Troye Sivan','Australiana','1995-06-05','Something to Give Each Other Tour: Paris N4',19,90,'Zénith Paris','Francia','Europa',6800,6800,1),
    ('Alec Benjamin','Estadounidense','1994-05-28','12 Notes Tour: London N6',20,90,'Eventim Apollo','UK','Europa',5000,5000,1)
    """))

    conn.execute(text("""
    INSERT INTO Empleados
    (empleado, departamento, cargo, salario_base, salario_real, fecha_contratacion, id_admin)
    VALUES
    ('Durant Chalker','Engineering','Gerente',3661.55,4112.55,'2005-12-05',1),
    ('Antonia Gledhill','Research and Development','soporte',1392.37,2336.37,'2022-08-06',1),
    ('Octavia Arniz','Engineering','analista',1862.03,2207.03,'2020-08-18',1),
    ('Dorisa Dunham','Training','Gerente',2538.83,3479.83,'2004-11-25',1),
    ('Eden Barnhart','Legal','analista',2167.64,2978.64,'2004-12-13',1),
    ('Nobie Tomashov','Training','soporte',4311.48,4902.48,'2012-10-09',1),
    ('Emmy Holston','Business Development','comercial',1646.74,1923.74,'2018-09-25',1),
    ('Nollie Fidal','Business Development','analista',3659.52,4601.52,'2006-07-31',1),
    ('Kim Southwick','Accounting','desarrollador',4765.38,5313.38,'2020-04-04',1),
    ('Valerye Ditchfield','Support','desarrollador',1070.06,1923.06,'2022-07-18',1),
    ('Chalmers MacLachlan','Engineering','comercial',4422.1,4564.1,'2012-05-15',1),
    ('Augie Ledgister','Research and Development','desarrollador',4875.1,5653.1,'2018-08-02',1),
    ('Cyndy Barter','Legal','soporte',4231.25,4787.25,'2021-12-13',1),
    ('Sherill Linklet','Marketing','soporte',1858.57,2752.57,'2009-02-17',1)
    """))

#--------------------------------------------------------------------------------------------------------------------------------------
    conn.commit()
    print("Base de datos creada")

