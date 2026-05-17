#!/usr/bin/env python3
"""
Демонстраційний скрипт для системи аналізу настроїв
Interactive Demo for Ukrainian Sentiment Analyzer
"""

from sentiment_analyzer import UkrainianSentimentAnalyzer


def print_header():
    """Виведення заголовка"""
    print("=" * 70)
    print("     СИСТЕМА АНАЛІЗУ НАСТРОЇВ ТЕКСТІВ УКРАЇНСЬКОЮ МОВОЮ")
    print("          Ukrainian Text Sentiment Analysis System")
    print("=" * 70)


def print_separator():
    """Виведення розділювача"""
    print("-" * 70)


def demo_predefined_texts():
    """Демонстрація на готових прикладах"""
    analyzer = UkrainianSentimentAnalyzer()
    
    print("\n[+] ДЕМОНСТРАЦІЯ НА ГОТОВИХ ТЕКСТАХ")
    print_separator()
    
    test_cases = [
        {
            "text": "Цей продукт просто чудовий! Я дуже задоволений покупкою.",
            "category": "[OK] Позитивний відгук"
        },
        {
            "text": "Жахливий сервіс, жодного разу більше не звернуся до них.",
            "category": "[XX] Негативний відгук"
        },
        {
            "text": "Середній товар за середню ціну, нічого особливого.",
            "category": "[--] Нейтральний відгук"
        },
        {
            "text": "Не поганий результат, але є над чим працювати.",
            "category": "[<>] Заперечення (не + негатив)"
        },
        {
            "text": "Дуже красивий і зручний інтерфейс, рекомендую всім!",
            "category": "[^] Посилювач (дуже + позитив)"
        },
        {
            "text": "Ненадійна компанія, обманули з доставкою.",
            "category": "[!] Скарга на сервіс"
        },
        {
            "text": "Погода сьогодні нормальна, нічого особливого.",
            "category": "[i] Нейтральний опис"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        result = analyzer.analyze(case["text"])
        label = analyzer.get_sentiment_label(result['sentiment'])
        
        print(f"\n[{i}] {case['category']}")
        print(f"    Текст: \"{case['text']}\"")
        print(f"    Результат: {label}")
        print(f"    ├─ Бали настрою: {result['score']}")
        print(f"    ├─ Впевненість: {result['confidence']*100:.1f}%")
        print(f"    ├─ Позитивних слів: {result['found_positive']}")
        print(f"    └─ Негативних слів: {result['found_negative']}")
    
    print_separator()


def interactive_mode():
    """Інтерактивний режим"""
    analyzer = UkrainianSentimentAnalyzer()
    
    print("\n[>] ІНТЕРАКТИВНИЙ РЕЖИМ")
    print("Введіть текст для аналізу (або 'quit' для виходу):")
    print_separator()
    
    while True:
        try:
            user_input = input("\n[>] Ваш текст: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'вихід', 'q']:
                print("\n[^] Дякую за використання! До побачення!")
                break
            
            if not user_input:
                print("[!] Будь ласка, введіть текст.")
                continue
            
            result = analyzer.analyze(user_input)
            label = analyzer.get_sentiment_label(result['sentiment'])
            
            print(f"\n[*] РЕЗУЛЬТАТ АНАЛІЗУ:")
            print(f"   Настрій: {label}")
            print(f"   ├─ Бали: {result['score']}")
            print(f"   ├─ Впевненість: {result['confidence']*100:.1f}%")
            print(f"   ├─ Всього слів: {result['word_count']}")
            
            if result['found_positive']:
                print(f"   ├─ Позитивні: {', '.join(result['found_positive'])}")
            if result['found_negative']:
                print(f"   └─ Негативні: {', '.join(result['found_negative'])}")
            
            # Emoji-візуалізація
            bar_length = 20
            score_normalized = (result['score'] + 1) / 2  # від -1..1 до 0..1
            filled = int(bar_length * score_normalized)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"\n   [{bar}] {result['score']:+.2f}")
            
        except KeyboardInterrupt:
            print("\n\n[^] До побачення!")
            break
        except Exception as e:
            print(f"[X] Помилка: {e}")


def batch_analysis_demo():
    """Демонстрація пакетного аналізу"""
    analyzer = UkrainianSentimentAnalyzer()
    
    print("\n[=] ПАКЕТНИЙ АНАЛІЗ")
    print_separator()
    
    texts = [
        "Супер якість!",
        "Жах і тільки...",
        "Нормально.",
        "Добрий день, як справи?",
        "Ненавиджу цей сервіс!"
    ]
    
    print(f"Аналізуємо {len(texts)} текстів одночасно...\n")
    
    results = analyzer.analyze_batch(texts)
    
    # Статистика
    stats = {'positive': 0, 'negative': 0, 'neutral': 0}
    
    for i, (text, result) in enumerate(zip(texts, results), 1):
        label = result['sentiment']
        stats[label] = stats.get(label, 0) + 1
        emoji = {'positive': '[+]', 'negative': '[-]', 'neutral': '[~]'}.get(label, '[?]')
        
        print(f"{i}. {emoji} [{label:10}] \"{text[:40]}{'...' if len(text) > 40 else ''}\"")
    
    print_separator()
    print("[#] СТАТИСТИКА:")
    print(f"   Позитивних: {stats['positive']} | Негативних: {stats['negative']} | Нейтральних: {stats['neutral']}")
    print_separator()


def show_system_info():
    """Виведення інформації про систему"""
    analyzer = UkrainianSentimentAnalyzer()
    
    print("\n[i] ІНФОРМАЦІЯ ПРО СИСТЕМУ")
    print_separator()
    print(f"Версія: MVP 1.0")
    print(f"Позитивних слів у словнику: {len(analyzer.positive_words)}")
    print(f"Негативних слів у словнику: {len(analyzer.negative_words)}")
    print(f"Посилювачів: {len(analyzer.intensifiers)}")
    print(f"Заперечень: {len(analyzer.negations)}")
    print(f"Алгоритм: Лексичний (словниковий) метод")
    print(f"Мова: Python 3.8+")
    print(f"Залежності: тільки стандартна бібліотека")
    print_separator()


def main():
    """Головна функція"""
    print_header()
    show_system_info()
    
    # Спочатку демонстрація
    demo_predefined_texts()
    
    # Пакетний аналіз
    batch_analysis_demo()
    
    # Інтерактивний режим
    print("\n[>>] Готовий до інтерактивного режиму!")
    interactive_mode()


if __name__ == "__main__":
    main()
