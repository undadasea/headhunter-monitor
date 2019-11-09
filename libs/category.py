"""
Library aims to search for multiple patterns in jobs descriprion.
Vacancy is a json object from API of headhunter website 'https://github.com/hhru/api'
"""

# CATEGORY CATALOGUE

jobs = {'engineer': ["engineer", "инженер", "develop", "разработчик", "алгоритм", "algorithm"], \
        'manager': ["manager", "менеджер"], \
        'admin':["admin", "администратор"], \
        'designer': ["designer", "дизайнер", "photoshop"],
        'director': ["director", "директор"]
        }

developer_types = {'bigdata engineer': ["data engineer", "spark", "hadoop"],
                   'data scientist': ["data scientist", "machine learning", "машинное обучение"],
                   'QA engineer': ["QA", "testing", "тестировани"],
                   'web developer': ["web developer", "javascript"]
                   }

developer_experience = {'intern' : ["intern", "стажер"],
                        'junior' : ["junior", "младший специалист"],
                        'middle' : ["middle"],
                        'senior' : ["senior", "старший"],
                        'teamlead' : ["teamlead", "lead", "тимлид", "ведущий инженер", "ведущий разработчик"]
                       }

def category(categories, vacancy):
    fields = [vacancy['name'], vacancy['snippet']['requirement'], vacancy['snippet']['responsibility']]
    for category in categories:
        hints = categories[category]
        for field in fields:
            for hint in hints:
                if field.lower().find(hint.lower()) >= 0:
                    return category
    return "No Match"
