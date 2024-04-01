#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

# *Мастерская. Яндекс Практикум*

# # Описание проекта ##

# 1. Знакомство с данными
#    - 1.1. Загрузка библиотек
#    - 1.2. Загрузка данных, проверка формата полей данных
# 2. Предобработка данных
#    - 2.1. Определение пропусков
#    - 2.2. Поиск дубликатов
#    - 2.3. Обнаружение анамальных значений
#    - 2.4. Определение уникальных названий по полям
# 3. Исследовательский анализ данных
#    - 3.1. Определим общее числов вакансий Бизнес аналитика, Аналитика данных размещеных на hh.ru и какого грейда
#    - 3.2. Найдем навыки hard-skills и soft-skills, которые хотят выдеть работадатели у кандидатов на должность Бизнес аналитик в зависимости от грейда
#    - 3.3. Определим какое количество вакансий Бизнес аналитика и какого грейда размещено на ресурсе hh.ru по городам и определим ТОП-15 городов по количеству предложений
# 4. Общий вывод

# **Путь к файлу:**
# - данные о вакансиях Бизнес аналитика `/Downloads/vacancies_ba_new.xlsx`
# - данные о вакансиях Аналитик данных `/Downloads/vacancies_da_new.xlsx`
# 
# **Цель:** Провести исследование имеющихся данных по вакансиям Бизнес аналитики и Аналитик данных. Определить идеального кандидата на должность Бизнес аналитика и Аналитика данных для различных грейдов. Расчитать помесячную динамику количества вакансий для Аналитика данных и Бизнес аналитиков.

# 1. Предобработка данных.
# 2. Исследовательский анализ данных.
# 3. Определение наиболее желаемых кандидатов на вакансии Аналитик данных и Бизнес-аналитик по следующим параметрам: самые важные hard-skils, самые важные soft-skils, опыт работы. Ответ отдельно дайте для грейдов Junior, Junior+, Middle, Senior.
# 4. Определение типичного места работы для Аналитика данных и Бизнес-аналитика по следующим параметрам: ТОП-работодателей, зарплата, тип занятости, график работы. Ответ отдельно дайте для грейдов Junior, Junior+, Middle, Senior.
# 5. Расчет помесячной динамики количества вакансий для Аналитика данных и Бизнес-аналитика. Ответ отдельно дайте для грейдов Junior, Junior+, Middle, Senior.
# 6. Формулирование выводов и рекомендаций.
# 7. Создание презентации.
# 

# **Знакомство с данными**

# **1.1. Загрузка библиотек**

# In[1]:


#импортируем библиотеки для работы с данными
import pandas as pd
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import math
from plotly.offline import iplot
import plotly.express as px
import folium


# **1.2. Загрузка данных**

# In[2]:


#загрузка файлов vacancies_ba_new и 
df_biza = pd.read_excel('C:/Users/1394945/Documents/Проект_Мастерская данных/vacancies_ba_new.xlsx')
df_da = pd.read_excel('C:/Users/1394945/Documents/Проект_Мастерская данных/vacancies_da_new.xlsx')

display(df_biza.head())  #выведем первые пять строк каждого датафрейма для визуальной оценки
display(df_biza.info())  #выведем общую информацию, для общей оценки данных
display(df_biza.describe().round(1))

display(df_da.head())    #выведем первые пять строк каждого датафрейма для визуальной оценки
display(df_da.info())    #выведем общую информацию, для общей оценки данных
display(df_da.describe().round(1))


# **Описание данных**
# <br>Заказчиком представлены два DataFrame, в которых содержатся информация о вакансия "Бизнес аналитика" и "Аналитика данных". Оба DataFrame содержат следующие поля:
# - `id` - идентификатор вакансии на сайте hh.ru,
# - `name` - наименование вакнсии на сайте hh.ru,
# - `published_at` - дата публикации вакансии на hh.ru,
# - `alternate_url` - адресная ссылка на вакансию на hh.ru,
# - `type`- тип вакансии,
# - `employer` - наименование работодателя,
# - `department` - департамент,
# - `area`- город где расположено рабочее место,
# - `experience` - требуемый опыт,
# - `key_skills` - профессиональные навыки и знания,
# - `schedule` - график работы,
# - `employment`- тип трудоустройства,
# - `description` - описание вакансии,
# - `description_lemmatized` - краткое описание вакансии,
# - `salary_from` - уровень дохода,
# - `salary_to` - нижний уровень дохода,
# - `salary_bin` - верхний уровень дохода,
# - `key_skills_from_key_skills_field`- дополнительные профессиональные навыки и знания,
# - `hard_skills_from_description`- жестские навыки,
# - `soft_skills_from_description` -мягкие навыки.

# # 2. Предобработка данных ###

# **2.1. Определение пропусков**

# In[3]:


#Выведем пропуски df_biza
print('Кол-во пропусков в df_biza')
report_biza = df_biza.isna().sum().to_frame()
report_biza = report_biza.rename(columns = {0: 'missing_values'})
report_biza ['% of total'] = (report_biza['missing_values']/df_biza.shape[0]).round(2)*100
display(report_biza.sort_values(by='missing_values', ascending = False))

#предварительно провели обработку в Excel данных в полях key_skills, hard_skills, soft_skills 
#удалили не нужные элементы [, ], '

#Выведем пропуски df_da
print('Кол-во пропусков в df_da')
report_da = df_da.isna().sum().to_frame()
report_da = report_da.rename(columns = {0: 'missing_values'})
report_da ['% of total'] = (report_da['missing_values']/df_da.shape[0]).round(2)*100
display(report_da.sort_values(by='missing_values', ascending = False))


# **2.2. Поиск дубликатов**

# In[4]:


#проверим на дубликаты в данных
display(f'Количество дубликатов по полю df_biza: {df_biza.duplicated().sum()}')

display(f'Количество дубликатов по полю df_da: {df_da.duplicated().sum()}')


