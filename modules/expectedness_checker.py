# modules/expectedness_checker.py
import json
import os

class ExpectednessChecker:
    def __init__(self):
        self.smpc_database = self._load_smpc_database()
    
    def _load_smpc_database(self):
        """Загружает базу данных по препаратам"""
        try:
            with open('knowledge/smpc_database.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Файл базы препаратов не найден!")
            return {}
    
    def extract_drug_name(self, text):
        """
        Извлекает название препарата из текста
        Возвращает первое найденное название препарата
        """
        text_lower = text.lower()
        
        # Ищем упоминания препаратов
        for drug_name in self.smpc_database.keys():
            if drug_name.lower() in text_lower:
                return drug_name
        
        # Если не нашли - возвращаем最常见的 препарат
        return "Препарат А"
    
    def check_expectedness(self, text, adverse_event):
        """
        Проверяет, является ли побочный эффект предвиденным для препарата
        """
        drug_name = self.extract_drug_name(text)
        
        if drug_name not in self.smpc_database:
            return {
                'is_expected': False,
                'reason': f"Препарат '{drug_name}' не найден в базе",
                'drug': drug_name
            }
        
        drug_info = self.smpc_database[drug_name]
        adverse_event_lower = adverse_event.lower()
        
        # Проверяем прямое совпадение
        for expected_effect, effect_info in drug_info['expected_effects'].items():
            if expected_effect.lower() == adverse_event_lower:
                return {
                    'is_expected': True,
                    'reason': f"Прямое указание в ИМП",
                    'drug': drug_name,
                    'effect_type': effect_info['type'],
                    'frequency': effect_info['frequency']
                }
        
        # Проверяем вхождение в симптомокомплекс
        for expected_effect, effect_info in drug_info['expected_effects'].items():
            if effect_info['type'] == 'symptom_complex':
                if adverse_event_lower in [symptom.lower() for symptom in effect_info.get('includes', [])]:
                    return {
                        'is_expected': True,
                        'reason': f"Входит в симптомокомплекс '{expected_effect}'",
                        'drug': drug_name,
                        'effect_type': effect_info['type'],
                        'frequency': effect_info['frequency'],
                        'parent_complex': expected_effect
                    }
        
        return {
            'is_expected': False,
            'reason': "Не описано в ИМП",
            'drug': drug_name
        }
    
    def get_available_drugs(self):
        """Возвращает список препаратов в базе"""
        return list(self.smpc_database.keys())

# Тестирование модуля
if __name__ == "__main__":
    checker = ExpectednessChecker()
    
    print("🧪 Тестирование модуля предвиденности:")
    print("=" * 50)
    
    test_cases = [
        {
            "text": "Пациент принимал Препарат А, появилась головная боль",
            "event": "головная боль"
        },
        {
            "text": "После приема Препарата Б возникла сыпь на коже", 
            "event": "сыпь"
        },
        {
            "text": "На фоне лечения Препаратом А отмечался зуд",
            "event": "зуд"
        },
        {
            "text": "Прием неизвестного препарата вызвал боль в животе",
            "event": "боль в животе"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        result = checker.check_expectedness(test_case["text"], test_case["event"])
        status = "🟢 ПРЕДВИДЕННЫЙ" if result['is_expected'] else "🔴 НЕПРЕДВИДЕННЫЙ"
        
        print(f"\nТест {i}: {status}")
        print(f"Препарат: {result['drug']}")
        print(f"Событие: {test_case['event']}")
        print(f"Причина: {result['reason']}")
        if 'frequency' in result:
            print(f"Частота: {result['frequency']}")
