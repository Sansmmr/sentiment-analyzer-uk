"""
Графічний інтерфейс для системи аналізу настроїв
GUI for Ukrainian Sentiment Analyzer
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from sentiment_analyzer import UkrainianSentimentAnalyzer


class SentimentAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Аналіз настроїв текстів українською")
        self.root.geometry("700x600")
        self.root.configure(bg='#f0f0f0')
        
        # Ініціалізація аналізатора
        self.analyzer = UkrainianSentimentAnalyzer()
        
        # Стилі
        self.style = ttk.Style()
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), background='#f0f0f0')
        self.style.configure('Result.TLabel', font=('Arial', 12), background='#f0f0f0')
        self.style.configure('Positive.TLabel', font=('Arial', 12, 'bold'), foreground='green', background='#f0f0f0')
        self.style.configure('Negative.TLabel', font=('Arial', 12, 'bold'), foreground='red', background='#f0f0f0')
        self.style.configure('Neutral.TLabel', font=('Arial', 12, 'bold'), foreground='blue', background='#f0f0f0')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Заголовок
        header = ttk.Label(self.root, text="СИСТЕМА АНАЛІЗУ НАСТРОЇВ", style='Header.TLabel')
        header.pack(pady=10)
        
        subheader = ttk.Label(self.root, text="Український текст → Оцінка настрою", style='Result.TLabel')
        subheader.pack(pady=5)
        
        # Рамка для вводу
        input_frame = ttk.LabelFrame(self.root, text="Введіть текст для аналізу", padding=10)
        input_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Поле для вводу тексту
        self.text_input = scrolledtext.ScrolledText(input_frame, height=8, wrap=tk.WORD, font=('Consolas', 11))
        self.text_input.pack(fill='both', expand=True)
        
        # Кнопки
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.analyze_btn = ttk.Button(button_frame, text="АНАЛІЗУВАТИ", command=self.analyze_text, width=20)
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="ОЧИСТИТИ", command=self.clear_all, width=15)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Рамка для результатів
        result_frame = ttk.LabelFrame(self.root, text="Результат аналізу", padding=10)
        result_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Результат настрою (великим шрифтом)
        self.sentiment_label = ttk.Label(result_frame, text="Настрій: ---", style='Result.TLabel')
        self.sentiment_label.pack(pady=5)
        
        # Деталі
        details_frame = ttk.Frame(result_frame)
        details_frame.pack(fill='x', pady=5)
        
        self.score_label = ttk.Label(details_frame, text="Бали: ---", style='Result.TLabel')
        self.score_label.pack(anchor='w')
        
        self.confidence_label = ttk.Label(details_frame, text="Впевненість: ---", style='Result.TLabel')
        self.confidence_label.pack(anchor='w')
        
        self.words_label = ttk.Label(details_frame, text="Знайдені слова: ---", style='Result.TLabel')
        self.words_label.pack(anchor='w')
        
        # Статус бар
        self.status_bar = ttk.Label(self.root, text="Готово до роботи", relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill='x')
        
        # Приклади текстів (кнопки швидкого вводу)
        examples_frame = ttk.LabelFrame(self.root, text="Швидкі приклади (клікніть для вставки)", padding=5)
        examples_frame.pack(padx=20, pady=5, fill='x')
        
        examples = [
            ("Позитивний", "Цей продукт чудовий! Я дуже задоволений."),
            ("Негативний", "Жахливий сервіс, нікому не рекомендую."),
            ("Нейтральний", "Сьогодні вівторок, погода нормальна."),
            ("Заперечення", "Це не поганий результат для початку.")
        ]
        
        for label, text in examples:
            btn = ttk.Button(examples_frame, text=label, 
                           command=lambda t=text: self.insert_example(t),
                           width=12)
            btn.pack(side=tk.LEFT, padx=5, pady=2)
    
    def insert_example(self, text):
        """Вставка прикладу тексту"""
        self.text_input.delete('1.0', tk.END)
        self.text_input.insert('1.0', text)
        self.status_bar.config(text=f"Вставлено приклад: {text[:30]}...")
    
    def analyze_text(self):
        """Аналіз тексту"""
        text = self.text_input.get('1.0', tk.END).strip()
        
        if not text:
            messagebox.showwarning("Увага", "Будь ласка, введіть текст для аналізу!")
            return
        
        try:
            result = self.analyzer.analyze(text)
            self.display_result(result)
            self.status_bar.config(text=f"Аналіз завершено. Знайдено {len(result['found_positive'])} позитивних, {len(result['found_negative'])} негативних слів.")
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка аналізу: {str(e)}")
    
    def display_result(self, result):
        """Відображення результату"""
        sentiment = result['sentiment']
        score = result['score']
        confidence = result['confidence'] * 100
        
        # Визначення стилю та кольору
        if sentiment == 'positive':
            style = 'Positive.TLabel'
            emoji = "[+]"
            color = 'green'
        elif sentiment == 'negative':
            style = 'Negative.TLabel'
            emoji = "[-]"
            color = 'red'
        else:
            style = 'Neutral.TLabel'
            emoji = "[~]"
            color = 'blue'
        
        # Оновлення міток
        self.sentiment_label.config(text=f"Настрій: {emoji} {sentiment.upper()}", style=style)
        self.score_label.config(text=f"Бали настрою: {score:+.2f} (від -1.0 до +1.0)")
        self.confidence_label.config(text=f"Впевненість: {confidence:.1f}%")
        
        # Слова
        pos_words = ', '.join(result['found_positive']) if result['found_positive'] else 'немає'
        neg_words = ', '.join(result['found_negative']) if result['found_negative'] else 'немає'
        self.words_label.config(text=f"Позитивні: {pos_words} | Негативні: {neg_words}")
    
    def clear_all(self):
        """Очищення всіх полів"""
        self.text_input.delete('1.0', tk.END)
        self.sentiment_label.config(text="Настрій: ---", style='Result.TLabel')
        self.score_label.config(text="Бали: ---")
        self.confidence_label.config(text="Впевненість: ---")
        self.words_label.config(text="Знайдені слова: ---")
        self.status_bar.config(text="Очищено. Готово до роботи.")


def main():
    root = tk.Tk()
    app = SentimentAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
