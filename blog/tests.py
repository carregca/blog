from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Comment, Post


def make_post(title="Hola mundo", **kwargs):
    return Post.objects.create(
        title=title, summary="Resumen", content="Contenido", **kwargs
    )


class PostModelTests(TestCase):
    def test_slug_se_genera_y_es_unico(self):
        a = make_post("Mi entrada")
        b = make_post("Mi entrada")
        self.assertEqual(a.slug, "mi-entrada")
        self.assertEqual(b.slug, "mi-entrada-2")

    def test_published_excluye_borradores_y_futuras(self):
        visible = make_post("Visible")
        make_post("Borrador", published=False)
        make_post("Futura", published_at=timezone.now() + timedelta(days=3))
        self.assertEqual(list(Post.objects.published()), [visible])


class BlogViewsTests(TestCase):
    def test_listado_ordenado_de_mas_nueva_a_mas_vieja(self):
        now = timezone.now()
        vieja = make_post("Vieja", published_at=now - timedelta(days=5))
        nueva = make_post("Nueva", published_at=now - timedelta(days=1))
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["posts"]), [nueva, vieja])

    def test_borrador_da_404_al_publico(self):
        borrador = make_post("Borrador", published=False)
        response = self.client.get(borrador.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_home_muestra_ultimas_entradas(self):
        make_post("Para la home")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Para la home")


class CommentTests(TestCase):
    def setUp(self):
        self.post = make_post()
        self.url = self.post.get_absolute_url()

    def test_visitante_anonimo_puede_comentar(self):
        response = self.client.post(self.url, {"name": "Ana", "body": "Muy bueno"})
        self.assertRedirects(
            response, f"{self.url}#comentarios", fetch_redirect_response=False
        )
        self.assertEqual(self.post.comments.count(), 1)

    def test_honeypot_bloquea_bots(self):
        self.client.post(
            self.url, {"name": "Bot", "body": "spam", "website": "http://spam.com"}
        )
        self.assertEqual(Comment.objects.count(), 0)

    def test_comentario_vacio_no_se_guarda(self):
        self.client.post(self.url, {"name": "", "body": ""})
        self.assertEqual(Comment.objects.count(), 0)

    def test_anonimo_no_puede_eliminar(self):
        comment = Comment.objects.create(post=self.post, name="Ana", body="Hola")
        response = self.client.post(reverse("blog:comment_delete", args=[comment.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())

    def test_admin_puede_eliminar(self):
        comment = Comment.objects.create(post=self.post, name="Ana", body="Hola")
        admin = get_user_model().objects.create_superuser("admin", "a@a.com", "clave-segura-123")
        self.client.force_login(admin)
        self.client.post(reverse("blog:comment_delete", args=[comment.pk]))
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_eliminar_por_get_no_esta_permitido(self):
        comment = Comment.objects.create(post=self.post, name="Ana", body="Hola")
        response = self.client.get(reverse("blog:comment_delete", args=[comment.pk]))
        self.assertEqual(response.status_code, 405)