# **Вывод:** Тип данных соответствует значениям в каждом поле, обработка в данной области не требуется. Определили, что имеются пропуски в полях `salary_to`, `department`, `hard_skills_from_description`, `salary_from`, `soft_skills_from_description` заполнять их или удалять нет необходимости, на исследование они не повлияют. Проводить обработку полей `salary_to` и `salary_from` нет необходимости, в расчет будем брать имеющиеся данные.
# Заполнять пропуски в полях не будем. Наименование столбцов соответствует правилам написания.
# <br>Дубликаты в данных отсутствуют. 

# In[5]:


display('Наименование столбцов в df_ba:', [column for column in df_biza])
display('Наименование столбцов в df_ba:', [column for column in df_da])


# In[6]:


#переименуем длинное наименование некоторых столбцов
df_biza = df_biza.rename(columns={'hard_skills_from_description':'hard_skills', 'soft_skills_from_description':'soft_skills'})
df_da = df_da.rename(columns={'hard_skills_from_description':'hard_skills', 'soft_skills_from_description':'soft_skills'})


# In[7]:


#проверим уникальность названия
print('Уникальные названия городов по вакансиям для Бизнес аналитиков')
df_biza_sity = df_biza.groupby('area')
display(df_biza['area'].sort_values().unique())

print('Уникальные названия городов по вакансиям для Аналитика данных')
df_da_sity = df_da.groupby('area')
display(df_da['area'].sort_values().unique())

print('Категория требуемого опыта для Бизнес аналитика')
df_biza_grade = df_biza.groupby('experience')
display(df_biza['experience'].sort_values().unique())

print('Категория требуемого опыта для Аналитика данных')
df_da_grade = df_da.groupby('experience')
display(df_da['experience'].sort_values().unique())

display(df_da['salary_bin'].sort_values().unique())


# **Вывод**: Все наименование городов имеют уникальное название иные интерпритации не обнаружены, корректировать и приводит в однообразное наименование нет необходимости. Так же определили, что вакансий группы Бизнес Аналити и Аналитик данных одинаковые категории (grade) по требуемому опыту работы к кандидата, их 4 (четыре):
# <br>**`Junior (no experince)`** - без опыта работы
# <br>**`Junior+ (1-3 years)`** - от 1 (одного) года до 3 (трёх) лет
# <br>**`Middle (3-6 years)`** - от 3 (трёх) лет до 6 (шести) лет
# <br>**`Senior (6+ years)`** - более 6 (шести) лет

# **2.3. Обнаружение анамальных значений**

# In[8]:


display(df_biza['salary_from'].describe())

#удалим строку со значением 60 рублей, что не искажал данные
display(df_biza['salary_from'].count())
df_biza[df_biza['salary_from'] == 60]  #выведем строчку с минимальным предложением

#display(df_biza.loc[2379, 'salary_from']) 
df_ba = df_biza.drop(index = 2379)
df_ba_group = ['salary_from']
display(df_ba[df_ba_group].describe().round(1))


# **2.4. Определение уникальных значений**

# In[9]:


#подсчитаем количество уникальных значений по расположению рабочих мест
print('Кол-во городов и стран в которых имеются вакансии Бизнес аналитика:', len(df_biza['area'].unique()))
print('Кол-во городов и стран в которых имеются вакансии Аналитика данных:', len(df_da['area'].unique()))


# In[10]:


#определим сколько вакансий Бизнес аналитика каждого грейда, проверим числовые показатели: min, max, mean, median
display(df_biza['experience'].value_counts())
df_biza_group = ['salary_from']
display(df_biza[df_biza_group].describe().round(1))

#определим сколько вакансий Аналитика данных каждого грейда, проверим числовые показатели 
display(df_da['experience'].value_counts())
df_da_group = ['salary_from']
display(df_da[df_da_group].describe().round(1))


# **Найдем уникальные значения по должности Бизнес аналитик в полях key_skills, hard_skills, soft_skills**

# In[11]:


print('Уникальные значения по полю key skills для Бизнес аналитика:')
df_ba.key_skills.str.split(', ').explode().value_counts()


# In[12]:


print('Уникальные значения по полю soft skills для Бизнес аналитика:')
df_ba.soft_skills.str.split(', ').explode().value_counts()


# In[13]:


print('Уникальные значения по полю hard skills для Бизнес аналитика:')
df_ba.hard_skills.str.split(', ').explode().value_counts()


# **Найдем уникальные значения по должности Аналитик данных в полях key_skills, hard_skills, soft_skills**

# In[14]:


print('Уникальные значения по полю key skills для Аналитика данных')
df_da.key_skills.str.split(', ').explode().value_counts()


# In[15]:


print('Уникальные значения по полю soft skills для Аналитику данных:')
df_da.soft_skills.str.split(', ').explode().value_counts()


# In[16]:


print('Уникальные значения по полю hard skills для Аналитику данных:')
df_da.hard_skills.str.split(', ').explode().value_counts()


# **Вывод:** загрузили данные и провели обработку для возможности проведения дальнейшего исследования. На момент обработки нам известно, что в файлах имеется информация по 4171 вакансии Бизнес аналитика и 786 вакансиях Аналитика данных. Выявили уникальные значения наименования городов в которых предлагается вакансии. Выявили, что по полю `salary_from` по должности Бизнес аналитик отсутствуют данные в 3244 записи, это 78% от общего объема, а по вакансиям Аналитик данных в поле `salary_from` в 717 записях отсутствуют данные, это 91%, значит на основании имеющихся данных по полю `salary_from` будем расчитывать средний уровень предлагаемого дохода.

# # Исследовательский анализ ##

# **3.1. Определим общее числов вакансий Бизнес аналитика, Аналитика данных размещеных на hh.ru и какого грейда**

# **Определим какое количество вакансий Бизнеса аналитика и какого грейда размещено на ресурсе hh.ru**

# In[17]:


#сгруппируем количество вакансий Бизнес аналитикам по грейдам 
df_ba_cnt=df_ba.groupby(['experience'])['id'].count().reset_index()
display(df_ba_cnt.sort_values(by='experience', ascending=True))

#для более наглядной визуализации строим гистограмму отображающщую количество вакансий каждого грейда
category = px.bar(df_ba_cnt, x='experience', 
                                 y='id', 
                                 color='experience', 
                                 text ='id',
                                 title='Распределение кол-ва вакансий Бизнеса аналитика по грейдам')

