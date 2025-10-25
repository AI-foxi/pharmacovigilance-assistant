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
    
    def _create_russian_mappings(self):  # ← ЭТА СТРОКА ДОЛЖНА БЫТЬ ВЫРОВНЕНА С ДРУГИМИ МЕТОДАМИ
        """Создает словарь для перевода русских терминов в английские"""
        mappings = {
            # Кардиологические
            'инфаркт миокарда': 'Myocardial infarction',
            'ишемия миокарда': 'Myocardial ischemia',
            'перикардиальный выпот': 'Pericardial effusion',
            'тромбоз коронарных артерий': 'Coronary artery thrombosis',
            'окклюзия коронарных артерий': 'Coronary artery occlusion',
            'артериальный тромбоз': 'Arterial thrombosis',
            'атриовентрикулярная блокада': 'Atrioventricular block first degree',
            'желудочковые экстрасистолы': 'Ventricular extrasystoles',
            'сердцебиение': 'Palpitations',
            'удлинение интервала qt': 'Prolonged electrocardiogram QT',
            'артериальная гипертензия': 'Hypertension',
            'хсн': 'Congestive cardiomyopathy',
            'суправентрикулярная тахикардия': 'Supraventricular tachycardia',
            'венозная тромбоэмболия': 'Venous thromboembolism',
            'артериальная тромбоэмболия': 'Arterial thromboembolism',
            'тромбоз глубоких вен': 'Deep vein thrombosis',
            'тэла': 'Pulmonary embolism',
            
            # Неврологические и психиатрические
            'психотическое расстройство': 'Psychotic disorder',
            'галлюцинации': 'Hallucinations',
            'гипестезия': 'Hypoaesthesia',
            'тремор': 'Tremor',
            'летаргия': 'Lethargy',
            'периферическая нейропатия': 'Peripheral sensory neuropathy',
            'головокружение': 'Dizziness',
            'головная боль': 'Headache',
            'сонливость': 'Somnolence',
            'заторможенность': 'Lethargy',
            'инсульт': 'Cerebrovascular accident',
            'синкопе': 'Syncope',
            'гипертензивная энцефалопатия': 'Hypertensive encephalopathy',
            
            # Дерматологические
            'сыпь': 'Rash',
            'дерматит': 'Dermatitis',
            'крапивница': 'Urticaria',
            'зуд': 'Pruritus',
            'эксфолиативный дерматит': 'Exfoliative dermatitis',
            'синдром стивенса-джонсона': 'Stevens-Johnson syndrome',
            'токсический эпидермальный некролиз': 'Toxic epidermal necrolysis',
            'тяжелые кожные реакции': 'Severe cutaneous adverse reactions',
            'ладонно-подошвенный синдром': 'Palmar-plantar erythrodysaesthesia syndrome',
            
            # Желудочно-кишечные
            'тошнота': 'Nausea',
            'рвота': 'Vomiting',
            'диарея': 'Diarrhoea',
            'запор': 'Constipation',
            'боль в животе': 'Abdominal pain',
            'диспепсия': 'Dyspepsia',
            'панкреатит': 'Pancreatitis acute',
            'колит': 'Colitis',
            'перфорация жкт': 'Gastrointestinal perforation',
            'непроходимость кишечника': 'Gastrointestinal obstruction',
            'желудочно-кишечное кровотечение': 'Gastrointestinal haemorrhage',
            'ректальное кровотечение': 'Rectal haemorrhage',
            
            # Печеночные
            'повышение алт': 'Alanine aminotransferase increased',
            'повышение аст': 'Aspartate aminotransferase increased',
            'повышение печеночных ферментов': 'Hepatic enzyme increased',
            'повышение трансаминаз': 'Transaminases increased',
            'повышение ггт': 'Gamma-glutamyltransferase increased',
            'гепатит': 'Hepatitis',
            'печеночная недостаточность': 'Acute hepatic failure',
            
            # Почечные
            'нарушение функции почек': 'Renal impairment',
            'почечная недостаточность': 'Renal failure',
            'острая почечная недостаточность': 'Renal failure acute',
            'нефрит': 'Nephritis',
            'протеинурия': 'Proteinuria',
            'нефротический синдром': 'Nephrotic syndrome',
            
            # Гематологические
            'лейкопения': 'Leukopenia',
            'нейтропения': 'Neutropenia',
            'тромбоцитопения': 'Thrombocytopenia',
            'лимфопения': 'Lymphopenia',
            'анемия': 'Anaemia',
            'фебрильная нейтропения': 'Febrile neutropenia',
            'коагулопатии': 'Coagulopathy',
            'синдром диссеминированного свертывания': 'Disseminated intravascular coagulation',
            
            # Инфекционные
            'сепсис': 'Sepsis',
            'пневмония': 'Pneumonia',
            'инфекции': 'Infection',
            'некротизирующий фасциит': 'Necrotising fasciitis',
            
            # Аллергические и иммунные
            'анафилактический шок': 'Anaphylactic shock',
            'анафилактические реакции': 'Anaphylactic reaction',
            'аллергические реакции': 'Anaphylactic reaction',
            'реакции гиперчувствительности': 'Hypersensitivity',
            'инфузионные реакции': 'Infusion related reaction',
            
            # Другие серьезные
            'смерть': 'Death',
            'летальный': 'Death',
            'погиб': 'Death',
            'умер': 'Death',
            'госпитализирован': 'Hospitalisation',
            'реанимация': 'Life threatening',
            'угроза жизни': 'Life threatening'
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
