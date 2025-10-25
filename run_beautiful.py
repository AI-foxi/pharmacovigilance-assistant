# run_beautiful.py - КРАСИВЫЙ ЗАПУСК
import os
import time
from modules.seriousness_checker import SeriousnessChecker
from modules.ime_checker import IMEChecker
from modules.expectedness_checker import ExpectednessChecker
from modules.causality_checker import CausalityChecker
from modules.missing_info_checker import MissingInfoChecker

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║    🏥  ФАРМАКОНАДЗОРНЫЙ АНАЛИЗАТОР  🏥                      ║")
    print("║         AI Assistant for Pharmacovigilance                  ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    time.sleep(1)

def loading_animation(text):
    print(f"{Colors.BLUE}{Colors.BOLD}🔄 {text}", end="", flush=True)
    for i in range(3):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print(f" ✅{Colors.END}")

def extract_adverse_events(text):
    common_events = [
        'головная боль', 'тошнота', 'сыпь', 'зуд', 'крапивница', 
        'отек', 'диарея', 'головокружение', 'судороги', 'боль в животе',
        'анафилактический шок', 'лихорадка', 'рвота', 'смерть', 'летальный',
        'погиб', 'умер', 'скончался', 'госпитализирован', 'реанимация'
    ]
    
    found_events = []
    text_lower = text.lower()
    
    for event in common_events:
        if event in text_lower:
            found_events.append(event)
    
    return found_events if found_events else ['неизвестное событие']

def main():
    print_logo()
    
    # Инициализация с анимацией
    print(f"{Colors.BOLD}🎯 ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ...{Colors.END}\n")
    
    loading_animation("Загрузка модуля серьезности")
    seriousness_checker = SeriousnessChecker()
    
    loading_animation("Загрузка IME анализатора")
    ime_checker = IMEChecker()
    
    loading_animation("Загрузка проверки предвиденности")
    expectedness_checker = ExpectednessChecker()
    
    loading_animation("Загрузка оценки причинности")
    causality_checker = CausalityChecker()
    
    loading_animation("Загрузка контроля данных")
    missing_info_checker = MissingInfoChecker()
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✨ СИСТЕМА ГОТОВА К РАБОТЕ!{Colors.END}\n")
    time.sleep(1)
    
    # Анализ кейсов
    print(f"{Colors.PURPLE}{Colors.BOLD}📂 АНАЛИЗ КЕЙСОВ:{Colors.END}\n")
    
    for i in range(1, 7):
        filename = f"data/cases/case_{i}.txt"
        
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                case_text = f.read().strip()
            
            adverse_events = extract_adverse_events(case_text)
            
            print(f"{Colors.CYAN}{Colors.BOLD}┌──────────────── КЕЙС {i} ────────────────┐{Colors.END}")
            print(f"{Colors.YELLOW}📄 {case_text}{Colors.END}")
            print(f"{Colors.BLUE}🔍 События: {', '.join(adverse_events)}{Colors.END}")
            
            # Проверка полноты данных
            missing_info = missing_info_checker.check_missing_information(case_text, adverse_events[0] if adverse_events else '')
            score_color = Colors.GREEN if missing_info['completeness_score'] > 70 else Colors.YELLOW if missing_info['completeness_score'] > 40 else Colors.RED
            print(f"{Colors.PURPLE}📊 Полнота данных: {score_color}{missing_info['completeness_score']}%{Colors.END}")
            
            if missing_info['missing_info']:
                print(f"{Colors.YELLOW}💡 Рекомендуется уточнить:{Colors.END}")
                for question in missing_info['questions'][:2]:
                    print(f"   • {question}")
            
            # Анализ каждого события
            for event in adverse_events:
                print(f"\n{Colors.GREEN}{Colors.BOLD}📋 Анализ: {event.upper()}{Colors.END}")
                
                # Серьезность
                seriousness = seriousness_checker.check_seriousness(case_text)
                serious_icon = "🔴" if seriousness['is_serious'] else "🟢"
                serious_color = Colors.RED if seriousness['is_serious'] else Colors.GREEN
                print(f"   {serious_icon} {serious_color}Серьезность: {seriousness['is_serious']}{Colors.END}")
                if seriousness['flags']:
                    print(f"      {Colors.YELLOW}Факторы: {', '.join(seriousness['flags'])}{Colors.END}")
                
                # IME
                ime_result = ime_checker.check_ime_significance(event)
                ime_icon = "🔴" if ime_result['is_significant'] else "🟢"
                ime_color = Colors.RED if ime_result['is_significant'] else Colors.GREEN
                print(f"   {ime_icon} {ime_color}IME значимость: {ime_result['is_significant']}{Colors.END}")
                if ime_result['found_terms']:
                    for term in ime_result['found_terms']:
                        print(f"      {Colors.BLUE}🏷️  {term['russian']} → {term['english']}{Colors.END}")
                
                # Предвиденность
                expectedness = expectedness_checker.check_expectedness(case_text, event)
                expected_icon = "🟢" if expectedness['is_expected'] else "🔴"
                expected_color = Colors.GREEN if expectedness['is_expected'] else Colors.RED
                print(f"   {expected_icon} {expected_color}Предвиденность: {expectedness['is_expected']}{Colors.END}")
                print(f"      {Colors.CYAN}💊 {expectedness['drug']}{Colors.END}")
                print(f"      {Colors.PURPLE}📝 {expectedness['reason']}{Colors.END}")
                
                # Причинность
                causality = causality_checker.analyze_causality(case_text, event)
                causality_color = Colors.RED if "Определенная" in causality['level'] else Colors.YELLOW if "Вероятная" in causality['level'] else Colors.BLUE
                print(f"   🔗 {causality_color}Причинность: {causality['level']}{Colors.END}")
                print(f"      {Colors.CYAN}💭 {causality['reasoning']}{Colors.END}")
            
            print(f"{Colors.CYAN}{Colors.BOLD}└──────────────────────────────────────────┘{Colors.END}\n")
            time.sleep(2)
                    
        else:
            print(f"{Colors.RED}❌ Файл {filename} не найден!{Colors.END}")
    
    print(f"{Colors.GREEN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                     🎉 АНАЛИЗ ЗАВЕРШЕН!                     ║")
    print("║           Все 5 модулей успешно проанализированы            ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

if __name__ == "__main__":
    main()
