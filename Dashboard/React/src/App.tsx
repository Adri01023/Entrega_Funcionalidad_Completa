import { useEffect, useState } from "react";
import "./App.css";
import "./dashboard.css";

//Dirección de nuestro endpoint que nos permite la conexión entre frontend y backend
const BASE_URL = "http://127.0.0.1:8000";

// http://localhost:8000/empleados/distribucion/grafico

// Array que contiene los graficos de prueba con sus url correspondientes
const graficos = [
  // Fútbol
  {
    nombre: "Rendimiento vs Media Posición",
    url: "/futbol/rendimiento/grafico",
  },
  { nombre: "Ranking Goleadores", url: "/futbol/goleadores/grafico" },
  { nombre: "Estadísticas por Equipo", url: "/futbol/equipos/grafico" },
  { nombre: "Eficiencia Goleadora", url: "/futbol/eficiencia/grafico" },

  // Empleados
  {
    nombre: "Distribución Salarial por Cargo",
    url: "/empleados/distribucion/grafico",
  },
  { nombre: "Ranking Salarial", url: "/empleados/ranking-salarial/grafico" },
  {
    nombre: "Comparativa Salario Real vs Base",
    url: "/empleados/comparativa-base/grafico",
  },
  {
    nombre: "Antigüedad Media por Cargo",
    url: "/empleados/antiguedad/grafico",
  },
  {
    nombre: "Estructura de Plantilla",
    url: "/empleados/estructura-plantilla/grafico",
  },

  // Conciertos
  {
    nombre: "Ranking Cantantes por Actividad",
    url: "/conciertos/actividad/grafico",
  },
  {
    nombre: "Distribución de Conciertos por Continente",
    url: "/conciertos/continentes/grafico",
  },
  {
    nombre: "Recintos Más Demandados",
    url: "/conciertos/recintos-top/grafico",
  },
  {
    nombre: "Ocupación Media por Cantante",
    url: "/conciertos/ocupacion/grafico",
  },
  {
    nombre: "Rentabilidad por Gira",
    url: "/conciertos/rentabilidad-giras/grafico",
  },

  // Películas
  { nombre: "Rentabilidad Películas", url: "/peliculas/rentabilidad/grafico" },
  { nombre: "Géneros Más Rentables", url: "/peliculas/generos/grafico" },
  {
    nombre: "Directores Más Taquilleros",
    url: "/peliculas/directores/grafico",
  },
  { nombre: "Películas con Mayor Pérdida", url: "/peliculas/perdidas/grafico" },
  {
    nombre: "Impacto Actores en Recaudación",
    url: "/peliculas/impacto-actores/grafico",
  },
];

//Estructura de dato que alberga el tipo de objeto a almacenar en el historial
type HistorialItem =
  | {
      type: "grafica";
      url: string;
      nombre: string;
      hora: string;
      count: number;
    }
  | {
      type: "csv";
      nombre: string;
      hora: string;
      lineas: number;
      columnas: number;
    };