#переименуем легенды графика
category.update_layout(xaxis_title = 'Грейд',
                       yaxis_title = 'Кол-во вакансий Бизнес аналитика', title_x=0.5)

#определим направление текста
category.update_xaxes(tickangle=0)
category.show()


# **Вывовд:** по большей части вакансий Бизнес аналитик от соискателей требуется опыт работы от 1 года (2121 вакансия) и от 3 лет (1596 вакансий), к данной категории относятся специалисты грейдом Junior+ и Middle.

# **Определим какое количество вакансий Аналитик данных и какого грейда размещено на ресурсе hh.ru**

# In[18]:


#сгруппируем количество вакансий Аналитика данных по грейдам 
df_da_cnt=df_da.groupby(['experience'])['id'].count().reset_index()

display(df_da_cnt.sort_values(by='experience', ascending=True))

#строим гистограмму отображающщую количество заведений в каждой категории
category = px.bar(df_da_cnt, x='experience', 
                                 y='id', 
                                 color='experience', 
                                 text ='id',
                                 title='Распределение кол-ва вакансий Аналитика данных по грейдам')

#переименуем легенды графика
category.update_layout(xaxis_title = 'Грейд',
                       yaxis_title = 'Кол-во вакансий Аналитик данных', title_x=0.5)

#определим направление текста
category.update_xaxes(tickangle=0)
category.show()


# **Вывовд:** по большей части вакансий Аналитика данных от соискателей требуется опыт работы от 1 года (387 вакансия) и от 3 лет (355 вакансий), к данной категории относятся специалисты грейдом Junior+ и Middle.

# **3.2. Найдем навыки hard-skills и soft-skills, которые хотят выдеть работадатели у кандидатов на должность Бизнес аналитик в зависимости от грейда**

# In[38]:


print('ТОП навыков необходимых Бизнес аналитику уровня ''Junior (no experince)'':')
print()
df_ba_skills_Jun = df_ba.loc[df_ba['experience'] == 'Junior (no experince)']
print('ТОП навыков hard_skills:')
display(df_ba_skills_Jun.hard_skills.str.split(', ').explode().value_counts())
print('ТОП навыков  soft_skills')
display(df_ba_skills_Jun.soft_skills.str.split(', ').explode().value_counts().head())
print('ТОП навыков  key_skills')
display(df_ba_skills_Jun.key_skills.str.split(', ').explode().value_counts().head(25))

print()

print('ТОП навыков необходимых Бизнес аналитику уровня ''Junior+ (1-3 years)'':')
print()
df_ba_skills_Jun = df_ba.loc[df_ba['experience'] == 'Junior+ (1-3 years)']
print('ТОП навыков hard_skills:')
display(df_ba_skills_Jun.hard_skills.str.split(', ').explode().value_counts())
print('ТОП навыков  soft_skills')
display(df_ba_skills_Jun.soft_skills.str.split(', ').explode().value_counts().head())
print('ТОП навыков  key_skills')
display(df_ba_skills_Jun.key_skills.str.split(', ').explode().value_counts().head(25))

print()

print('ТОП навыков необходимых Бизнес аналитику уровня ''Middle (3-6 years)'':')
df_ba_skills_Jun = df_ba.loc[df_ba['experience'] == 'Middle (3-6 years)']
print()
print('ТОП навыков hard_skills:')
display(df_ba_skills_Jun.hard_skills.str.split(', ').explode().value_counts())
print('ТОП навыков  soft_skills')
display(df_ba_skills_Jun.soft_skills.str.split(', ').explode().value_counts().head(10))
print('ТОП навыков  key_skills')
display(df_ba_skills_Jun.key_skills.str.split(', ').explode().value_counts().head(25))

print()

print('ТОП навыков необходимых Бизнес аналитику уровня ''Senior (6+ years)'':')
print()
df_ba_skills_Jun = df_ba.loc[df_ba['experience'] == 'Senior (6+ years)']
print('ТОП навыков hard_skills:')
display(df_ba_skills_Jun.hard_skills.str.split(', ').explode().value_counts())
print('ТОП навыков  soft_skills')
display(df_ba_skills_Jun.soft_skills.str.split(', ').explode().value_counts().head())
print('ТОП навыков  key_skills')
display(df_ba_skills_Jun.key_skills.str.split(', ').explode().value_counts().head(25))


# **Выводы:** из выведенной информации мы может сделать вывод, что для соискателей на позиции Бизнес аналитик необходимо владеть навыками работы с документацией, иметь развитиые коммуникативные навыки, умение вести переговоры, знание программного приложения confluence и иметь аналитическое мышление, знать SQL, а так же пакет MS Office.

# In[39]:


print('ТОП навыков необходимых Аналитика данных уровня ''Junior (no experince)'':')
print()
df_da_skills_Jun = df_da.loc[df_ba['experience'] == 'Junior (no experince)']
print('ТОП навыков hard_skills:')
display(df_da_skills_Jun.hard_skills.str.split(', ').explode().value_counts())
print('ТОП навыков  soft_skills')
display(df_da_skills_Jun.soft_skills.str.split(', ').explode().value_counts().head())
print('ТОП навыков  key_skills')
display(df_da_skills_Jun.key_skills.str.split(', ').explode().value_counts().head(25))

print()

print('ТОП навыков необходимых Аналитику уровня ''Junior+ (1-3 years)'':')
print()
df_da_skills_Jun = df_da.loc[df_ba['experience'] == 'Junior+ (1-3 years)']
print('ТОП навыков hard_skills:')
display(df_da_skills_Jun.hard_skills.str.split(', ').explode().value_counts())
print('ТОП навыков  soft_skills')
display(df_da_skills_Jun.soft_skills.str.split(', ').explode().value_counts().head())
print('ТОП навыков  key_skills')
display(df_da_skills_Jun.key_skills.str.split(', ').explode().value_counts().head(25))

print()

