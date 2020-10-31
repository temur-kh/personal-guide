# Проект "Персональный гид" - MADE Mail.ru Group

## Запуск

Локально можно запустить все с помощью следующей команды:
```
 docker-compose -f docker-compose.dev.yml up -d --build
```

Перезапуск с изменениями проекта также происходит по вышеуказанной команде.

## Сайт

http://18.188.11.56:9090/ - здесь можно посмотреть результат.
Пока нет ssl сертификата, так как не получается взять доменное имя на freenom.com. Попробую потом еще раз.

## Подключение к MongoDB

- IP: 18.188.11.56
- PORT: 27017
- USERNAME: user
- PASSWORD: personalguide2020
- DATABASE: database

Методы подключения:
1. Python клиент
2. Mongo shell
3. MongoDB Compass Community
