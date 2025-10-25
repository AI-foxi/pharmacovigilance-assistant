import os

print("=== СОЗДАНИЕ ПРОЕКТА ===")

# Создаем папки
folders = ['data/cases', 'modules']
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✅ Папка: {folder}")

# Создаем обязательные файлы
files = {
    'main.py': '''
print("🚀 Фармаконадзорный ассистент запущен!")
print("Добавь свои кейсы в data/cases/")
''',
    
    'modules/__init__.py': '#',
    
    'modules/seriousness.py': '''
class SeriousnessChecker:
    def check(self, text):
        serious = any(word in text.lower() for word in 
                     ['госпитализ', 'смерть', 'реанимация'])
        return serious
'''
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Файл: {path}")

print("✅ СТРУКТУРА СОЗДАНА!")