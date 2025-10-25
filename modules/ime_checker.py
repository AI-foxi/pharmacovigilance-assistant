# modules/ime_checker.py
import json
import os

class IMEChecker:
    def __init__(self):
        self.ime_terms = self._load_ime_terms()
        self.russian_mappings = self._create_russian_mappings()
    
    def _load_ime_terms(self):
        """Загружает IME термины из JSON файла"""
        try:
            with open('knowledge/ime_list.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('important_medical_events', [])
        except FileNotFoundError:
            print("⚠️ Файл IME списка не найден! Используем базовый список.")
            return [
                "Anaphylactic shock", "Stevens-Johnson syndrome", 
                "Acute hepatic failure", "Cardiac arrest"
            ]
    
    def _create_russian_mappings(self):
        """Создает словарь для перевода русских терминов в английские"""
        mappings = {
            'анафилактический шок': 'Anaphylactic shock',
            'анафилактическая реакция': 'Anaphylactic reaction', 
            'анафилаксия': 'Anaphylactic shock',
            'остановка сердца': 'Cardiac arrest',
            'инфаркт миокарда': 'Myocardial infarction',
            'инфаркт': 'Myocardial infarction',
            'синдром стивенса-джонсона': 'Stevens-Johnson syndrome',
            'токсический эпидермальный некролиз': 'Toxic epidermal necrolysis',
            'острая печеночная недостаточность': 'Acute hepatic failure',
            'острая почечная недостаточность': 'Acute kidney injury',
            'инсульт': 'Cerebrovascular accident',
            'сепсис': 'Sepsis',
            'панкреатит': 'Pancreatitis acute',
            'суицидальные мысли': 'Suicidal ideation'
        }
        return mappings
    
    def check_ime_significance(self, text):
        """
        Проверяет, содержит ли текст клинически значимые события (IME)
        Возвращает: {'is_significant': True/False, 'found_terms': ['термин1', 'термин2']}
        """
        text_lower = text.lower()
        found_terms = []
        
        for russian_term, english_term in self.russian_mappings.items():
            if russian_term in text_lower:
                if english_term in self.ime_terms:
                    found_terms.append({
                        'russian': russian_term,
                        'english': english_term
                    })
        
        return {
            'is_significant': len(found_terms) > 0,
            'found_terms': found_terms
        }
