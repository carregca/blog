import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="título")),
                ("slug", models.SlugField(blank=True, help_text="Parte de la URL. Se completa sola a partir del título.", max_length=220, unique=True, verbose_name="slug")),
                ("summary", models.CharField(help_text="Se muestra en el listado del blog y en la home.", max_length=300, verbose_name="resumen")),
                ("content", models.TextField(help_text="Texto de la entrada. Los saltos de línea se respetan; una línea en blanco separa párrafos.", verbose_name="contenido")),
                ("cover", models.ImageField(blank=True, help_text="Imagen principal (opcional).", upload_to="posts/covers/", verbose_name="portada")),
                ("published", models.BooleanField(default=True, help_text="Destildala para guardar la entrada como borrador.", verbose_name="publicada")),
                ("published_at", models.DateTimeField(default=django.utils.timezone.now, verbose_name="fecha de publicación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="última edición")),
            ],
            options={
                "verbose_name": "entrada",
                "verbose_name_plural": "entradas",
                "ordering": ["-published_at"],
            },
        ),
        migrations.CreateModel(
            name="PostMedia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="posts/media/", validators=[django.core.validators.FileExtensionValidator(("jpg", "jpeg", "png", "gif", "webp", "mp4", "webm", "ogg", "pdf"))], verbose_name="archivo")),
                ("caption", models.CharField(blank=True, max_length=200, verbose_name="epígrafe")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="orden")),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="media", to="blog.post", verbose_name="entrada")),
            ],
            options={
                "verbose_name": "archivo multimedia",
                "verbose_name_plural": "archivos multimedia",
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, verbose_name="nombre")),
                ("body", models.TextField(max_length=1000, verbose_name="comentario")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="fecha")),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="blog.post", verbose_name="entrada")),
            ],
            options={
                "verbose_name": "comentario",
                "verbose_name_plural": "comentarios",
                "ordering": ["created_at"],
            },
        ),
    ]