print('ТОП навыков необходимых Аналитику данных уровня ''Middle (3-6 years)'':')
df_da_skills_Jun = df_da.loc[df_ba['experience'] == 'Middle (3-6 years)']
print('ТОП навыков hard_skills:')
display(df_da_skills_Jun.hard_skills.str.split(', ').explode().value_counts())
print('ТОП навыков  soft_skills')
display(df_da_skills_Jun.soft_skills.str.split(', ').explode().value_counts().head())
print('ТОП навыков  key_skills')
display(df_da_skills_Jun.key_skills.str.split(', ').explode().value_counts().head(25))


print()

print('ТОП навыков необходимых Аналитику данных уровня ''Senior (6+ years)'':')
df_da_skills_Jun = df_da.loc[df_ba['experience'] == 'Senior (6+ years)']
print('ТОП навыков hard_skills:')
display(df_da_skills_Jun.hard_skills.str.split(', ').explode().value_counts())
print('ТОП навыков  soft_skills')
display(df_da_skills_Jun.soft_skills.str.split(', ').explode().value_counts().head())
print('ТОП навыков  key_skills')
display(df_da_skills_Jun.key_skills.str.split(', ').explode().value_counts().head(25))


# **Вывод:** из выведенной информации мы может сделать вывод, что для соискателей на позиции Аналитик данных необходимо знание языка программирование Python, хорошее значние библиотеки Pandas, знание программного приложения confluence, навыками работы с документацией, умение работать с приложением визуализации BI, хорошее значниеммуникативные навыки, умение вести переговоры и иметь аналитическое мышление. 

# **3.3. Определим какое количество вакансий Бизнес аналитика и какого грейда размещено на ресурсе hh.ru по городам и определим ТОП-15 городов по количеству предложений**

# In[40]:


#построим сводную таблицу распределения вакансий Бизнес аналитика по ТОП-20 городам
ba_sity_top = df_ba['area'].value_counts().reset_index().head(15)
print('ТОП-15 городов по кол-ву предложений для Бизнес аналитика')
display(ba_sity_top)

#построим сводную таблицу количества заведений по категориям и улицам
ba_sity_category = pd.pivot_table(df_ba, 
                                 index=['area', 'experience'],
                                 values= 'id',
                                aggfunc='count').sort_values(by='id', ascending = False).reset_index()
print()
print('Количество предложений по грейдам в ТОП-15 городов для Бизнес аналитика')
display(ba_sity_category)

ba_sity_top15_category = ba_sity_category[ba_sity_category['area'].isin(ba_sity_top['index'])]
display(ba_sity_top15_category.groupby(['area', 'experience']).agg({'id':'sum'}))


# In[41]:


#строим гистограмму отображающщую количество заведений в каждой категории
category = px.bar(ba_sity_top15_category.sort_values(by=['experience', 'id', 'area'], ascending = True).reset_index(),
                                 x='id', 
                                 y='area', 
                                 color='experience', 
                                 width=1000, 
                                 height=650,
                                 text ='id',
                                 title='ТОП-15 городов с предложениями для Бизнес аналитика')

#переименуем легенды графика
category.update_layout(xaxis_title = 'Кол-во размещенных вакансий Бизнес аналитика по городам',
                       yaxis_title = 'Город', title_x=0.5)


#определим направление текста
category.update_xaxes(tickangle=0)
category.show()


# **Посмотрим какое количество вакансий Аналитика данных и какого грейда размещено на ресурсе hh.ru по городам и определим ТОП-15 городов по количеству предложений**

# In[42]:


#построим сводную таблицу распределения вакансий Бизнес аналитика по ТОП-15 городам
da_sity_top = df_da['area'].value_counts().reset_index().head(15)
print('ТОП-15 городов по кол-ву предложений для Аналитика данных')
display(da_sity_top)

#построим сводную таблицу количества заведений по категориям и улицам
da_sity_category = pd.pivot_table(df_da, 
                                 index=['area', 'experience'],
                                 values= 'id',
                                aggfunc='count').sort_values(by='id', ascending = False).reset_index()
print()
print('Количество предложений по грейдам в ТОП-15 городов для Аналитика данных')
#display(da_sity_category)

da_sity_top15_category = da_sity_category[da_sity_category['area'].isin(ba_sity_top['index'])]
display(da_sity_top15_category.groupby(['area', 'experience']).agg({'id':'sum'}))


# In[43]:


#строим гистограмму отображающщую количество заведений в каждой категории
category_da = px.bar(da_sity_top15_category.sort_values(by=[ 'id'], ascending = True).reset_index(), #'area',
                                 x='id', 
                                 y='area', 
                                 color='experience', 
                                 width=1000, 
                                 height=650,
                                 text ='id',
                                 title='ТОП-15 городов с предложениями для Аналитика данных')

#переименуем легенды графика
category_da.update_layout(xaxis_title = 'Кол-во размещенных вакансий Аналитика данных по городам',
                        yaxis_title = 'Город', title_x=0.5)


#определим направление текста
category_da.update_xaxes(tickangle=0)
category_da.show()


# **Посмотрим какое количество вакансий Бизнес аналитика и какого грейда размещено на ресурсе hh.ru по работодателям и определим ТОП-15 работодателей по количеству предложений**

# In[44]:


#построим сводную таблицу распределения вакансий Бизнес аналитика по ТОП-15 работадателям
ba_emp_top = df_ba['employer'].value_counts().reset_index().head(15)
print('ТОП-15 работодателей по кол-ву предложений для Бизнес аналитика')
display(ba_emp_top)

#построим сводную таблицу количества заведений по категориям и улицам
ba_emp_category = pd.pivot_table(df_ba, 
                                 index=['employer', 'experience'],
                                 values= 'id',
                                aggfunc='count').sort_values(by='id', ascending = False).reset_index()
print()
print('Количество вакансий по грейдам в ТОП-15 работодателей для Бизнес аналитика')
display(ba_emp_category)

ba_emp_top15_category = ba_emp_category[ba_emp_category['employer'].isin(ba_emp_top['index'])]
ba_emp_top15_category_group = ba_emp_top15_category.groupby(['employer', 'experience']).agg({'id':'sum'})
display(ba_emp_top15_category_group)


# In[45]:


