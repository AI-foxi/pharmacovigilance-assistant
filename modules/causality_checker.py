# modules/causality_checker.py
import re
from datetime import datetime

class CausalityChecker:
    def analyze_causality(self, text, adverse_event):
        """
        Анализирует причинно-следственную связь по шкале ВОЗ
        Возвращает: {'level': 'Определенная/Вероятная/...', 'reasoning': 'обоснование'}
        """
        text_lower = text.lower()
        event_lower = adverse_event.lower()
        
        # Извлекаем факты из текста
        facts = self._extract_facts(text_lower, event_lower)
        
        # Применяем алгоритм ВОЗ
        causality_level = self._apply_who_algorithm(facts)
        
        return {
            'level': causality_level,
            'reasoning': self._generate_reasoning(causality_level, facts),
            'facts': facts
        }
    
    def _extract_facts(self, text, event):
        """Извлекает факты для оценки причинности"""
        facts = {
            'time_relationship': self._check_time_relationship(text),
            'dechallenge': self._check_dechallenge(text, event),
            'rechallenge': self._check_rechallenge(text),
            'alternative_causes': self._check_alternative_causes(text),
            'known_effect': self._check_known_effect(text, event),
            'drug_mentioned': self._check_drug_mention(text)
        }
        return facts
    
    def _check_time_relationship(self, text):
        """Проверяет временную связь"""
        time_patterns = [
            r'через\s+(\d+)\s*(час|день|недел)',
            r'после\s+приема',
            r'на\s+фоне\s+лечения',
            r'при\s+приеме'
        ]
        
        for pattern in time_patterns:
            if re.search(pattern, text):
                return "есть"
        return "нет данных"
    
    def _check_dechallenge(self, text, event):
        """Проверяет результат отмены препарата"""
        improvement_terms = [
            'улучшение', 'исчезли', 'прошли', 'купирова', 'нормализова',
            'регресс', 'прекратил', 'выздоровел'
        ]
        
        withdrawal_terms = ['отмен', 'прекратил', 'перестал']
        
        # Проверяем улучшение после отмены
        has_withdrawal = any(term in text for term in withdrawal_terms)
        has_improvement = any(term in text for term in improvement_terms)
        
        if has_withdrawal and has_improvement:
            return "положительная"
        elif has_withdrawal and not has_improvement:
            return "отрицательная"
        else:
            return "нет данных"
    
    def _check_rechallenge(self, text):
        """Проверяет данные о повторном назначении"""
        rechallenge_terms = [
            'повторно', 'снова', 'рецидив', 'возобновил'
        ]
        
        if any(term in text for term in rechallenge_terms):
            return "есть"
        return "нет данных"
    
    def _check_alternative_causes(self, text):
        """Проверяет альтернативные причины"""
        alternative_patterns = [
            r'на\s+фоне\s+([а-я]+)\s+заболеван',  # на фоне другого заболевания
            r'сопутствующ',  # сопутствующие заболевания
            r'одновременно\s+принимал',  # другие препараты
            r'в\s+анамнезе'  # история болезни
        ]
        
        for pattern in alternative_patterns:
            if re.search(pattern, text):
                return "есть"
        return "нет данных"
    
    def _check_known_effect(self, text, event):
        """Проверяет известность эффекта"""
        # В реальном проекте здесь была бы проверка по базе знаний
        known_effects = [
            'аллерги', 'анафилаксия', 'сыпь', 'тошнота', 'головная боль',
            'крапивница', 'зуд', 'отек', 'рвота', 'диарея'
        ]
        
        if any(effect in event for effect in known_effects):
            return "известный"
        return "неизвестный"
    
    def _check_drug_mention(self, text):
        """Проверяет упоминание препарата"""
        drug_patterns = [
            r'препарат', r'лекарств', r'таблет', r'капсул', r'инъекц'
        ]
        
        if any(pattern in text for pattern in drug_patterns):
            return "есть"
        return "нет"
    
    def _apply_who_algorithm(self, facts):
        """Применяет алгоритм оценки по шкале ВОЗ"""
        
        # Определенная
        if (facts['time_relationship'] == "есть" and
            facts['rechallenge'] == "есть" and
            facts['dechallenge'] == "положительная" and
            facts['alternative_causes'] == "нет данных"):
            return "Определенная"
        
        # Вероятная
        elif (facts['time_relationship'] == "есть" and
              facts['dechallenge'] == "положительная" and
              facts['alternative_causes'] == "нет данных"):
            return "Вероятная"
        
        # Возможная
        elif (facts['time_relationship'] == "есть" and
              facts['alternative_causes'] == "нет данных"):
            return "Возможная"
        
        # Сомнительная
        elif (facts['time_relationship'] == "нет данных" or
              facts['alternative_causes'] == "есть"):
            return "Сомнительная"
        
        # Условная
        elif facts['drug_mentioned'] == "нет":
            return "Условная"
        
        else:
            return "Неклассифицируемая"
    
    def _generate_reasoning(self, level, facts):
        """Генерирует обоснование оценки"""
        reasoning_templates = {
            "Определенная": "Четкая временная связь, положительная десенсибилизация и положительная реакция на повторное назначение. Альтернативные причины исключены.",
            "Вероятная": "Временная связь присутствует, положительная десенсибилизация. Альтернативные причины маловероятны.",
            "Возможная": "Временная связь имеется, но данных о десенсибилизации недостаточно.",
            "Сомнительная": "Отсутствует четкая временная связь или имеются альтернативные причины.",
            "Условная": "Недостаточно данных для оценки причинно-следственной связи.",
            "Неклассифицируемая": "Информация противоречива или недостаточна для классификации."
        }
        
        return reasoning_templates.get(level, "Не удалось оценить связь.")

# Тестирование модуля
if __name__ == "__main__":
    checker = CausalityChecker()
    
    print("🧪 Тестирование модуля причинности:")
    print("=" * 50)
    
    test_cases = [
        "Пациент через 2 часа после приема препарата отметил появление сыпи. Препарат отменен, сыпь исчезла через сутки.",
        "На фоне лечения развилась тошнота. Одновременно пациент принимал другие препараты.",
        "Пациент скончался. Причина смерти не установлена."
    ]
    
    for i, case in enumerate(test_cases, 1):
        result = checker.analyze_causality(case, "сыпь")
        print(f"\nТест {i}: {result['level']}")
        print(f"Текст: {case}")
        print(f"Обоснование: {result['reasoning']}")
