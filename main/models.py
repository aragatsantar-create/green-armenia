from django.db import models

class Project(models.Model):
    title = models.CharField("Название проекта", max_length=200)
    description = models.TextField("Описание")
    year = models.IntegerField("Год реализации")
    trees_planted = models.IntegerField("Посажено деревьев", default=0)
    is_active = models.BooleanField("Активен сейчас", default=True)
    
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
    
    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name="Проект")
    image = models.ImageField("Фото", upload_to='projects/')
    order = models.IntegerField("Порядок отображения", default=0)
    
    class Meta:
        verbose_name = "Фото проекта"
        verbose_name_plural = "Фото проектов"
        ordering = ['order']
    
    def __str__(self):
        return f"Фото для {self.project.title}"

class Volunteer(models.Model):
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=20, blank=True)
    message = models.TextField("Сообщение", blank=True)
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)
    
    class Meta:
        verbose_name = "Заявка волонтера"
        verbose_name_plural = "Заявки волонтеров"
    
    def __str__(self):
        return f"{self.name} - {self.email}"

class AboutPage(models.Model):
    title = models.CharField("Заголовок страницы", max_length=200, default="О нас")
    content = models.TextField("История проекта")
    image = models.ImageField("Фото для страницы", upload_to='about/', blank=True, null=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Страница 'О нас'"
        verbose_name_plural = "Страницы 'О нас'"

    def __str__(self):
        return self.title
class ContactInfo(models.Model):
    address = models.CharField("Адрес", max_length=300, blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    facebook = models.URLField("Facebook", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    telegram = models.URLField("Telegram", blank=True)
    description = models.TextField("Краткое описание для футера", blank=True, default="Aragats Antar — восстанавливаем леса Армении для будущих поколений.")
    
    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"
    
    def __str__(self):
        return "Контакты сайта"