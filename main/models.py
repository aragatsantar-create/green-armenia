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

# === НОВАЯ МОДЕЛЬ ДЛЯ СТРАНИЦЫ JOIN ===
class JoinPage(models.Model):
    # Русский
    title_ru = models.CharField("Заголовок (русский)", max_length=200, default="Присоединяйтесь к нам!")
    subtitle_ru = models.TextField("Подзаголовок (русский)", blank=True, default="Заполните форму ниже, чтобы стать частью команды Aragats Antar")
    text_1_ru = models.TextField("Текст 1 (русский)", blank=True)
    text_2_ru = models.TextField("Текст 2 (русский)", blank=True)
    text_3_ru = models.TextField("Текст 3 (русский)", blank=True)
    text_4_ru = models.TextField("Текст 4 (русский)", blank=True)
    text_5_ru = models.TextField("Текст 5 (русский)", blank=True)

    # English
    title_en = models.CharField("Заголовок (english)", max_length=200, default="Join us!")
    subtitle_en = models.TextField("Подзаголовок (english)", blank=True, default="Fill out the form below to become part of the Aragats Antar team")
    text_1_en = models.TextField("Текст 1 (english)", blank=True)
    text_2_en = models.TextField("Текст 2 (english)", blank=True)
    text_3_en = models.TextField("Текст 3 (english)", blank=True)
    text_4_en = models.TextField("Текст 4 (english)", blank=True)
    text_5_en = models.TextField("Текст 5 (english)", blank=True)

    # Հայերեն (Уже с правильными HTML-тегами и цветом!)
    title_hy = models.CharField("Заголовок (հայերեն)", max_length=200, default="Միացեք մեզ!")
    subtitle_hy = models.TextField("Подзаголовок (հայերեն)", blank=True, default="Լրացրեք ստորև բերված ձևը՝ Aragats Antar-ի թիմի մաս դառնալու համար")
    text_1_hy = models.TextField("Текст 1 (հայերեն)", blank=True, default="«<strong>Aragats Antar</strong>»-ը պարզապես անտառների վերականգնման ծրագիր չէ։ Այն համախոհների համայնք է, որտեղ յուրաքանչյուրը կարող է գտնել իր տեղը և իրական ներդրում ունենալ Հայաստանի բնության և կլիմայի պահպանման գործում։")
    text_2_hy = models.TextField("Текст 2 (հայերեն)", blank=True, default="Մենք փնտրում ենք <strong>ագրոնոմների և դենդրոլոգների</strong>։ Մեզ անհրաժեշտ են <span class=\"brand-color\"><strong>կամավոր-կանաչապատողներ</strong></span>, ովքեր պատրաստ են մասնակցել շաբաթօրյակներին, տնկել ծառեր և խնամել տնկիները։")
    text_3_hy = models.TextField("Текст 3 (հայերեն)", blank=True, default="Եթե դուք <span class=\"brand-color\"><strong>SMM մասնագետ</strong></span> եք, մենք ձեզ կվստահենք սոցիալական ցանցերի վարումը և բովանդակության ստեղծումը։ <strong>Քոփիռայթերները</strong> կօգնեն մեզ գրել տեքստեր կայքի և ԶԼՄ-ների համար։ <span class=\"brand-color\"><strong>Կոնտենտ ստեղծողները և լուսանկարիչները</strong></span> կնկարահանեն տեսանյութեր ու լուսանկարներ՝ ցուցադրելով Արագածի գեղեցկությունն ու անտառների վերականգնման ընթացքը։")
    text_4_hy = models.TextField("Текст 4 (հայերեն)", blank=True, default="Իսկ եթե ունեք այլ մասնագիտություններ՝ դիզայն, իրավաբանություն, հաշվապահություն, լոգիստիկա կամ այլ ոլորտներ, վստահ ենք՝ ձեր գիտելիքներն ու փորձը նույնպես կարող են կարևոր ներդրում ունենալ մեր առաքելության մեջ։")
    text_5_hy = models.TextField("Текст 5 (հայերեն)", blank=True, default="<strong>Ի՞նչ կստանաք դուք։</strong> Իրական փորձ, նոր ծանոթություններ, եզակի լուսանկարներ լեռների ֆոնին, պորտֆոլիոյի համալրում և գիտակցում, որ դուք ավելի լավն եք դարձնում աշխարհը։ Յուրաքանչյուր տնկած ծառը ձեր անձնական ներդրումն է Հայաստանի ապագայում։")

    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Страница 'Присоединиться'"
        verbose_name_plural = "Страница 'Присоединиться'"

    def __str__(self):
        return "Страница 'Присоединиться'"