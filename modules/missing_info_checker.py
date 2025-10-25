# modules/missing_info_checker.py
import re
from datetime import datetime

class MissingInfoChecker:
    def check_missing_information(self, text, adverse_event):
        """
        Проверяет, какая информация отсутствует в кейсе
        Возвращает: {'missing_info': ['пункт1', 'пункт2'], 'questions': ['вопрос1', 'вопрос2']}
        """
        text_lower = text.lower()
        
        # Проверяем наличие ключевой информации
        checks = {
            'patient_age': self._check_patient_age(text_lower),
            'patient_gender': self._check_patient_gender(text_lower),
            'drug_name': self._check_drug_name(text_lower),
            'drug_dose': self._check_drug_dose(text_lower),
            'event_start_date': self._check_event_start_date(text_lower),
            'event_end_date': self._check_event_end_date(text_lower),
            'time_to_onset': self._check_time_to_onset(text_lower),
            'outcome': self._check_outcome(text_lower, adverse_event),
            'dechallenge_result': self._check_dechallenge_result(text_lower),
            'rechallenge_info': self._check_rechallenge_info(text_lower),
            'lab_data': self._check_lab_data(text_lower),
            'concomitant_drugs': self._check_concomitant_drugs(text_lower),
            'medical_history': self._check_medical_history(text_lower),
            'event_severity': self._check_event_severity(text_lower)
        }
        
        missing_info = []
        questions = []
        
        for info_type, is_present in checks.items():
            if not is_present['present']:
                missing_info.append(info_type)
                questions.append(is_present['question'])
        
        return {
            'missing_info': missing_info,
            'questions': questions,
            'completeness_score': self._calculate_completeness_score(checks),
            'critical_missing': self._identify_critical_missing(missing_info)
        }
    
    def _check_patient_age(self, text):
        """Проверяет наличие возраста пациента"""
        age_patterns = [
            r'(\d+)\s*лет',
            r'(\d+)\s*года',
            r'возраст\s*(\d+)',
            r'пациент\w*\s*(\d+)'
        ]
        
        for pattern in age_patterns:
            if re.search(pattern, text):
                return {'present': True, 'question': ''}
        
        return {
            'present': False, 
            'question': 'Какой возраст пациента?'
        }
    
    def _check_patient_gender(self, text):
        """Проверяет наличие пола пациента"""
        gender_indicators = ['пациентка', 'женщина', 'девушка', 'девочка', 'мужчина', 'муж', 'юноша']
        
        if any(indicator in text for indicator in gender_indicators):
            return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Какой пол пациента?'
        }
    
    def _check_drug_name(self, text):
        """Проверяет наличие названия препарата"""
        drug_indicators = ['препарат', 'лекарств', 'таблет', 'капсул', 'инъекц', 'введение']
        
        if any(indicator in text for indicator in drug_indicators):
            return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Какой препарат принимал пациент?'
        }
    
    def _check_drug_dose(self, text):
        """Проверяет наличие дозировки препарата"""
        dose_patterns = [
            r'(\d+)\s*мг',
            r'(\d+)\s*мкг',
            r'(\d+)\s*г',
            r'(\d+)\s*таблет',
            r'(\d+)\s*капсул',
            r'доз[ау]и'
        ]
        
        for pattern in dose_patterns:
            if re.search(pattern, text):
                return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Какая дозировка препарата?'
        }
    
    def _check_event_start_date(self, text):
        """Проверяет наличие даты начала события"""
        date_patterns = [
            r'\d{1,2}\.\d{1,2}\.\d{4}',
            r'\d{1,2}\.\d{1,2}',
            r'\d{1,2}\s*[а-я]+\s*\d{4}',
            r'начал[оа]\s*\d'
        ]
        
        start_indicators = ['начал', 'появ', 'возник', 'развит']
        
        has_date = any(re.search(pattern, text) for pattern in date_patterns)
        has_start_indicator = any(indicator in text for indicator in start_indicators)
        
        if has_date and has_start_indicator:
            return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Когда началось нежелательное явление?'
        }
    
    def _check_event_end_date(self, text):
        """Проверяет наличие даты окончания события"""
        end_indicators = ['закончил', 'прекратил', 'исчез', 'прошл', 'купирова', 'нормализова']
        
        if any(indicator in text for indicator in end_indicators):
            return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Когда закончилось нежелательное явление?'
        }
    
    def _check_time_to_onset(self, text):
        """Проверяет наличие времени до начала события"""
        time_patterns = [
            r'через\s*(\d+)\s*(час|день|недел|месяц)',
            r'спустя\s*(\d+)\s*(час|день)',
            r'через\s*(\d+)\s*суток'
        ]
        
        for pattern in time_patterns:
            if re.search(pattern, text):
                return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Через сколько времени после приема препарата началось явление?'
        }
    
    def _check_outcome(self, text, adverse_event):
        """Проверяет наличие исхода события"""
        outcome_indicators = [
            'выздоровел', 'улучшил', 'нормализовал', 'исчезл', 'прошл',
            'ухудшил', 'осложнил', 'госпитализирован', 'умер', 'скончал'
        ]
        
        # Если есть серьезное событие, но нет исхода - это критично
        serious_events = ['смерть', 'летальн', 'погиб', 'умер', 'скончал']
        is_serious = any(event in adverse_event for event in serious_events)
        
        has_outcome = any(indicator in text for indicator in outcome_indicators)
        
        if has_outcome:
            return {'present': True, 'question': ''}
        
        if is_serious:
            return {
                'present': False,
                'question': 'Каков был исход серьезного нежелательного явления?'
            }
        else:
            return {
                'present': False,
                'question': 'Каков был исход нежелательного явления?'
            }
    
    def _check_dechallenge_result(self, text):
        """Проверяет наличие информации об отмене препарата"""
        dechallenge_indicators = ['отмен', 'прекратил', 'перестал', 'отменил']
        outcome_indicators = ['улучшил', 'исчезл', 'прошл', 'сохранил', 'ухудшил']
        
        has_dechallenge = any(indicator in text for indicator in dechallenge_indicators)
        has_outcome = any(indicator in text for indicator in outcome_indicators)
        
        if has_dechallenge and has_outcome:
            return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Что произошло после отмены препарата?'
        }
    
    def _check_rechallenge_info(self, text):
        """Проверяет наличие информации о повторном назначении"""
        rechallenge_indicators = ['повторно', 'снова', 'рецидив', 'возобновил', 'вновь']
        
        if any(indicator in text for indicator in rechallenge_indicators):
            return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Было ли повторное назначение препарата?'
        }
    
    def _check_lab_data(self, text):
        """Проверяет наличие лабораторных данных"""
        lab_indicators = [
            'анализ', 'лабораторн', 'кровь', 'моч', 'биохими', 'гемоглобин',
            'лейкоцит', 'тромбоцит', 'алт', 'аст', 'креатинин'
        ]
        
        if any(indicator in text for indicator in lab_indicators):
            return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Есть ли данные лабораторных исследований?'
        }
    
    def _check_concomitant_drugs(self, text):
        """Проверяет наличие информации о сопутствующих препаратах"""
        concomitant_indicators = [
            'одновременно', 'сопутствующ', 'также принимал', 'другие препарат',
            'комбинац', 'сочетан'
        ]
        
        if any(indicator in text for indicator in concomitant_indicators):
            return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Принимал ли пациент другие препараты одновременно?'
        }
    
    def _check_medical_history(self, text):
        """Проверяет наличие информации о сопутствующих заболеваниях"""
        history_indicators = [
            'анамнез', 'сопутствующ', 'хроническ', 'страдает', 'болеет',
            'в анамнезе', 'история болезн'
        ]
        
        if any(indicator in text for indicator in history_indicators):
            return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Есть ли у пациента сопутствующие заболевания?'
        }
    
    def _check_event_severity(self, text):
        """Проверяет наличие информации о тяжести события"""
        severity_indicators = [
            'легк', 'средн', 'тяжел', 'крайне тяжел', 'умерен',
            'интенсивн', 'выражен'
        ]
        
        if any(indicator in text for indicator in severity_indicators):
            return {'present': True, 'question': ''}
        
        return {
            'present': False,
            'question': 'Какова тяжесть нежелательного явления?'
        }
    
    def _calculate_completeness_score(self, checks):
        """Рассчитывает оценку полноты информации"""
        total_checks = len(checks)
        present_checks = sum(1 for check in checks.values() if check['present'])
        
        return round((present_checks / total_checks) * 100, 1)
    
    def _identify_critical_missing(self, missing_info):
        """Определяет критически важную отсутствующую информацию"""
        critical_info = [
            'drug_name', 'outcome', 'event_start_date', 'dechallenge_result'
        ]
        
        return [info for info in missing_info if info in critical_info]

# Тестирование модуля
if __name__ == "__main__":
    checker = MissingInfoChecker()
    
    print("🧪 Тестирование модуля проверки недостающей информации:")
    print("=" * 60)
    
    test_cases = [
        {
            "text": "Пациент 45 лет отметил сыпь после приема препарата",
            "event": "сыпь"
        },
        {
            "text": "Развилась тошнота",
            "event": "тошнота"
        },
        {
            "text": "Пациентка 30 лет через 2 часа после приема Препарата А 500 мг отметила появление крапивницы. Препарат отменен, симптомы исчезли через 6 часов.",
            "event": "крапивница"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        result = checker.check_missing_information(test_case["text"], test_case["event"])
        
        print(f"\nТест {i}:")
        print(f"Текст: {test_case['text']}")
        print(f"Полнота информации: {result['completeness_score']}%")
        
        if result['missing_info']:
            print("❌ Отсутствует информация:")
            for question in result['questions']:
                print(f"   - {question}")
            
            if result['critical_missing']:
                print("🚨 Критически важная отсутствующая информация!")
        else:
            print("✅ Вся необходимая информация присутствует")