#строим гистограмму отображающщую количество заведений в каждой категории
category = px.bar(ba_emp_top15_category_group.sort_values(by=['id', 'employer', 'experience'], ascending = True).reset_index(),
                                 x='id', 
                                 y='employer', 
                                 color='experience', 
                                 width=950, 
                                 height=650,
                                 text ='id',
                                 title='ТОП-15 работодетелей с предложениями для Бизнес аналитика')

#переименуем легенды графика
category.update_layout(xaxis_title = 'Кол-во размещенных вакансий Бизнес аналитика по работадателям',
                       yaxis_title = 'Работодатель', title_x=0.5)


#определим направление текста
category.update_xaxes(tickangle=0)
category.show()


# **Посмотрим какое количество вакансий Аналитика данных и какого грейда размещено на ресурсе hh.ru по работодателям и определим ТОП-15 работодателей по количеству предложений**

# In[78]:


#построим сводную таблицу распределения вакансий Аналитик данных по ТОП-15 работодателям
da_emp_top = df_da['employer'].value_counts().reset_index().head(15)
print('ТОП-15 работодателей по кол-ву предложений для Аналитика данных')
display(da_emp_top)

#построим сводную таблицу количества заведений по категориям и улицам
da_emp_category = pd.pivot_table(df_da, 
                                 index=['employer', 'experience'],
                                 values= 'id',
                                 aggfunc='count').sort_values(by='id', ascending = False).reset_index()
print()
print('Количество предложений по грейдам в ТОП-15 городов для Аналитика данных')
display(da_emp_category)

da_emp_top15_category = da_emp_category[da_emp_category['employer'].isin(da_emp_top['index'])]
display(da_emp_top15_category.groupby(['employer', 'experience']).agg({'id':'sum'}))


# In[79]:


#строим гистограмму отображающщую количество заведений в каждой категории
category_da_emp = px.bar(da_emp_top15_category.sort_values(by=['id', 'employer', 'experience'], ascending = True).reset_index(),
                                 x='id', 
                                 y='employer', 
                                 color='experience', 
                                 width=1000, 
                                 height=650,
                                 text ='id',
                                 title='ТОП-15 работодателей с предложениями для Аналитика данных')

#переименуем легенды графика
category_da_emp.update_layout(xaxis_title = 'Кол-во размещенных вакансий Аналитика данных по работадателям',
                        yaxis_title = 'Работадатель', title_x=0.5)


#определим направление текста
category_da_emp.update_xaxes(tickangle=0)
category_da_emp.show()


# **Проведем анализ уровня дохода по вакансиям Бизнес аналитика и Аналитика данных**

# In[48]:


#сгруппируем данные по Бизнес аналитикам по грейду и уровню дохода (salary_from), 
#просмотрим распределение значений дохода: min, max, mean., и т.д.
print('Уровень дохода по полю salary_from')
display(df_ba.groupby('experience')['salary_from'].describe().reset_index(0).round(1))
fig = px.box(df_ba.sort_values('experience', ascending=True), 
             x=('experience'), 
             y='salary_from', 
             title = 'Распределение уровня дохода в зависимости от грейда у Бизнес аналитиков', 
             color = 'experience', points='all')
fig.update_layout(xaxis_title = 'Грейд',
                  yaxis_title = 'Уровень дохода')
fig.show()


print('Уровень дохода по полю salary_to')
display(df_ba.groupby('experience')['salary_to'].describe().reset_index(0).round(1))
fig = px.box(df_ba.sort_values('experience', ascending=True), 
             x=('experience'), y='salary_to', 
             title = 'Распределение уровня дохода в зависимости от грейда у Бизнес аналитиков',
             color = 'experience', points='all')
fig.update_layout(xaxis_title = 'Грейд',
                  yaxis_title = 'Уровень дохода')
fig.show()


# In[49]:


#Бизнес аналитик средний и медианный уровень дохода по городам в зависимости от грейда
df_ba_area_salary = pd.pivot_table(df_ba, 
                                 index=['area'],
                                 values= 'salary_to',
                                 columns= ['experience'],
                                 aggfunc=[np.mean],fill_value=0).reset_index().round()
display(df_ba_area_salary)

#Бизнес аналитик средний и медианный уровень дохода по работадателям в зависимости от грейда
df_ba_emp_salary = pd.pivot_table(df_ba, 
                                 index=['employer'],
                                 values= 'salary_to',
                                 columns= ['experience'],
                                 aggfunc=[np.mean],fill_value=0).reset_index().round()
display(df_ba_emp_salary)


# In[50]:


#Аналитик данных средний и меридианный уровень дохода по городам в зависимости от грейда
df_da_area_salary = pd.pivot_table(df_da, 
                                 index=['area'],
                                 values= 'salary_to',
                                 columns= ['experience'],
                                 aggfunc=[np.mean],fill_value=0).reset_index().round()
display(df_da_area_salary)

#Аналитик данных средний и медианный уровень дохода по работадателям в зависимости от грейда
df_da_emp_salary = pd.pivot_table(df_da, 
                                 index=['employer'],
                                 values= 'salary_to',
                                 columns= ['experience'],
                                 aggfunc=[np.mean],fill_value=0).reset_index().round()
display(df_da_emp_salary)


# In[51]:


#сгруппируем данные по Бизнес аналитикам по грейду и уровню дохода (salary_from), 
#просмотрим распределение значений дохода: min, max, mean., и т.д.
print('Уровень дохода по полю salary_from')
display(df_da.groupby('experience')['salary_from'].describe().reset_index(0).round(1))
fig = px.box(df_da.sort_values('experience', ascending=True), 
             x='experience', 
             y='salary_from', 
             title = 'Распределение уровня дохода в зависимости от грейда у Аналитика данных', 
             color = 'experience', points='all')
fig.update_layout(xaxis_title = 'Грейд',
                  yaxis_title = 'Уровень дохода')
fig.show()


print('Уровень дохода по полю salary_to')
display(df_da.groupby('experience')['salary_to'].describe().reset_index(0).round(1))
fig = px.box(df_da.sort_values('experience', ascending=True), 
            x=('experience'), 
            y='salary_to', 
            title = 'Распределение уровня дохода в зависимости от грейда у Аналитика данных', 
            color = 'experience', points='all')
