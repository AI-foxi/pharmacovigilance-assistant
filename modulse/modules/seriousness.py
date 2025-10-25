
class SeriousnessChecker:
    def check(self, text):
        serious = any(word in text.lower() for word in 
                     ['госпитализ', 'смерть', 'реанимация'])
        return serious
