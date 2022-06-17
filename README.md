Тестовое задание
===

> Если возникают вопросы, то их можно (нужно) задавать.

Реализовать `CRUD` приложения для `клиентов`, [спецификация](/openapi.yaml)

# Уровни сложности

## Болгарский перец (Обычный) &#x1FAD1;

- Реализовать спецификацию **полностью**
- Валидация
- [Вложенное обновление](/INNER_UPDATE.md)
- Мягкое удаление (soft delete)

## Калифорнийский чили &#127798;

- Сортировка по нескольким полям с разными направлениями
- Поиск по текстовым полям вложенных моделей
- Возможность в листинге фильтровать по доходу, количеству детей и типу образования

## Чипотле &#127798; &#127798;

- Docker + Docker Compose
- Очередь событий + потребители, которые выводят в консоль ФИО клиента и операцию (Создание, обновление и удаление)

## Табаско &#127798; &#127798; &#127798;

- Динамическая фильтрация в листинге
- Потребитель ведет лог действий в БД + АПИ которое позволяет посмотреть, какие действия происходили и какие изменения были совершенны(разница в состоянии, до, после) 

# Dotnet

## Рекомендуемый стек
 - dotnet Core 6+
 - EF

### Задачка для пытливых умов (Частичное обновление)

- Если пришло поле - обновляем
- Если не пришло - ничего не делаем
- Если пришел `null` - удаляем


# Node.js

Частичное обновление обязательно.

### Рекомендуемы стек

- node > 14
- AdonisJS | NestJS

