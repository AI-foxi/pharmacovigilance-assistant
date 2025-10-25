
# modules/seriousness_checker.py
class SeriousnessChecker:
    def check_seriousness(self, text):
        """
        Проверяет, является ли случай серьезным
        Возвращает: {'is_serious': True/False, 'flags': ['причина1', 'причина2']}
        """
        
        # Приводим текст к нижнему регистру для поиска
        text_lower = text.lower()
        
        # Словарь серьезных критериев
        seriousness_words = {
            'death': ['смерть', 'летальный', 'погиб', 'умер', 'скончался'],
            'life_threatening': ['угроза жизни', 'реанимация', 'орит', 'интенсивная терапия'],
            'hospitalization': ['госпитализ', 'стационар', 'поступил в больницу', 'госпитализирован'],
            'disability': ['инвалид', 'нетрудоспособность', 'инвалидность'],
            'congenital': ['врожденн', 'аномалия', 'порок развития'],
            'overdose': ['передозировка', 'отравление', 'интоксикация']
        }
        
        found_flags = []
        
        # Ищем каждую категорию в тексте
        for category, words in seriousness_words.items():
            for word in words:
                if word in text_lower:
                    found_flags.append(category)
                    break  # нашли одно слово - достаточно
        
        return {
            'is_serious': len(found_flags) > 0,
            'flags': found_flags
        }

# Простой тест
if __name__ == "__main__":
    checker = SeriousnessChecker()
    test_text = "Пациент госпитализирован с анафилактическим шоком"
    result = checker.check_seriousness(test_text)
    print(f"Тест: {test_text}")
    print(f"Результат: {result}")
