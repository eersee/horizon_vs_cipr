import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# ------------------------------------------------------------
# Текстовое наполнение слайдов (запасной вариант, если нет картинки)
# ------------------------------------------------------------
slides_data = {}

# Заглушки для всех слайдов от 1 до 90
for i in range(1, 91):
    slides_data[i] = {
        "title": f" ",
        "content": f"<p>Содержание слайда {i} из презентации «Горизонт-ВС».</p>"
    }

# Точные заголовки для ключевых слайдов (по желанию можно заполнить)
# Здесь можно добавить осмысленные заголовки для слайдов, которые будут показываться в модальном окне
slides_data[2] = {"title": "Экосистема Горизонт-ВС", "content": ""}
slides_data[3] = {"title": "Платформа серверной виртуализации", "content": ""}
slides_data[5] = {"title": "Высокая доступность", "content": ""}
slides_data[30] = {"title": "Отказоустойчивость", "content": ""}
slides_data[44] = {"title": "Полный и инкриментальный бекап", "content": ""}
slides_data[45] = {"title": "Полный и инкриментальный бекап", "content": ""}
slides_data[46] = {"title": "Полный и инкриментальный бекап", "content": ""}
slides_data[48] = {"title": "Импорт ВМ", "content": ""}
slides_data[49] = {"title": "Импорт ВМ", "content": ""}
slides_data[51] = {"title": "Восстановление ВМ из копии", "content": ""}
slides_data[52] = {"title": "Восстановление ВМ из копии", "content": ""}
slides_data[7] = {"title": "Живая миграция – процесс", "content": ""}
slides_data[8] = {"title": "Живая миграция – требования", "content": ""}
slides_data[23] = {"title": "Добавление ресурсов", "content": ""}
slides_data[24] = {"title": "Добавление ресурсов", "content": ""}
slides_data[10] = {"title": "Affinity и Anti-Affinity", "content": ""}
slides_data[11] = {"title": "Affinity и Anti-Affinity", "content": ""}
slides_data[12] = {"title": "Affinity и Anti-Affinity", "content": ""}
slides_data[13] = {"title": "Affinity и Anti-Affinity", "content": ""}
slides_data[14] = {"title": "Affinity и Anti-Affinity", "content": ""}
slides_data[18] = {"title": "Миграция и клонирование", "content": ""}
slides_data[19] = {"title": "Миграция и клонирование", "content": ""}
slides_data[20] = {"title": "Миграция и клонирование", "content": ""}
slides_data[21] = {"title": "Миграция и клонирование", "content": ""}
slides_data[26] = {"title": "Снэпшоты", "content": ""}
slides_data[28] = {"title": "Снэпшоты", "content": ""}
slides_data[32] = {"title": "Ролевая модель", "content": ""}
slides_data[33] = {"title": "Ролевая модель", "content": ""}
slides_data[34] = {"title": "Ролевая модель", "content": ""}
slides_data[35] = {"title": "Ролевая модель", "content": ""}
slides_data[36] = {"title": "Ролевая модель", "content": ""}
slides_data[67] = {"title": "Разграничение прав доступа", "content": ""}
slides_data[68] = {"title": "Разграничение прав доступа", "content": ""}
slides_data[38] = {"title": "Аудит и статистика", "content": ""}
slides_data[39] = {"title": "Аудит и статистика", "content": ""}
slides_data[40] = {"title": "Аудит и статистика", "content": ""}
slides_data[41] = {"title": "Аудит и статистика", "content": ""}
slides_data[42] = {"title": "Аудит и статистика", "content": ""}
slides_data[57] = {"title": "Отчётность", "content": ""}
slides_data[58] = {"title": "Отчётность", "content": ""}
slides_data[70] = {"title": "Тонкие клиенты – обзор", "content": ""}
slides_data[71] = {"title": "Мониторинг", "content": ""}
# ... можно продолжить для 70-89, но достаточно и общей заглушки
slides_data[90] = {"title": "Контакты", "content": "<p>Ирина Барламова, Денис Обиднык<br>+7 981 751 4412<br>info@rt-intech.ru<br>www.rt-intech.ru</p>"}

# ------------------------------------------------------------
# Группировка разделов: ключ = номер плитки (1..9), значение = список слайдов
# ------------------------------------------------------------
sections = {
    1: [2, 3, 5, 30] + list(range(44, 47)) + [48, 49] + [51, 52],   # Экосистема
    2: [7, 8, 23, 24],                                              # Живая миграция + добавление ресурсов
    3: list(range(10, 15)),                                          # Affinity и Anti-Affinity (10-14)
    4: list(range(18, 22)),                                          # Миграция и клонирование данных (18-21)
    5: [26, 28] + list(range(44, 47)),                               # Снэпшоты ВМ и бекапы (26,28,44-46)
    6: list(range(32, 37)) + [67, 68],                               # Ролевая модель и права доступа (32-36,67-68)
    7: list(range(38, 43)) + [57, 58],                               # Аудит, статистика и отчетность (38-42,57,58)
    8: list(range(70, 90)),                                          # Мониторинг и миграция (70-89)
    9: [90]                                                          # Контакты
}

tiles = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ------------------------------------------------------------
# Функция проверки наличия изображения слайда
# ------------------------------------------------------------
def image_exists(slide_num):
    for ext in ['.png', '.jpg', '.jpeg']:
        path = os.path.join('static', 'slides', f"{slide_num}{ext}")
        if os.path.exists(path):
            return f"/static/slides/{slide_num}{ext}"
    return None

# ------------------------------------------------------------
# Маршруты Flask
# ------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html', tiles=tiles, sections=sections)

@app.route('/api/slide/<int:slide_num>')
def get_slide(slide_num):
    img_url = image_exists(slide_num)
    if img_url:
        title = slides_data.get(slide_num, {}).get("title", f"Слайд {slide_num}")
        return jsonify({"title": title, "has_image": True, "image_url": img_url})
    else:
        data = slides_data.get(slide_num, {"title": f"Слайд {slide_num}", "content": "<p>Нет данных</p>"})
        return jsonify({
            "title": data["title"],
            "has_image": False,
            "content": data.get("content", "<p>Нет описания</p>")
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)