# main.py
import os
from modules.seriousness_checker import SeriousnessChecker
from modules.ime_checker import IMEChecker
from modules.expectedness_checker import ExpectednessChecker
from modules.causality_checker import CausalityChecker
from modules.missing_info_checker import MissingInfoChecker

def extract_adverse_events(text):
    """Извлекает нежелательные явления из текста с улучшенным поиском"""
    # Расширенный список медицинских терминов
    common_events = [
        # Кардиологические
        'инфаркт миокарда', 'ишемия миокарда', 'перикардиальный выпот', 
        'тромбоз коронарных артерий', 'артериальный тромбоз', 'тромбоэмболия',
        'атриовентрикулярная блокада', 'желудочковые экстрасистолы', 'сердцебиение',
        'удлинение интервала qt', 'артериальная гипертензия', 'хсн',
        'суправентрикулярная тахикардия', 'венозная тромбоэмболия',
        'артериальная тромбоэмболия', 'тромбоз глубоких вен', 'тэла',
        
        # Неврологические
        'психотическое расстройство', 'галлюцинации', 'гипестезия', 'тремор',
        'летаргия', 'периферическая нейропатия', 'головокружение', 'головная боль',
        'сонливость', 'заторможенность', 'инсульт', 'синкопе', 
        'гипертензивная энцефалопатия',
        
        # Общие серьезные
        'смерть', 'летальный', 'погиб', 'умер', 'госпитализирован', 
        'реанимация', 'угроза жизни'
    ]
    
    found_events = []
    text_lower = text.lower()
    
    for event in common_events:
        if event in text_lower:
            found_events.append(event)
    
    return found_events if found_events else ['неизвестное событие']

def main():
    print("🚀 ФАРМАКОНАДЗОРНЫЙ АССИСТЕНТ v5.0 - ПОЛНАЯ ВЕРСИЯ")
    print("=" * 70)
    
    # Создаем проверяльщики
    seriousness_checker = SeriousnessChecker()
    ime_checker = IMEChecker()
    expectedness_checker = ExpectednessChecker()
    causality_checker = CausalityChecker()
    missing_info_checker = MissingInfoChecker()
    
    # Показываем доступные препараты
    available_drugs = expectedness_checker.get_available_drugs()
    print(f"💊 Препараты в базе: {', '.join(available_drugs)}")
    
    # Проверяем все 6 кейсов
    for i in range(1, 7):
        filename = f"data/cases/case_{i}.txt"
        
        if os.path.exists(filename):
            # Читаем файл
            with open(filename, 'r', encoding='utf-8') as f:
                case_text = f.read().strip()
            
            # Извлекаем нежелательные явления
            adverse_events = extract_adverse_events(case_text)
            
            # Выводим результат
            print(f"\n{'='*70}")
            print(f"📋 КЕЙС {i}:")
            print(f"📄 Текст: {case_text}")
            print(f"🔍 Выявленные события: {', '.join(adverse_events)}")
            
            # Проверяем недостающую информацию
            missing_info_result = missing_info_checker.check_missing_information(case_text, adverse_events[0] if adverse_events else '')
            print(f"📊 Полнота информации: {missing_info_result['completeness_score']}%")
            
            if missing_info_result['missing_info']:
                print("❌ Отсутствует информация:")
                for question in missing_info_result['questions']:
                    print(f"   - {question}")
            
            # Анализируем каждое событие
            for event in adverse_events:
                print(f"\n   📍 Анализ события: '{event.upper()}'")
                
                # Серьезность
                seriousness_result = seriousness_checker.check_seriousness(case_text)
                seriousness_status = "🔴 СЕРЬЕЗНЫЙ" if seriousness_result['is_serious'] else "🟢 НЕ серьезный"
                print(f"   ⚠️  Серьезность: {seriousness_status}")
                if seriousness_result['flags']:
                    print(f"      Причины: {', '.join(seriousness_result['flags'])}")
                
                # IME значимость
                ime_result = ime_checker.check_ime_significance(event)
                ime_status = "🔴 ЗНАЧИМЫЙ" if ime_result['is_significant'] else "🟢 НЕ значимый"
                print(f"   🏥 IME значимость: {ime_status}")
                if ime_result['found_terms']:
                    for term in ime_result['found_terms']:
                        print(f"      Найден IME: '{term['russian']}' → {term['english']}")
                
                # Предвиденность
                expectedness_result = expectedness_checker.check_expectedness(case_text, event)
                expectedness_status = "🟢 ПРЕДВИДЕННЫЙ" if expectedness_result['is_expected'] else "🔴 НЕПРЕДВИДЕННЫЙ"
                print(f"   📋 Предвиденность: {expectedness_status}")
                print(f"      Препарат: {expectedness_result['drug']}")
                print(f"      Причина: {expectedness_result['reason']}")
                if 'frequency' in expectedness_result:
                    print(f"      Частота: {expectedness_result['frequency']}")
                
                # Причинно-следственная связь
                causality_result = causality_checker.analyze_causality(case_text, event)
                print(f"   🔗 Причинность: {causality_result['level']}")
                print(f"      Обоснование: {causality_result['reasoning']}")
                    
        else:
            print(f"\n❌ Файл {filename} не найден!")
    
    print(f"\n{'='*70}")
    print("🎉 АНАЛИЗ ЗАВЕРШЕН! Все 5 модулей работают!")
    print("📈 Функциональность полная: Серьезность, IME, Предвиденность, Причинность, Полнота данных")

if __name__ == "__main__":
    main()