//Función por defecto para que funcione la app en react
function App() {
  // Use states con valores por defectos
  // Estado para el gráfico actual, inicializado con el primer gráfico
  const [graficoActual, setGraficoActual] = useState(graficos[0].url);

  // Setea por defecto la sección dashboard (Inicio)
  const [seccion, setSeccion] = useState("dashboard");
  // Seteamos el modo noche por defecto
  const [modo, setModo] = useState("noche");
  // Se guarda el archivo csv que sube el usuario, inicializado a null
  const [archivo, setArchivo] = useState<File | null>(null);

  /* useState con persistencia a fichero JSON del historial */
  const [historial, setHistorial] = useState<HistorialItem[]>(() => {
    const saved = localStorage.getItem("historial");
    return saved ? JSON.parse(saved) : [];
  });

  // Última gráfica consultada que solo puede ser de tipo grafica o null
  const [ultimaGrafica, setUltimaGrafica] = useState<Extract<
    HistorialItem,
    { type: "grafica" }
  > | null>(null);

  //Use effect cuando cambie el historial
  useEffect(() => {
    // Filtra solo los elementos de tipo "grafica"
    const graficasHistorial = historial.filter(
      (item): item is Extract<HistorialItem, { type: "grafica" }> =>
        item.type === "grafica",
    );

    if (graficasHistorial.length > 0) {
      setUltimaGrafica(graficasHistorial[graficasHistorial.length - 1]);
    } else {
      setUltimaGrafica(null);
    }
  }, [historial]);

  /* Evento que maneja el cambio de modo de los estilos entre modo día y noche */
  useEffect(() => {
    document.body.setAttribute("data-mode", modo);
  }, [modo]);

  /* Persistencia automática en localStorage */
  useEffect(() => {
    localStorage.setItem("historial", JSON.stringify(historial));
  }, [historial]);

  /* Registrar gráfica en el historial */
  const registrarGrafica = (url: string) => {
    // Busca el gráfico en la lista de gráficos disponibles
    const grafica = graficos.find((g) => g.url === url);
    if (!grafica) return; //condicion de salida si grafica vacia

    const hora = new Date().toLocaleString(); //guardamos como string la fecha

    // Prev estado previo del historial
    setHistorial((prev) => {
      // Se busca si existe en el historial la gráfica con la misma url
      const existe = prev.find((h) => h.type === "grafica" && h.url === url);

      //Si existe se aumenta el contador
      if (existe && existe.type === "grafica") {
        return prev.map((h) =>
          //Operador ternario, si condicion falsa se devuelve el mismo objeto,
          // Si condicion verdadera, se devuelve el mismo objeto actualizando fecha y total+1
          h.type === "grafica" && h.url === url
            ? { ...h, count: h.count + 1, hora }
            : h,
        );
      }

      //En caso de no existir se devuelve un nuevo objeto al historial
      return [
        ...prev,
        {
          type: "grafica",
          url,
          nombre: grafica.nombre,
          hora,
          count: 1,
        },
      ];
    });
  };

  // La función comprueba que el archivo subido por el usuario sea un archivo con extensión csv
  // Evento de React nativo que se ejecuta al cambiar el valor del input
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    //Operador de Encadenamiento Opcional que devuelve null. Evita excepción
    const file = e.target.files?.[0];
    if (!file) return; //si archivo null se sale de la funcion

    //Extensión check
    if (!file.name.endsWith(".csv")) {
      alert("Solo se permiten archivos CSV");
      return;
    }

    setArchivo(file);
  };

  // Se lee el fichero csv para guardar el total de lineas y columnas (campos)
  // Objeto nativo de JS File
  // Para las promesas -> https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise
  const parseCSV = (file: File) =>
    // Se crea nueva promesa para la correcta ejecución de funciones asíncronas
    // Resolve y Reject son callbacks de exito y error en base al resultado de la ejecución del codigo
    new Promise<{ lineas: number; columnas: number }>((resolve, reject) => {
      // FileReader de JS
      const reader = new FileReader();

      //Metodo de FileReader que ejecuta el evento al acabar la carga del fichero
      reader.onload = (event) => {
        //Casting del resultado del fichero a String
        const text = event.target?.result as string;
        //Si fichero vacio rechazamos
        if (!text) return reject("Archivo vacío");

        // Filas divididas por retornos de carro, se eliminan filas vacias
        // y se borran espacios en blanco innecesarios con trim
        const rows = text
          .split("\n")
          .map((r) => r.trim())
          .filter((r) => r !== "");

        //Para las columnas solo separamos una fila por comas
        const columnas = rows[0].split(",").length;

        //Devuelve un objeto con las lineas y columnas al acabar la ejecución de la promesa
        resolve({
          lineas: rows.length,
          columnas,
        });
      };

      reader.onerror = () => reject("Error leyendo archivo");

      reader.readAsText(file);
    });

  // Función asíncrona que permite no bloquear la ejecución del hilo principal en su llamada
  //
  const uploadCSV = async () => {
    if (!archivo) return; // condicion de salida si archivo está en null

    try {
      //await pausa la ejecucion hasta que reciba respuesta de la funcion que parsea el fichero
      const { lineas, columnas } = await parseCSV(archivo);

      //crea un nuevo objeto de tipo HistorialItem para guardarlo
      const nuevaEntrada: HistorialItem = {
        type: "csv",
        nombre: archivo.name,
        hora: new Date().toLocaleString(),
        lineas,
        columnas,
      };

      // Se añade al historial previo la nueva entrada en un nuevo array
      // prev (haciendo spread) hace referencia al estado previo del historial
      setHistorial((prev) => [...prev, nuevaEntrada]);
      setArchivo(null);
    } catch (err) {
      console.error(err);
    }
  };

  //Funcion que llama a hacer un clear del historial en la persistencia
  const clearHistorial = () => {
    setHistorial([]);
    localStorage.removeItem("historial");
  };

  // <> agrupa varios elementos sin usar nuevo div
  // dentro de return, comentarios -> {/* */}
  // var === valor && -> Render condicional: https://react.dev/learn/conditional-rendering
  // true && algo → devuelve algo
  // false && algo → devuelve false (no renderiza nada)
  return (
    <>
      <h1 id="titleDashboard">PyBusiness Analytics - Dashboard</h1>

      <div className="contenedor">
        <div className="logo">
          <img src="/icons/logo.svg" alt="Logo" className="logo-icon" />
        </div>

        <nav className="sidebar">
          <button
            className={`sidebar-item ${seccion === "dashboard" ? "active" : ""}`}
            onClick={() => setSeccion("dashboard")}
          >
            <img src="/icons/home.svg" alt="Home" className="icon" />
          </button>

          <button
            className={`sidebar-item ${seccion === "files" ? "active" : ""}`}
            onClick={() => setSeccion("files")}
          >
            <img src="/icons/folder.svg" alt="Files" className="icon" />
          </button>

          <button
            className={`sidebar-item ${seccion === "upload" ? "active" : ""}`}
            onClick={() => setSeccion("upload")}
          >
            <img src="/icons/upload.svg" alt="Subir" className="icon" />
          </button>

          <button
            className={`sidebar-item ${seccion === "charts" ? "active" : ""}`}
            onClick={() => setSeccion("charts")}
          >
            <img src="/icons/charts.svg" alt="Gráficas" className="icon" />
          </button>

          <button
            className={`sidebar-item ${seccion === "settings" ? "active" : ""}`}
            onClick={() => setSeccion("settings")}
          >
            <img
              src="/icons/settings.svg"
              alt="Configuración"
              className="icon"
            />
          </button>
        </nav>

        <div className="search-bar">
          <input
            id="sear-input"
            name="search"
            type="text"
            placeholder="Buscar..."
            className="search-input"
          />
          <button className="search-button">
            <img src="/icons/search.svg" alt="Buscar" className="search-icon" />
          </button>
        </div>

        <div className="user-panel">
          <img src="/icons/user.svg" alt="Usuario" className="user-avatar" />
          <div className="user-info">
            <span className="user-name">Juanito Alcachofa</span>
            <button className="logout-button">Cerrar sesión</button>
          </div>
        </div>

        <main className="main-content">
          {/* DASHBOARD */}
          {seccion === "dashboard" && (
            <>
              <h1>Inicio</h1>

              {/* Si no null se obtiene de la misma manera que en charts */}
              {ultimaGrafica ? (
                <div className="last-graph">
                  <h2>Última gráfica consultada</h2>
                  <p>{ultimaGrafica.nombre}</p>
                  <img
                    src={`${BASE_URL}${ultimaGrafica.url}`}
                    alt={ultimaGrafica.nombre}
                  />
                </div>
              ) : (
                <p>Aún no se ha consultado ninguna gráfica</p>
              )}
            </>
          )}

          {/* CHARTS */}
          {seccion === "charts" && (
            <>
              <h1>Gráficas</h1>

              <select
                id="selectGraph"
                className="dropdown-graphs"
                value={graficoActual}
                onChange={(e) => {
                  const url = e.target.value;
                  setGraficoActual(url);
                  registrarGrafica(url);
                }}
              >
                {graficos.map((g) => (
                  <option key={g.url} value={g.url}>
                    {g.nombre}
                  </option>
                ))}
              </select>

              <div className="graph">
                {/* Se concatena URL con ruta de gráfico */}
                <img src={`${BASE_URL}${graficoActual}`} alt="Gráfico" />
              </div>
            </>
          )}

          {/* ARCHIVOS (folder) */}
          {seccion === "files" && (
            <>
              <div className="files-header">
                <h1>Historial de gráficas</h1>
              </div>

              <div className="files-list">
                {/* Map recorre el array historial
                 Item se refiere al propio elemento y Idx a su índice */}
                {historial.map((item, idx) => {
                  if (item.type === "grafica") {
                    return (
                      <div key={idx} className="file-item">
                        <div className="file-left">
                          <strong>{item.nombre}</strong>
                          <p>Última consulta: {item.hora}</p>
                        </div>

                        <div className="file-right">
                          <span>x{item.count}</span>
                        </div>
                      </div>
                    );
                  }

                  {
                    /* Si no grafica, se asume que .csv */
                  }
                  return (
                    <div key={idx} className="file-item">
                      <div className="file-left">
                        <strong>{item.nombre}</strong>
                        <p>Añadido: {item.hora}</p>
                        <p>
                          Filas: {item.lineas} | Columnas: {item.columnas}
                        </p>
                      </div>

                      <div className="file-right">
                        <span>CSV</span>
                      </div>
                    </div>
                  );
                })}
              </div>

              <button className="upload-button" onClick={clearHistorial}>
                Limpiar historial
              </button>
            </>
          )}

          {/* UPLOAD */}
          {seccion === "upload" && (
            <>
              <h1>Subir archivos</h1>

              <div className="upload-box">
                <input type="file" accept=".csv" onChange={handleFileChange} />

                <button
                  className="upload-button"
                  onClick={uploadCSV}
                  disabled={!archivo}
                >
                  Subir archivo
                </button>
              </div>
            </>
          )}

          {/* SETTINGS */}
          {seccion === "settings" && (
            <>
              <h1>Configuración</h1>

              <div className="settings-box">
                <label>Modo de visualización:</label>

                <select value={modo} onChange={(e) => setModo(e.target.value)}>
                  <option value="noche">Modo noche</option>
                  <option value="dia">Modo día</option>
                </select>
              </div>
            </>
          )}
        </main>
      </div>
    </>
  );
}

export default App;
