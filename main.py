# main.py
import os
from modules.seriousness_checker import SeriousnessChecker

def main():
    print("🚀 ФАРМАКОНАДЗОРНЫЙ АССИСТЕНТ")
    print("=" * 50)
    
    # Создаем проверяльщик серьезности
    checker = SeriousnessChecker()
    
    # Проверяем все 6 кейсов
    for i in range(1, 7):
        filename = f"data/cases/case_{i}.txt"
        
        if os.path.exists(filename):
            # Читаем файл
            with open(filename, 'r', encoding='utf-8') as f:
                case_text = f.read().strip()
            
            # Анализируем серьезность
            result = checker.check_seriousness(case_text)
            
            # Выводим результат
            status = "🔴 СЕРЬЕЗНЫЙ" if result['is_serious'] else "🟢 НЕ серьезный"
            print(f"\nКейс {i}: {status}")
            print(f"📄 Текст: {case_text}")
            
            if result['flags']:
                print(f"⚠️  Причины: {', '.join(result['flags'])}")
            else:
                print("✅ Серьезных критериев не найдено")
                
        else:
            print(f"\n❌ Файл {filename} не найден!")
    
    print("\n" + "=" * 50)
    print("📊 АНАЛИЗ ЗАВЕРШЕН!")

if __name__ == "__main__":
    main()