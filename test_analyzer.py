"""
Модульні тести для системи аналізу настроїв
Unit tests for Ukrainian Sentiment Analyzer
"""

import unittest
from sentiment_analyzer import UkrainianSentimentAnalyzer


class TestUkrainianSentimentAnalyzer(unittest.TestCase):
    """Тести для UkrainianSentimentAnalyzer"""
    
    def setUp(self):
        """Налаштування перед кожним тестом"""
        self.analyzer = UkrainianSentimentAnalyzer()
    
    def test_positive_sentiment(self):
        """Тест позитивного настрою"""
        text = "Цей продукт чудовий! Я дуже задоволений."
        result = self.analyzer.analyze(text)
        
        self.assertEqual(result['sentiment'], 'positive')
        self.assertGreater(result['score'], 0)
        self.assertGreater(len(result['found_positive']), 0)
    
    def test_negative_sentiment(self):
        """Тест негативного настрою"""
        text = "Жахливий сервіс, ненавиджу це місце!"
        result = self.analyzer.analyze(text)
        
        self.assertEqual(result['sentiment'], 'negative')
        self.assertLess(result['score'], 0)
        self.assertGreater(len(result['found_negative']), 0)
    
    def test_neutral_sentiment(self):
        """Тест нейтрального настрою"""
        text = "Сьогодні вівторок. На вулиці сухо."
        result = self.analyzer.analyze(text)
        
        self.assertEqual(result['sentiment'], 'neutral')
        self.assertEqual(result['score'], 0.0)
    
    def test_negation_handling(self):
        """Тест обробки заперечень"""
        text = "Це не поганий продукт"
        result = self.analyzer.analyze(text)
        
        # "не поганий" має бути позитивним або нейтральним
        self.assertNotEqual(result['sentiment'], 'negative')
    
    def test_intensifiers(self):
        """Тест посилювачів"""
        text1 = "Це добрий продукт"
        text2 = "Це дуже добрий продукт"
        
        result1 = self.analyzer.analyze(text1)
        result2 = self.analyzer.analyze(text2)
        
        # Посилювач "дуже" має збільшити вплив
        self.assertGreaterEqual(
            result2['positive_count'], 
            result1['positive_count']
        )
    
    def test_empty_text(self):
        """Тест порожнього тексту"""
        result = self.analyzer.analyze("")
        
        self.assertEqual(result['sentiment'], 'neutral')
        self.assertEqual(result['score'], 0.0)
        self.assertEqual(result['word_count'], 0)
    
    def test_batch_analysis(self):
        """Тест пакетного аналізу"""
        texts = [
            "Чудово!",
            "Жахливо!",
            "Нормально."
        ]
        results = self.analyzer.analyze_batch(texts)
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['sentiment'], 'positive')
        self.assertEqual(results[1]['sentiment'], 'negative')
    
    def test_case_insensitivity(self):
        """Тест нечутливості до регістру"""
        text1 = "Чудовий продукт"
        text2 = "чудовий продукт"
        text3 = "ЧУДОВИЙ продукт"
        
        result1 = self.analyzer.analyze(text1)
        result2 = self.analyzer.analyze(text2)
        result3 = self.analyzer.analyze(text3)
        
        self.assertEqual(result1['sentiment'], result2['sentiment'])
        self.assertEqual(result2['sentiment'], result3['sentiment'])
    
    def test_confidence_calculation(self):
        """Тест розрахунку впевненості"""
        text = "чудовий чудовий чудовий чудовий чудовий"
        result = self.analyzer.analyze(text)
        
        # Багато емоційних слів → висока впевненість
        self.assertGreater(result['confidence'], 0.5)


class TestPreprocessor(unittest.TestCase):
    """Тести для препроцесора тексту"""
    
    def setUp(self):
        self.analyzer = UkrainianSentimentAnalyzer()
    
    def test_text_cleaning(self):
        """Тест очищення тексту"""
        text = "Чудовий!!! Продукт... (тест)"
        words = self.analyzer.preprocess_text(text)
        
        # Перевіряємо, що є слова
        self.assertGreater(len(words), 0)
        
        # Перевіряємо, що видалено розділові знаки
        for word in words:
            self.assertNotIn('!', word)
            self.assertNotIn('.', word)
            self.assertNotIn('(', word)
    
    def test_lowercase_conversion(self):
        """Тест приведення до нижнього регістру"""
        text = "ЧУДОВИЙ ПрОдУкТ"
        words = self.analyzer.preprocess_text(text)
        
        self.assertEqual(words[0], "чудовий")
        self.assertEqual(words[1], "продукт")


class TestEdgeCases(unittest.TestCase):
    """Тести для граничних випадків"""
    
    def setUp(self):
        self.analyzer = UkrainianSentimentAnalyzer()
    
    def test_very_long_text(self):
        """Тест довгого тексту"""
        text = "чудовий " * 1000
        result = self.analyzer.analyze(text)
        
        self.assertEqual(result['sentiment'], 'positive')
        self.assertEqual(result['word_count'], 1000)
    
    def test_mixed_sentiment(self):
        """Тест змішаного настрою"""
        text = "Продукт чудовий, але ціна жахлива"
        result = self.analyzer.analyze(text)
        
        # Має бути змішаний результат
        self.assertGreater(len(result['found_positive']), 0)
        self.assertGreater(len(result['found_negative']), 0)


def run_tests():
    """Запуск всіх тестів"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Додаємо всі тести
    suite.addTests(loader.loadTestsFromTestCase(TestUkrainianSentimentAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestPreprocessor))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Запускаємо
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 60)
    print("ЗАПУСК МОДУЛЬНИХ ТЕСТІВ")
    print("=" * 60)
    success = run_tests()
    print("=" * 60)
    print(f"РЕЗУЛЬТАТ: {'✅ УСПІШНО' if success else '❌ ПОМИЛКА'}")
    print("=" * 60)
