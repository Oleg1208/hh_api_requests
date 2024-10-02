import requests
import json
from collections import Counter
import datetime

class HHVacancyAnalyzer:
    """Класс для анализа вакансий с HeadHunter."""
    def __init__(self):
        # Базовый URL для API HeadHunter
        self.base_url = "https://api.hh.ru/vacancies"
        # Заголовок для запросов
        self.headers = {"User-Agent": "VacancyAnalyzer/1.0"}

    def get_vacancies(self, query, area="1", experience="", employment="", salary=""):
        """Получает вакансии с API HeadHunter."""
        params = {
            "text": query,
            "area": area,
            "experience": experience,
            "employment": employment,
            "salary": salary,
            "per_page": 100  # Максимальное количество вакансий на страницу
        }
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API HeadHunter: {e}")
            return None

    def parse_requirements(self, description):
        """Извлекает требования из описания вакансии."""
        # Здесь можно улучшить парсинг, используя более сложные методы обработки текста
        return [req.strip().lower() for req in description.split() if len(req) > 2]

    def analyze_vacancies(self, query, area="1", experience="", employment="", salary=""):
        """Анализирует вакансии и возвращает результаты."""
        data = self.get_vacancies(query, area, experience, employment, salary)
        if data is None:
            return None
        vacancies = data['items']
        total_vacancies = len(vacancies)
        # Расчет средней зарплаты
        salaries = [v['salary']['from'] for v in vacancies if v.get('salary') and v['salary'].get('from')]
        avg_salary = sum(salaries) / len(salaries) if salaries else 0
        # Сбор всех требований
        all_requirements = []
        for vacancy in vacancies:
            description = vacancy.get('snippet', {}).get('requirement', '')
            if description:
                requirements = self.parse_requirements(description)
                all_requirements.extend(requirements)
        # Подсчет требований
        req_count = Counter(all_requirements)
        # Расчет процентов для требований
        req_percentage = {req: (count / total_vacancies) * 100 for req, count in req_count.items()}
        # Сортировка требований по убыванию
        sorted_req = sorted(req_count.items(), key=lambda x: x[1], reverse=True)
        # Формирование результата
        result = {
            "query": query,
            "total_vacancies": total_vacancies,
            "average_salary": round(avg_salary, 2),
            "requirements": {
                "count": dict(sorted_req),
                "percentage": {k: round(v, 2) for k, v in req_percentage.items()}
            }
        }
        # Дополнительная аналитика
        result["top_5_requirements"] = dict(sorted_req[:5])
        result["unique_requirements"] = len(req_count)
        return result

    def save_results(self, result, query):
        """Сохраняет результаты в JSON файл."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{query.replace(' ', '_')}_analysis_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"Результаты сохранены в файл: {filename}")

def main():
    analyzer = HHVacancyAnalyzer()
    # Запрос параметров у пользователя
    query = input("Введите название вакансии: ")
    area = input("Введите ID региона (по умолчанию 1 - Москва): ") or "1"
    experience = input("Введите опыт работы (noExperience, between1And3, between3And6, moreThan6): ") or ""
    employment = input("Введите тип занятости (full, part, project, volunteer): ") or ""
    salary = input("Введите желаемую зарплату: ") or ""
    # Анализ вакансий
    result = analyzer.analyze_vacancies(query, area, experience, employment, salary)
    if result:
        # Вывод результатов на экран
        print("nРезультаты анализа:")
        print(f"Всего вакансий: {result['total_vacancies']}")
        print(f"Средняя зарплата: {result['average_salary']} руб.")
        print("nТоп-5 требований:")
        for req, count in result['top_5_requirements'].items():
            print(f"{req}: {count} раз")
        print(f"nУникальных требований: {result['unique_requirements']}")
        # Сохранение результатов в файл
        analyzer.save_results(result, query)
    else:
        print("Не удалось получить данные для анализа.")

if __name__ == "__main__":
    main()
