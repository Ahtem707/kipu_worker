"""
Файл - взаимодействует с базой данных
"""
from peewee import *
from settings.settings import DATABASE, USER, PASSWORD, HOST, PORT

db = PostgresqlDatabase(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT, autorollback=True)


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class DeleteMessage(BaseModel):
    chat_id = BigIntegerField()
    message_id = CharField(max_length=200)

    class Meta:
        db_table = 'delete_message'


class Levels(BaseModel):
    title = CharField(max_length=500)

    class Meta:
        db_table = 'levels'


class Specializations(BaseModel):
    title = CharField(max_length=500)
    direction_selection = IntegerField()

    class Meta:
        db_table = 'specialization'


class FormOfEmployment(BaseModel):
    title = CharField(max_length=500)

    class Meta:
        db_table = 'form_of_employment'


class Vacancy(BaseModel):
    title = CharField(max_length=100, verbose_name='Наименование')
    description = TextField(verbose_name='Описание вакансии')
    type_vacancy = CharField(max_length=3)
    busyness = CharField(max_length=100)
    schedule = CharField(max_length=100)
    address = CharField(max_length=100)
    active = BooleanField()

    class Meta:
        db_table = 'vacancy_card'


class PracticeSpecializations(BaseModel):
    title = CharField(max_length=500)
    choice_of_direction = IntegerField()

    class Meta:
        db_table = 'practicespecializations'


class Practice(BaseModel):
    title = CharField(max_length=500)
    practice_period = CharField(max_length=100)
    description = TextField()
    separator = CharField(max_length=100, default='Внутреняя')
    active = BooleanField()

    class Meta:
        db_table = 'practice'


class Projects(BaseModel):
    title = CharField(max_length=100)
    description = TextField()
    type_projects = CharField(max_length=30)
    status = CharField(max_length=20)
    author = CharField(max_length=100)
    team = CharField(max_length=100, null=True)
    participants_count = IntegerField(default=1)
    link = TextField()

    class Meta:
        db_table = 'projects_card'


class Mailing(BaseModel):
    level = ForeignKeyField(Levels, on_delete='CASCADE')
    course = CharField(max_length=20)
    specialization = CharField(max_length=100, null=True)
    form_of_employment = ForeignKeyField(FormOfEmployment, on_delete='CASCADE', null=True)
    sending_start_date = DateField(null=True)
    date_of_last_mailing = DateField(null=True)
    date_of_next_mailing = DateField(null=True)
    user_id = BigIntegerField()
    mailing_type = CharField(max_length=100)
    mailing_period = CharField(max_length=100)
    term_period = CharField(max_length=100, null=True)

    class Meta:
        db_table = 'mailing'


class Events(BaseModel):
    title = CharField(max_length=500)
    date = DateTimeField(null=True)
    description = TextField(null=True)

    class Meta:
        db_table = 'events'


class Course(BaseModel):
    COURSE = [('1', '1'),
              ('2', '2'),
              ('3', '3'),
              ('4', '4'),
              ('5', '5'),
              ('Выпускник', 'Выпускник')]
    course = CharField(max_length=20, choices=COURSE)
    levels = ForeignKeyField(Levels, on_delete='CASCADE')

    class Meta:
        db_table = 'course'


class ListVacancies(BaseModel):
    COURSE = [('1', '1'),
              ('2', '2'),
              ('3', '3'),
              ('4', '4'),
              ('5', '5'),
              ('Выпускник', 'Выпускник')]
    vacancies = ForeignKeyField(Vacancy, on_delete='CASCADE')
    level = ForeignKeyField(Levels, on_delete='CASCADE')
    specialization = ForeignKeyField(Specializations, on_delete='CASCADE')
    course = ForeignKeyField(Course, on_delete='CASCADE')


    class Meta:
        db_table = 'listvacancies'


class ListPractices(BaseModel):
    COURSE = [('1', '1'),
              ('2', '2'),
              ('3', '3'),
              ('4', '4'),
              ('5', '5'),
              ('Выпускник', 'Выпускник')]
    practices = ForeignKeyField(Practice, on_delete='CASCADE', )
    level = ForeignKeyField(Levels, on_delete='CASCADE')
    specialization = ForeignKeyField(PracticeSpecializations, on_delete='CASCADE')
    course = ForeignKeyField(Course, on_delete='CASCADE')


    class Meta:
        db_table = 'listpracticess'