fig.update_layout(xaxis_title = 'Грейд',
                  yaxis_title = 'Уровень дохода')
fig.show()


# **Проведем более детальное исследование вакансий Бизнес аналитика по грейдам в разрезе городов и работодателей**

# In[52]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Бизнес аналитик 
#отфильтруем по Junior(no experince)
df_ba_pivot_junior = df_ba.pivot_table(index=['area', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Junior (no experince)"').round()
top5_ba_area_junior = df_ba_pivot_junior['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Бизнес аналитика по городам для Junior(no experince): min , max, median, mean')
display(df_ba_pivot_junior)

print()
print('ТОП-5 предложений по зарплате для Бизнес аналитика по городам для начинающего специалиста Junior(no experince)')
display(top5_ba_area_junior) 


# In[53]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Бизнес аналитик 
#отфильтруем по Junior+ (1-3 years)
df_ba_pivot_junior3 = df_ba.pivot_table(index=['area', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Junior+ (1-3 years)"').round()
top5_ba_area_junior3 = df_ba_pivot_junior3['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Бизнес аналитика по городам для Junior+ (1-3 years): min , max, median, mean')
display(df_ba_pivot_junior3)

print()
print('ТОП-5 предложений по зарплате для Бизнес аналитика по городам для Junior+ (1-3 years)')
display(top5_ba_area_junior3) 


# In[54]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Бизнес аналитик 
#отфильтруем по Middle (3-6 years)
df_ba_pivot_middle = df_ba.pivot_table(index=['area', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Middle (3-6 years)"').round()
top5_ba_area_middle = df_ba_pivot_middle['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Бизнес аналитика по городам для Middle (3-6 years): min , max, median, mean')
display(df_ba_pivot_middle)

print()
print('ТОП-5 предложений по зарплате для Бизнес аналитика по городам для Middle (3-6 years)')
display(top5_ba_area_middle)


# In[55]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Бизнес аналитик 
#отфильтруем по Senior (6+ years)
df_ba_pivot_senior = df_ba.pivot_table(index=['area', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Senior (6+ years)"').round()
top5_ba_area_senior = df_ba_pivot_senior['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Бизнес аналитика по городам для Senior (6+ years): min , max, median, mean')
display(df_ba_pivot_senior)

print()
print('ТОП-5 предложений по зарплате для Бизнес аналитика по городам для начинающего специалиста Senior (6+ years)')
display(top5_ba_area_senior)


# In[56]:


#построим сводную таблицу с отображением среднего дохода по работадателям для вакансии Бизнес аналитик 
#отфильтруем по Junior(no experince)
df_ba_pivot_junior_emp = df_ba.pivot_table(index=['employer', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Junior (no experince)"').round()
top5_ba_emp_junior = df_ba_pivot_junior_emp['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Бизнес аналитика по работадателям для Junior(no experince): min , max, median, mean')
display(df_ba_pivot_junior_emp)

print()
print('ТОП-5 предложений по зарплате для Бизнес аналитика по  для Junior(no experince)')
display(top5_ba_emp_junior) 


# In[57]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Бизнес аналитик 
#отфильтруем по Junior+ (1-3 years)
df_ba_pivot_junior3_emp = df_ba.pivot_table(index=['employer', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Junior+ (1-3 years)"').round()
top5_ba_emp_junior3 = df_ba_pivot_junior3_emp['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Бизнес аналитика по работадателям для Junior+ (1-3 years): min , max, median, mean')
display(df_ba_pivot_junior3_emp)

print()
print('ТОП-5 предложений по зарплате для Бизнес аналитика по работадателям для Junior+ (1-3 years)')
display(top5_ba_emp_junior3) 


# In[58]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Бизнес аналитик 
#отфильтруем по Middle (3-6 years)
df_ba_pivot_middle_epm = df_ba.pivot_table(index=['employer', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Middle (3-6 years)"').round()
top5_ba_emp_middle = df_ba_pivot_middle_epm['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Бизнес аналитика по городам для Middle (3-6 years): min , max, median, mean')
display(df_ba_pivot_middle_epm)

print()
print('ТОП-5 предложений по зарплате для Бизнес аналитика по городам для Middle (3-6 years)')
display(top5_ba_emp_middle)


# In[59]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Бизнес аналитик 
#отфильтруем по Senior (6+ years)
df_ba_pivot_senior_emp = df_ba.pivot_table(index=['employer', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Senior (6+ years)"').round()
top5_ba_emp_senior = df_ba_pivot_senior_emp['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Бизнес аналитика по работадателям для Senior (6+ years): min , max, median, mean')
display(df_ba_pivot_senior_emp)

print()
print('ТОП-5 предложений по зарплате для Бизнес аналитика по работадателям для Senior (6+ years)')
display(top5_ba_emp_senior)


# **Проведем более детальное исследование вакансий Аналитика данных по грейдам в разрезе городов и работодателей**

# In[60]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Аналитик данных
#отфильтруем по Junior(no experince)
df_da_pivot_junior = df_da.pivot_table(index=['area', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Junior (no experince)"').round()
top5_da_area_junior = df_da_pivot_junior['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Аналитика данных по городам для Junior(no experince): min , max, median, mean')
display(df_da_pivot_junior)

print()
print('ТОП-5 предложений по зарплате для Аналитика данных по городам для начинающего специалиста Junior(no experince)')
display(top5_da_area_junior) 


# In[61]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Аналитик данных 
#отфильтруем по Junior+ (1-3 years)
df_da_pivot_junior3 = df_da.pivot_table(index=['area', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Junior+ (1-3 years)"').round()
top5_da_area_junior3 = df_da_pivot_junior3['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Аналитика данных по городам для Junior+ (1-3 years): min , max, median, mean')
display(df_da_pivot_junior3)

print()
print('ТОП-5 предложений по зарплате для Аналитика данных по городам для Junior+ (1-3 years)')
display(top5_da_area_junior3) 


# In[62]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Аналитика данных 
#отфильтруем по Middle (3-6 years)
df_da_pivot_middle = df_da.pivot_table(index=['area', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Middle (3-6 years)"').round()
top5_da_area_middle = df_da_pivot_middle['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Аналитика данных по городам для Middle (3-6 years): min , max, median, mean')
display(df_da_pivot_middle)

print()
print('ТОП-5 предложений по зарплате для Аналитика данных по городам для Middle (3-6 years)')
display(top5_da_area_middle)


# In[63]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Аналитика данных 
#отфильтруем по Senior (6+ years)
df_da_pivot_senior = df_da.pivot_table(index=['area', 'experience'],
                                values=['salary_from'],
                                aggfunc=[len, np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Senior (6+ years)"').round()
top5_da_area_senior = df_da_pivot_senior['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Аналитика данных по городам для Senior (6+ years): min , max, median, mean')
display(df_da_pivot_senior)

print()
print('ТОП-5 предложений по зарплате для Аналитика данных по городам для начинающего специалиста Senior (6+ years)')
display(top5_da_area_senior)


# In[64]:


#построим сводную таблицу с отображением среднего дохода по работадателям для вакансии Аналитик данных 
#отфильтруем по Junior(no experince)
df_da_pivot_junior_emp = df_da.pivot_table(index=['employer', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Junior (no experince)"').round()
top5_da_emp_junior = df_da_pivot_junior_emp['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Аналитика данных по работадателям для Junior(no experince): min , max, median, mean')
display(df_da_pivot_junior_emp)

print()
print('ТОП-5 предложений по зарплате для Аналитика данных по  для Junior(no experince)')
display(top5_da_emp_junior) 


# In[65]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Аналитика данных 
#отфильтруем по Junior+ (1-3 years)
df_da_pivot_junior3_emp = df_da.pivot_table(index=['employer', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Junior+ (1-3 years)"').round()
top5_da_emp_junior3 = df_da_pivot_junior3_emp['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Аналитика данных по работадателям для Junior+ (1-3 years): min , max, median, mean')
display(df_da_pivot_junior3_emp)

print()
print('ТОП-5 предложений по зарплате для Аналитика данных по работадателям для Junior+ (1-3 years)')
display(top5_da_emp_junior3) 


# In[66]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Аналитика данных 
#отфильтруем по Middle (3-6 years)
df_da_pivot_middle_epm = df_da.pivot_table(index=['employer', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Middle (3-6 years)"').round()
top5_da_emp_middle = df_da_pivot_middle_epm['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Аналитика данных по городам для Middle (3-6 years): min , max, median, mean')
display(df_da_pivot_middle_epm)

print()
print('ТОП-5 предложений по зарплате для Аналитика данных по городам для Middle (3-6 years)')
display(top5_da_emp_middle)


# In[67]:


#построим сводную таблицу с отображением среднего дохода по городам для вакансии Аналитика данных 
#отфильтруем по Senior (6+ years)
df_da_pivot_senior_emp = df_da.pivot_table(index=['employer', 'experience'],
                                values=['salary_from'],
                                aggfunc=[np.min, np.mean, np.median, np.max], 
                                fill_value = 0).query('experience == "Senior (6+ years)"').round()
top5_da_emp_senior = df_da_pivot_senior_emp['median'].sort_values(by='salary_from', ascending=False).head(5)
print('Предложений по зарплате для Аналитика данных по работадателям для Senior (6+ years): min , max, median, mean')
display(df_da_pivot_senior_emp)

print()
print('ТОП-5 предложений по зарплате для Аналитика данных по работадателям для Senior (6+ years)')
display(top5_da_emp_senior)


# **Вывод:** большая часть предложенных вакансий для Бизнес аналитиков и Аналитиков данных предлагается в Москве, и уровень дохода в среднем для данных специалистов так же больше в Москве.

# **Посмотреть распределение вакансий по датам публикации, есть ли какая то сезонность**

# In[68]:


df_ba['day_publication'] = df_ba['published_at'].dt.weekday
df_ba['month_publication'] = df_ba['published_at'].dt.month
df_ba['year_publication'] = df_ba['published_at'].apply(lambda x: x.strftime('%Y-%m-%d'))
df_ba.head()


# In[69]:


#сгруппируем количество вакансий Бизнес аналитикам по грейдам 
df_ba_cnt=df_ba.groupby(['day_publication', 'experience'])['id'].count().reset_index()
display(df_ba_cnt.sort_values(by='day_publication', ascending=True))


#для более наглядной визуализации строим гистограмму размещения вакансия по дням
category = px.bar(df_ba_cnt, x='day_publication', 
                                 y='id', 
                                 color='experience', 
                                 text ='id',
                                 title='Кол-во размещенных вакансий для Бизнес аналитика по дням недели')

#переименуем легенды графика
category.update_layout(xaxis_title = 'День',
                       yaxis_title = 'Кол-во вакансий Бизнес аналитика', title_x=0.5)


# In[70]:


#сгруппируем количество вакансий Бизнес аналитикам по грейдам и по месяцам
df_ba_cnt=df_ba.groupby(['month_publication', 'experience'])['id'].count().reset_index()
display(df_ba_cnt.sort_values(by='month_publication', ascending=True))


#для более наглядной визуализации строим гистограмму отображающщую количество вакансий каждого грейда
category = px.bar(df_ba_cnt, x='month_publication', 
                                 y='id', 
                                 color='experience', 
                                 text ='id',
                                 title='Кол-во размещенных вакансий для Бизнес аналитика по месяцам')

#переименуем легенды графика
category.update_layout(xaxis_title = 'месяц',
                       yaxis_title = 'Кол-во вакансий Бизнес аналитика', title_x=0.5)


# In[71]:


df_da['day_publication'] = df_ba['published_at'].dt.weekday
df_da['month_publication'] = df_ba['published_at'].dt.month
df_da['year_publication'] = df_da['published_at'].apply(lambda x: x.strftime('%Y-%m-%d'))
df_da.head()


# In[72]:


#сгруппируем количество вакансий Аналитика данных по грейдам по дням недели
df_da_cnt=df_da.groupby(['day_publication', 'experience'])['id'].count().reset_index()
display(df_da_cnt.sort_values(by='day_publication', ascending=True))


#для более наглядной визуализации строим гистограмму размещения вакансия по дням
category = px.bar(df_da_cnt, x='day_publication', 
                                 y='id', 
                                 color='experience', 
                                 text ='id',
                                 title='Кол-во размещенных вакансий для Аналитика данных по дням недели')

#переименуем легенды графика
category.update_layout(xaxis_title = 'День',
                       yaxis_title = 'Кол-во вакансий Аналитик данных', title_x=0.5)


# In[80]:


#сгруппируем количество вакансий Бизнес аналитикам по грейдам по месяцам
df_da_cnt=df_da.groupby(['month_publication', 'experience'])['id'].count().reset_index()
display(df_da_cnt.sort_values(by='month_publication', ascending=True))


#для более наглядной визуализации строим гистограмму размещения вакансия по месяцам
category = px.bar(df_da_cnt, x='month_publication', 
                                 y='id', 
                                 color='experience', 
                                 text ='id',
                                 title='Кол-во размещенных вакансий для Аналитика данных по месяцам')

#переименуем легенды графика
category.update_layout(xaxis_title = 'Месяц',
                       yaxis_title = 'Кол-во вакансий Аналитик данных', title_x=0.5)


# **Посмотреть распределение вакансий по типу занятости**

# In[74]:


#построим сводную таблицу с отображением кол-во вакансий Бизнес аналитик по типу занятости
df_ba_pivot_employ = df_ba.pivot_table(index=['employment'],
                                values=['salary_from'],
                                aggfunc=[len, np.mean], 
                                fill_value = 0).round()
print('Общее количество вакансий Бизнес аналитика по типу занятости с средним уровнем оплаты')
display(df_ba_pivot_employ)

print()
#построим сводную таблицу с отображением кол-во вакансий Бизнес аналитик по типу занятости и грейдам
df_ba_pivot_employ_exp = df_ba.pivot_table(index=['employment', 'experience'],
                                values=['salary_from'],
                                aggfunc=[len, np.mean], 
                                fill_value = 0).round()
print('Количество вакансий Бизнес аналитика по типу занятости в разрезе по грейдам с средним уровнем оплаты')
display(df_ba_pivot_employ_exp)


# In[75]:


#построим сводную таблицу с отображением кол-во вакансий Аналитик данных по типу занятости
df_da_pivot_employ = df_da.pivot_table(index=['employment'],
                                values=['salary_from'],
                                aggfunc=[len, np.mean], 
                                fill_value = 0).round()
print('Общее количество вакансий Аналитика данных по типу занятости с средним уровнем оплаты')
display(df_da_pivot_employ)

print()
#построим сводную таблицу с отображением кол-во вакансий Аналитик данных по типу занятости и грейдам
df_da_pivot_employ_exp = df_da.pivot_table(index=['employment', 'experience'],
                                values=['salary_from'],
                                aggfunc=[len, np.mean], 
                                fill_value = 0).round()
print('Количеств)о вакансий Аналитика данных по типу занятости в разрезе по грейдам с средним уровнем оплаты')
display(df_da_pivot_employ_exp)


# **Посмотреть распределение вакансий по формату работы: гибкий график, полный рабочий день, сменный график, удаленная работа**

# In[76]:


#построим сводную таблицу с отображением кол-во вакансий Бизнес аналитик по формату работы
df_ba_pivot_employ_schedule = df_ba.pivot_table(index=['schedule'],
                                values=['salary_from'],
                                aggfunc=[len, np.mean], 
                                fill_value = 0).round()
print('Общее количество вакансий Бизнес аналитика по формату работы с средним уровнем оплаты')
display(df_ba_pivot_employ_schedule)

print()
#построим сводную таблицу с отображением кол-во вакансий Бизнес аналитик по формату работы и грейдам
df_ba_pivot_employ_exp_schedule = df_ba.pivot_table(index=['schedule', 'experience'],
                                values=['salary_from'],
                                aggfunc=[len, np.mean], 
                                fill_value = 0).round()
print('Количество вакансий Бизнес аналитика по типу занятости в разрезе по грейдам с средним уровнем оплаты')
display(df_ba_pivot_employ_exp_schedule)


# In[77]:


#построим сводную таблицу с отображением кол-во вакансий Аналитик данных по формату работы
df_da_pivot_employ_schedule = df_da.pivot_table(index=['schedule'],
                                values=['salary_from'],
                                aggfunc=[len, np.mean], 
                                fill_value = 0).round()
print('Общее количество вакансий Аналитик данных по типу занятости с средним уровнем оплаты')
display(df_da_pivot_employ_schedule)

print()
#построим сводную таблицу с отображением кол-во вакансий Аналитик данных по формату работы и грейдам
df_da_pivot_employ_exp_schedule = df_da.pivot_table(index=['schedule', 'experience'],
                                values=['salary_from'],
                                aggfunc=[len, np.mean], 
                                fill_value = 0).round()
print('Количество вакансий Аналитик данных по типу занятости в разрезе по грейдам с средним уровнем оплаты')
display(df_da_pivot_employ_exp_schedule)


# **4. Общий вывод**
# <br>Из проведенного исследования мы видим, что предложения для соискателей для Бизнес аналитика больше в несколько раз, чем для Аналитика данных. Больше всего вакансий для аналитика данных было размещено в январе 2024 года, а спрос на Аналитиков данных больше в ноябре. 
# Для обоих специальностей требуется свой перечень необходимых навыков и умений работы в специализированных программах. Для Бизнес аналитика необходимы знания программы 1С, умение проводить Бизнес-Анализ, знание SQL и MS Office. Для Аналитика данных требуется знание в области SQL, Python, хорошее знание инструментов библиотеки Pandas, программ визуализации данных (BI), умение проводить. 
# Так же мы видим, что средний уровень дохода для Аналитиков данных на каждом грейде выше, чем у Бизнес аналитика.

# **Ссылка на презентацию:**  https://disk.yandex.ru/i/kE6liD-HV1xO9A
