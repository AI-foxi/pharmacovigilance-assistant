# main.py - Основной файл проекта
import os
from modules.seriousness_checker import SeriousnessChecker

def main():
    print("🚀 Pharmacovigilance AI Assistant")
    print("Repository: https://github.com/Al-foxi/pharmacovigilance-assistant")
    
    # Проверяем структуру
    if not os.path.exists('data/cases'):
        os.makedirs('data/cases')
        print("✅ Created data/cases folder")
        print("💡 Please add your case files: case_1.txt ... case_6.txt")
        return
    
    # Загружаем кейсы
    cases = []
    for i in range(1, 7):
        filename = f'data/cases/case_{i}.txt'
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                cases.append(f.read())
            print(f"✅ Loaded: {filename}")
        else:
            print(f"❌ Missing: {filename}")
            cases.append("")
    
    # Анализируем
    checker = SeriousnessChecker()
    print("\n📊 Analysis Results:")
    
    for i, case_text in enumerate(cases, 1):
        if case_text:
            result = checker.check_seriousness(case_text)
            status = "SERIOUS" if result['is_serious'] else "not serious"
            print(f"Case {i}: {status} - Flags: {result['flags']}")

if __name__ == "__main__":
    main()