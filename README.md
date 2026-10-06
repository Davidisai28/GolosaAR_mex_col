# Golosa AR — Proyecto COIL (México - Colombia)

**Golosa AR** (o *Avioncito*) es un videojuego móvil interactivo que reinventa este juego tradicional combinando **Realidad Aumentada (AR)**, trivias educativas y retos físicos. Este proyecto nace como una iniciativa colaborativa internacional (COIL) entre equipos de México y Colombia.

El prototipo está desarrollado en **Unity (plataforma Android)** empleando el patrón arquitectónico **MVC (Modelo-Vista-Controlador)** para asegurar un código mantenible y escalable, separando de forma estricta la interfaz de usuario, la lógica de negocio y el acceso a los datos.

---

## Flujo de Trabajo y Ramas (Git Workflow)

Para asegurar que todo el equipo pueda colaborar de manera ordenada y sin sobrescribir el trabajo de los demás, hemos adoptado un flujo de trabajo estructurado en Git.

> **Regla principal e inquebrantable:** **NUNCA** se debe hacer `push` directo a la rama `main` ni a la rama `develop`. Todo el trabajo de desarrollo debe ocurrir en la rama de `feature` correspondiente a tu tarea. Una vez que tu trabajo esté listo y probado, se debe crear un **Pull Request (PR)** hacia `develop`.

### ¿Para qué sirve cada rama?

| Rama | Propósito / Responsabilidad de la Rama |
| :--- | :--- |
| `main` | **Producción.** Solo contiene código 100% funcional y versiones estables validadas al cierre de cada iteración o *Sprint*. Nadie desarrolla aquí. |
| `develop` | **Integración.** Es la rama principal de trabajo en equipo. Aquí se junta el código de todos para verificar que las diferentes partes (`feature/*`) funcionen bien en conjunto. |
| `feature/ui-vistas` | **Diseño e Interfaz.** Todo lo relacionado a la interacción visual: Pantallas, menús, HUD, flujo de registro, etc. Trabaja sobre `Assets/Scenes`, `Assets/Sprites` y `Assets/Scripts/View`. |
| `feature/capa-ar` | **Realidad Aumentada.** Lógica exclusiva de AR Foundation, la detección de planos del mundo real, el posicionamiento y la interacción del tablero 3D (`Assets/Scripts/AR`, `Assets/Prefabs`). |
| `feature/controladores-logica` | **Lógica del Juego (Controlador).** El "cerebro" del juego: Flujo de la partida, turnos de los jugadores, eventos, sistema de puntuación (`Assets/Scripts/Controller`). |
| `feature/modelos-datos` | **Datos y Persistencia (Modelo).** Definición de las entidades (Jugador, Tablero), acceso a los bancos de preguntas (`.json`) y guardado local (`PlayerPrefs`) (`Assets/Scripts/Model`, `Assets/Scripts/Data`, `Assets/Resources/Questions`). |

**Pasos sugeridos para tu día a día:**
1. Asegúrate de tener la rama base actualizada: `git checkout develop` seguido de `git pull origin develop`.
2. Pásate a la rama en la que tienes asignado trabajar: por ejemplo, `git checkout feature/ui-vistas`.
3. Trae los cambios de develop a tu rama para evitar estar desactualizado: `git merge develop`.
4. Escribe tu código, prueba y registra tus avances (`git commit`).
5. Sube tu rama al servidor (`git push origin <tu-rama>`) y abre un PR en GitHub para que el equipo lo integre a `develop`.

---

## Estructura del Proyecto (Arquitectura MVC en Unity)

Para mantener el proyecto libre de código "spaghetti", hemos organizado los `Scripts` (y demás recursos) usando la arquitectura **MVC**. *Por favor, respeta el lugar de cada archivo.*

```text
Assets/
├── Prefabs/               # Elementos reutilizables listos para instanciar (tablero 3D, botones, fichas, paneles UI).
├── Resources/
│   └── Questions/         # Bancos de preguntas y retos almacenados en archivos .json (fáciles de editar por diseñadores).
├── Scenes/                # Escenas principales de Unity (ej. MainMenu, ARGame, GameOver).
├── Scripts/
│   ├── AR/                # Scripts aislados para gestionar AR (ARSessionManager, PlaneDetection, BoardPlacement).
│   ├── Controller/        # (Controlador) Orquestadores lógicos (GameManager, TurnManager, ScoreSystem). Reciben inputs de View, modifican Model.
│   ├── Data/              # Servicios de guardado y carga (ContentRepository para leer JSONs, LocalStorageService para PlayerPrefs).
│   ├── Model/             # (Modelo) Estructuras y estado de los datos (PlayerModel, BoardModel, GameSession). De preferencia sin MonoBehaviour.
│   └── View/              # (Vista) Lógica de la UI (botones, animaciones, textos). Escucha eventos del Controlador para actualizar pantalla.
└── Sprites/               # Imágenes 2D, íconos y texturas (idealmente importados desde Figma).
```

### ¿Cómo interactúan las capas?
- **View (Vista):** Capta el toque del jugador en un botón de la pantalla y le avisa al **Controller**. (¡Ojo! La Vista NO evalúa respuestas ni suma puntajes).
- **Controller (Controlador):** Escucha a la Vista, aplica las reglas del juego (ej. comprobar respuesta correcta) y actualiza el **Model**.
- **Model (Modelo):** Modifica su estado interno (ej. suma 10 puntos) y notifica a los interesados que los datos cambiaron.
- **View (Vista):** Se entera de que el puntaje subió y actualiza el texto en la pantalla, independientemente de cómo se haya calculado ese valor.
