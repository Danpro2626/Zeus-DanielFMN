# Icono de ZEUS para Android (Samsung / One UI)

El icono está pensado para Android y para el estilo de **One UI**: fondo a sangre que el sistema recorta en *squircle*, y una capa monocromática para los **iconos temáticos** de One UI 5+ (Android 13+). No incluye ningún elemento de iOS.

![Vista previa: squircle de One UI, círculo y versión monocromática](icon-preview.png)

*De izquierda a derecha: máscara squircle (One UI), máscara circular y capa monocromática de los iconos temáticos.*

## Diseño

- **Concepto:** un medidor de carga abierto (270°) y un rayo en forma de Z. Se reconoce por la silueta aun a tamaños pequeños: *energía + velocidad + Zeus*.
- **Color:** verde bosque profundo de fondo y degradado esmeralda → lima en el medidor. El rayo, casi blanco, es el punto de mayor contraste.
- **Zona segura:** todo el dibujo cabe dentro del círculo de 66 dp que Android garantiza visible en un lienzo de 108 dp, así que ninguna máscara (squircle, círculo, lágrima) recorta nada.

| Elemento | Valor |
|---|---|
| Fondo | `#0D2318` → `#050F0A` (diagonal) |
| Medidor | `#2BEA8A` → `#B2F04A`, trazo 6,5 dp, extremos redondeados |
| Rayo | `#FFFFFF` → `#EAFFD0` |

## Qué hay en `android/`

```
android/
├── play-store-icon-512.png               Icono de 512 px para Google Play
└── res/
    ├── drawable/
    │   ├── ic_launcher_background.xml    Capa de fondo (vector, 108 dp)
    │   ├── ic_launcher_foreground.xml    Capa frontal (vector, 108 dp)
    │   └── ic_launcher_monochrome.xml    Capa para iconos temáticos
    ├── mipmap-anydpi-v26/
    │   ├── ic_launcher.xml               <adaptive-icon> (fondo + frente + monocromo)
    │   └── ic_launcher_round.xml
    └── mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/
        ├── ic_launcher.png               Respaldo para Android 7.1 y anteriores
        └── ic_launcher_round.png
```

Los iconos son vectoriales, así que se ven nítidos en cualquier densidad y en las pantallas de alta resolución de los Galaxy.

## Opción A: instalar la PWA en el Samsung (sin Android Studio)

1. Publica el proyecto (por ejemplo en GitHub Pages, ver el README).
2. Abre la dirección en **Chrome** o **Samsung Internet** y elige *Instalar app* / *Añadir a pantalla de inicio*.
3. El navegador usa los iconos de `manifest.webmanifest`. Para la PWA se generaron dos variantes en `assets/icons/`:
   - `icon-192.png` y `icon-512.png`: con esquinas redondeadas (`purpose: any`).
   - `icon-maskable-192.png` y `icon-maskable-512.png`: a sangre, con el dibujo dentro del 80 % central (`purpose: maskable`) para que Android aplique su propia máscara.

Chrome en Android crea una WebAPK con el icono *maskable*. En Samsung Internet el resultado puede variar según la versión; si ves el icono dentro de un recuadro blanco, instala desde Chrome.

## Opción B: usarlo en un proyecto de Android Studio

1. **Borra** los iconos que genera la plantilla de Android Studio para que no haya recursos duplicados:
   - `app/src/main/res/mipmap-*/ic_launcher*.webp`
   - `app/src/main/res/mipmap-anydpi-v26/ic_launcher*.xml` y `mipmap-anydpi/`
   - `app/src/main/res/drawable/ic_launcher_background.xml`
   - `app/src/main/res/drawable-v24/ic_launcher_foreground.xml`
2. **Copia** el contenido de `android/res/` dentro de `app/src/main/res/`.
3. En `AndroidManifest.xml`, dentro de `<application>`:

   ```xml
   <application
       android:icon="@mipmap/ic_launcher"
       android:roundIcon="@mipmap/ic_launcher_round"
       ... >
   ```

4. Sincroniza Gradle y ejecuta la app. Para previsualizar sin instalar, abre `mipmap-anydpi-v26/ic_launcher.xml` en Android Studio y usa la vista *Design*.

**Compatibilidad**

| Android | Qué se muestra |
|---|---|
| 13 o superior (One UI 5+) | Icono adaptativo; con *Iconos temáticos* activados, la capa monocromática teñida con el color del tema |
| 8 a 12 | Icono adaptativo (fondo + frente) con la máscara del lanzador |
| 7.1 o anterior | PNG `ic_launcher.png` / `ic_launcher_round.png` |

Para que el icono temático funcione, el usuario debe activar **Ajustes → Fondo de pantalla y estilo → Paleta de colores → Iconos temáticos** (la ruta exacta puede variar según el modelo y la versión de One UI).

## Opción C: generar un APK a partir de la PWA

Si quieres un APK sin escribir código Android, puedes empaquetar la PWA con [Bubblewrap](https://github.com/GoogleChromeLabs/bubblewrap) o [PWABuilder](https://www.pwabuilder.com). Ambos leen `manifest.webmanifest` y toman el icono *maskable*. Ten en cuenta que una *Trusted Web Activity* exige verificar el dominio con un archivo `assetlinks.json` en la raíz del sitio, algo que con GitHub Pages en una subruta (`usuario.github.io/zeus`) requiere un dominio propio o un repositorio `usuario.github.io`.

## Subirlo a Google Play

Usa `android/play-store-icon-512.png` (512 × 512 px, PNG). Google aplica su propia máscara, por eso el archivo es un cuadrado a sangre sin esquinas redondeadas.

## Regenerar o retocar el icono

Toda la geometría (anillo, rayo, colores) está en un único archivo:

```bash
pip install cairosvg pillow
python3 tools/make_icons.py
```

Cambia las constantes de arriba del script (`R`, `SW`, `A_FILL`, `BOLT_RAW`, colores) y se regeneran los PNG, los SVG y los XML de Android a la vez, sin que se desalineen entre sí.
