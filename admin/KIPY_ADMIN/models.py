from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class Users(models.Model):
    telegram_id = models.BigIntegerField(verbose_name='ID Телеграм')
    sername = models.CharField(max_length=100, verbose_name='Имя пользователя')
    tg_login = models.CharField(max_length=100, null=True, verbose_name='Логин')
    gender = models.CharField(max_length=100, verbose_name='Пол')
    phone = models.CharField(max_length=100, null=True, verbose_name='Телефон')
    birthday = models.DateField(verbose_name='Дата рождения пользователя')
    end_blocking = models.DateTimeField(verbose_name='Дата Окончания блокировки', default=datetime.strptime('01.01.1999 00:00', '%d.%m.%Y %H:%M'))
    direction_blocking = models.TextField(verbose_name='Причина блокировки')
    mail = models.EmailField(max_length=100, null=True, verbose_name='Почта')

    def __str__(self):
        return f'{self.sername}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users_card'
        ordering = ['id']


class Projects(models.Model):
    TYPE = [
        ('Волонтерский', 'Волонтерский'),
        ('Коммерческий', 'Коммерческий'),

    ]
    STATUS = [
        ('Только идея', 'Только идея'),
        ('В поиске команды', 'В поиске команды'),
        ('Проект завершен', 'Проект завершен'),
        ('Проект заморожен', 'Проект заморожен'),
    ]
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание проекта')
    type_projects = models.CharField(max_length=30, choices=TYPE, default='Волонтерский', verbose_name='Тип проекта')
    status = models.CharField(max_length=20, choices=STATUS, default='Только идея', verbose_name='Статус проекта')
    author = models.CharField(max_length=100, verbose_name='Автор проекта')
    team = models.CharField(max_length=100, null=True, verbose_name='Команда')
    participants_count = models.PositiveIntegerField(verbose_name='Кол-во людей в команде',default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    link = models.TextField(verbose_name='Ссылка на подробное описанние проекта')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        db_table = 'projects_card'
        ordering = ['id']


class Vacancy(models.Model):
    VACANCY = [
        ('Практика', 'Практика'),
        ('Стажировка', 'Стажировка'),
        ('Работа', 'Работа'),
        ('Все типы', 'Все типы'),
    ]
    BUSYNESS = [
        ('Разовая занятость', 'Разовая занятость'),
        ('Частичная занятость', 'Частичная занятость'),
        ('Полная занятость', 'Полная занятость')
    ]
    SCHEDULE = [
        ('Стандартное время', 'Стандартное время'),
        ('Гибкий график', 'Гибкий график'),
    ]
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание вакансии')
    type_vacancy = models.CharField(max_length=30, choices=VACANCY, default='Практика', verbose_name='Тип вакансии')
    busyness = models.CharField(max_length=100,  choices=BUSYNESS, default='Разовая занятость', verbose_name='Занятность')
    schedule = models.CharField(max_length=100,  choices=SCHEDULE, default='Стандартное время', verbose_name='График работы')
    address = models.CharField(max_length=100, verbose_name='Адресс вакансии')
    active = models.BooleanField(verbose_name='Статус активности', default=True)
    # contacts = models.CharField(verbose_name='Контакты')
    # date = models.DateTimeField(verbose_name='Дата создания уведомления')
    # actuality = models.BooleanField(default=True, verbose_name='Актуальность объявления')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        db_table = 'vacancy_card'
        ordering = ['id']


class Practice(models.Model):
    TERM = [('Сентябрь — Январь', 'Сентябрь — Январь'),
            ('Февраль — Май', 'Февраль — Май'),
            ('Июнь — Август', 'Июнь — Август'),
            ]
    STATUS = [('Внутреняя', 'Внутреняя'),
              ('Партнера', 'Партнера')
              ]
    title = models.CharField(max_length=500, verbose_name='Наименование')
    practice_period = models.CharField(max_length=100, choices=TERM, verbose_name='Период практики')
    description = models.TextField(verbose_name='Описание')
    separator = models.CharField(max_length=100, choices=STATUS, default='Внутреняя', verbose_name='Тип вакансии')
    active = models.BooleanField(verbose_name='Статус активности', default=True)


class DeleteMessage(models.Model):
    chat_id = models.BigIntegerField(verbose_name='Чат ID')
    message_id = models.CharField(max_length=200, verbose_name='ID Сообщений')

    def str(self):
        return f"{self.chat_id}"

    class Meta:
        verbose_name = 'Удаление сообщений'
        verbose_name_plural = 'Удаление сообщений'
        db_table = 'delete_message'
