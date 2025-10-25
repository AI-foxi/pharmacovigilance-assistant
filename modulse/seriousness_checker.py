# modules/seriousness_checker.py
import re

class SeriousnessChecker:
    def check_seriousness(self, text):
        seriousness_words = {
            'death': ['смерть', 'летальный', 'погиб', 'умер'],
            'life_threatening': ['угроза жизни', 'реанимация', 'орит'],
            'hospitalization': ['госпитализ', 'стационар', 'поступил в больницу'],
            'disability': ['инвалид', 'нетрудоспособность'],
            'congenital': ['врожденн', 'аномалия']
        }
        
        found_flags = []
        for category, words in seriousness_words.items():
            for word in words:
                if word in text.lower():
                    found_flags.append(category)
                    break
        
        return {'is_serious': len(found_flags) > 0, 'flags': found_flags}