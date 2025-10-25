# main.py
import os
from modules.seriousness_checker import SeriousnessChecker
from modules.ime_checker import IMEChecker

def main():
    print("🚀 ФАРМАКОНАДЗОРНЫЙ АССИСТЕНТ v2.0")
    print("=" * 60)
    
    # Создаем проверяльщики
    seriousness_checker = SeriousnessChecker()
    ime_checker = IMEChecker()
    
    # Проверяем все 6 кейсов
    for i in range(1, 7):
        filename = f"data/cases/case_{i}.txt"
        
        if os.path.exists(filename):
            # Читаем файл
            with open(filename, 'r', encoding='utf-8') as f:
                case_text = f.read().strip()
            
            # Анализируем серьезность
            seriousness_result = seriousness_checker.check_seriousness(case_text)
            
            # Анализируем IME значимость
            ime_result = ime_checker.check_ime_significance(case_text)
            
            # Выводим результат
            print(f"\n📋 КЕЙС {i}:")
            print(f"📄 Текст: {case_text}")
            
            # Серьезность
            seriousness_status = "🔴 СЕРЬЕЗНЫЙ" if seriousness_result['is_serious'] else "🟢 НЕ серьезный"
            print(f"⚠️  Серьезность: {seriousness_status}")
            if seriousness_result['flags']:
                print(f"   Причины: {', '.join(seriousness_result['flags'])}")
            
            # IME значимость
            ime_status = "🔴 ЗНАЧИМЫЙ" if ime_result['is_significant'] else "🟢 НЕ значимый"
            print(f"🏥 IME значимость: {ime_status}")
            if ime_result['found_terms']:
                for term in ime_result['found_terms']:
                    print(f"   Найден IME: '{term['russian']}' → {term['english']}")
                    
        else:
            print(f"\n❌ Файл {filename} не найден!")
    
    print("\n" + "=" * 60)
    print("📊 АНАЛИЗ ЗАВЕРШЕН!")

if __name__ == "__main__":
    main()
