Этот код представляет собой парсер вакансий с сайта HeadHunter, который анализирует требования и зарплаты в вакансиях, а затем сохраняет результаты в JSON-файл.

Как это работает:

Инициализация: Создается объект класса HHVacancyAnalyzer, который устанавливает базовый URL API HeadHunter и заголовок для запросов.

Получение вакансий: Метод get_vacancies отправляет запрос к API HeadHunter с заданными параметрами (название вакансии, регион, опыт работы, тип занятости, желаемая зарплата) и возвращает JSON-ответ.

Анализ вакансий: Метод analyze_vacancies обрабатывает полученные данные и выполняет следующие действия:

Подсчитывает общее количество найденных вакансий.Рассчитывает среднюю зарплату по вакансиям, если информация о зарплате доступна.Извлекает требования из описаний вакансий, подсчитывает количество каждого требования и рассчитывает процент встречаемости каждого требования.Сортирует требования по убыванию количества.Формирует словарь result с результатами анализа, включая общее количество вакансий, среднюю зарплату, список требований (с количеством и процентом встречаемости), топ-5 требований и количество уникальных требований.
Сохранение результатов: Метод save_results сохраняет результаты анализа в JSON-файл с уникальным именем, включающим название вакансии, дату и время запроса.

Запуск: В функции main запрашиваются параметры запроса у пользователя (название вакансии, регион, опыт работы, тип занятости, желаемая зарплата), запускается анализ вакансий, результаты выводятся на экран и сохраняются в файл.

Дополнительные возможности:

Обработка ошибок: В код добавлена обработка ошибок, возникающих при запросе к API HeadHunter.Фильтрация по критериям: Пользователь может задать дополнительные критерии фильтрации вакансий (опыт работы, тип занятости, желаемая зарплата).Дополнительная аналитика: В результате анализа предоставляется информация о топ-5 требованиях и количестве уникальных требований.
Как использовать:

Запустите скрипт.Введите необходимые параметры запроса (название вакансии, регион и т.д.).Результаты анализа будут выведены на экран и сохранены в JSON-файл.
