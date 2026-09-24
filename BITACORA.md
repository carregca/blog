# Bitácora — TP Django: sitio personal con blog

> **Borrador para completar con tu experiencia.** Las decisiones y problemas técnicos de abajo son los que aparecieron al migrar el portfolio a Django; agregá/quitá lo que te haya pasado a vos y reescribilo con tus palabras y fechas reales.

## Punto de partida

Portfolio estático (`indexprueba.html` + `styles.css`) con secciones inicio, sobre mí, habilidades, proyectos y contacto, tema oscuro/claro y CV descargable.

## Plan

1. Crear el proyecto Django (`config`) y dos apps: `portfolio` y `blog`.
2. Convertir el HTML en templates con herencia (`base.html`) y `{% static %}`.
3. Modelos del blog: `Post`, `PostMedia`, `Comment`.
4. Admin para crear entradas y moderar comentarios.
5. Vistas: listado paginado, detalle con formulario de comentarios.
6. Estilos del blog coherentes con el portfolio.
7. Tests, README y entrega.

## Dificultades y cómo las resolví

**1. Rutas de archivos estáticos.** En el HTML original los recursos estaban con rutas relativas (`css/styles.css`, `images/…`, `cv/cv.pdf`). En Django dejan de funcionar: hay que ponerlos en `static/`, cargar `{% load static %}` y usar `{% static '…' %}`. Además, las anclas del menú (`#proyectos`) pasaron a `{% url 'home' %}#proyectos` porque en el blog ya no estamos en la home.

**2. Un selector global rompió el encabezado de la entrada.** `styles.css` define estilos directamente sobre la etiqueta `header` (posición fija, fondo, blur). Al usar `<header>` dentro de la entrada para el título, se comportaba como una segunda barra fija. Lo cambié por un `<div class="post-header">`. Lección: los selectores de etiqueta desnuda condicionan todo el sitio.

**3. Especificidad del CSS heredado.** Reglas como `.section > p` pisaban estilos nuevos (por ejemplo el aviso de borrador). Resolví subiendo la especificidad del selector nuevo en lugar de tocar `styles.css`.

**4. El tema oscuro/claro no se recordaba.** En una sola página no importaba, pero con un blog el visitante cambia de página y el tema volvía a oscuro. Moví el script a `theme.js` y guardo la elección en `localStorage`. También corregí un detalle del modo claro: el subrayado del menú era blanco sobre fondo claro.

**5. Slugs únicos.** Dos entradas con el mismo título generarían la misma URL. `Post.save()` genera el slug desde el título y agrega `-2`, `-3`… si ya existe.

**6. "Solo el admin borra comentarios".** Además del admin de Django, agregué un botón *Eliminar* en la entrada que solo se muestra con el permiso `blog.delete_comment`. La vista lo vuelve a verificar del lado del servidor (403 si no lo tiene) y solo acepta POST, porque ocultar el botón no alcanza como seguridad.

**7. Spam en comentarios sin login.** Sin registro, cualquiera puede publicar. Sumé un campo honeypot y validación de largo; la moderación queda a cargo del admin.

**8. Archivos multimedia.** `ImageField` necesita Pillow. Para videos y PDFs usé un modelo aparte (`PostMedia`) con un validador de extensiones, y en el template decido cómo mostrar cada archivo (`<img>`, `<video>` o enlace). En desarrollo hay que servir `MEDIA_ROOT` desde `urls.py`.

## Qué haría distinto

- Usar Markdown (o un editor enriquecido) para poder dar formato al texto de las entradas.
- Validar el tamaño de los archivos subidos y redimensionar imágenes grandes (`proyecto-60-seconds.png` pesa casi 3 MB).
- Separar la lista de habilidades y proyectos del portfolio en modelos, así se editan desde el admin en vez de estar escritos en el template.

## Cosas que quedaron en el tintero

- Menú de navegación en celulares (el CSS original oculta los links a partir de 650px y no hay menú hamburguesa).
- Categorías/etiquetas y buscador para las entradas.
- Feed RSS.
- Registro/login de usuarios comentaristas y respuestas anidadas.
- Deploy (PythonAnywhere, Render, etc.): pasar `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` por variables de entorno (ya están preparadas en `settings.py`) y configurar `collectstatic`.
- Cambiar `SECRET_KEY` y usar una base de datos distinta a SQLite si el sitio crece.
