"""Carga entradas de ejemplo para ver el blog funcionando: python manage.py seed_blog"""
from datetime import timedelta

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Comment, Post

DEMOS = [
    {
        "title": "Cómo armé este blog con Django",
        "summary": "Modelos, admin y templates: el recorrido para sumar un blog a mi portfolio.",
        "cover": None,
        "days_ago": 1,
        "content": (
            "Mi portfolio empezó como un HTML y un CSS sueltos. Para agregarle un blog "
            "lo migré a Django y separé el sitio en dos apps: portfolio (la home) y blog.\n\n"
            "El blog tiene tres modelos: Post, PostMedia (imágenes, videos o PDF adjuntos) y "
            "Comment. Las entradas se crean solamente desde el panel de administración, "
            "y los comentarios los puede escribir cualquiera pero solo el administrador "
            "puede borrarlos.\n\n"
            "Lo mejor de usar el admin de Django es que no tuve que programar formularios "
            "de carga: con registrar los modelos ya tenía todo el CRUD."
        ),
    },
    {
        "title": "Automatizando facturas con n8n e IA",
        "summary": "Un flujo que recibe facturas por mail, las lee con IA y las guarda en Google Sheets.",
        "cover": "proyecto-automatizacion.png",
        "days_ago": 8,
        "content": (
            "La idea era no cargar facturas a mano. El flujo en n8n arranca cuando llega un "
            "mail con adjuntos: separa cada archivo, se lo pasa a un modelo de IA que extrae "
            "los datos y los estructura.\n\n"
            "Después hay tres ramas: guardar cada factura en una planilla de Google Sheets, "
            "armar un informe que se envía por mail y, si faltan datos, generar un borrador "
            "de remito para completar.\n\n"
            "Lo más difícil fue lograr que la IA devuelva siempre la misma estructura."
        ),
    },
    {
        "title": "Diseñando la base de datos de un cine",
        "summary": "Del diagrama entidad-relación en MySQL Workbench a las tablas de funciones, butacas y tickets.",
        "cover": "proyecto-cines.png",
        "days_ago": 15,
        "content": (
            "Para el sistema de gestión de un cine empecé por el diagrama entidad-relación en "
            "MySQL Workbench. Las tablas principales son películas, salas, funciones, butacas, "
            "clientes, tickets y ventas.\n\n"
            "Después vinieron las relaciones: una función une una película con una sala en un "
            "horario, y cada ticket reserva una butaca de esa función.\n\n"
            "También armé procedimientos almacenados para las operaciones que se repiten, "
            "como registrar una venta."
        ),
    },
]


class Command(BaseCommand):
    help = "Crea entradas y un comentario de ejemplo (solo si el blog está vacío)."

    def handle(self, *args, **options):
        if Post.objects.exists():
            self.stdout.write("Ya hay entradas cargadas: no se hizo nada.")
            return

        now = timezone.now()
        images_dir = settings.BASE_DIR / "static" / "images"

        for demo in DEMOS:
            post = Post(
                title=demo["title"],
                summary=demo["summary"],
                content=demo["content"],
                published_at=now - timedelta(days=demo["days_ago"]),
            )
            if demo["cover"] and (images_dir / demo["cover"]).exists():
                with open(images_dir / demo["cover"], "rb") as f:
                    post.cover.save(demo["cover"], File(f), save=False)
            post.save()

        first = Post.objects.first()
        Comment.objects.create(
            post=first,
            name="Visitante de ejemplo",
            body="Comentario de prueba. El administrador puede eliminarlo desde /admin.",
        )
        self.stdout.write(self.style.SUCCESS(f"{len(DEMOS)} entradas de ejemplo creadas."))
