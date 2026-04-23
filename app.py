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
slides_data[3] = {"title": "Экосистема – компоненты", "content": ""}
slides_data[5] = {"title": "Платформа серверной виртуализации (продолжение)", "content": ""}
slides_data[30] = {"title": "Сетевая виртуализация – детали", "content": ""}
slides_data[44] = {"title": "Резервное копирование – дедупликация", "content": ""}
slides_data[45] = {"title": "Резервное копирование – репликация", "content": ""}
slides_data[46] = {"title": "Резервное копирование – проверка", "content": ""}
slides_data[48] = {"title": "VDI – роуминг профилей", "content": ""}
slides_data[49] = {"title": "VDI – интеграция с AD", "content": ""}
slides_data[51] = {"title": "Мониторинг – триггеры", "content": ""}
slides_data[52] = {"title": "Мониторинг – SLA", "content": ""}
slides_data[7] = {"title": "Живая миграция – процесс", "content": ""}
slides_data[8] = {"title": "Живая миграция – требования", "content": ""}
slides_data[23] = {"title": "Кластеризация", "content": ""}
slides_data[24] = {"title": "Отказоустойчивость", "content": ""}
slides_data[10] = {"title": "Affinity – правила", "content": ""}
slides_data[11] = {"title": "Anti-Affinity – правила", "content": ""}
slides_data[12] = {"title": "Примеры использования", "content": ""}
slides_data[13] = {"title": "Настройка политик", "content": ""}
slides_data[14] = {"title": "Мониторинг affinity", "content": ""}
slides_data[18] = {"title": "Миграция SDRS – начало", "content": ""}
slides_data[19] = {"title": "Миграция SDRS – процесс", "content": ""}
slides_data[20] = {"title": "Миграция SDRS – без прерывания", "content": ""}
slides_data[21] = {"title": "Клонирование данных", "content": ""}
slides_data[26] = {"title": "Снэпшоты – создание", "content": ""}
slides_data[28] = {"title": "Снэпшоты – восстановление", "content": ""}
slides_data[32] = {"title": "Ролевая модель – администратор", "content": ""}
slides_data[33] = {"title": "Ролевая модель – оператор", "content": ""}
slides_data[34] = {"title": "Ролевая модель – пользователь", "content": ""}
slides_data[35] = {"title": "Ролевая модель – аудитор", "content": ""}
slides_data[36] = {"title": "Разграничение прав доступа", "content": ""}
slides_data[67] = {"title": "Управление доступом – детали", "content": ""}
slides_data[68] = {"title": "Управление доступом – примеры", "content": ""}
slides_data[38] = {"title": "Аудит – логи", "content": ""}
slides_data[39] = {"title": "Аудит – события", "content": ""}
slides_data[40] = {"title": "Аудит – отчёты", "content": ""}
slides_data[41] = {"title": "Статистика – производительность", "content": ""}
slides_data[42] = {"title": "Статистика – использование ресурсов", "content": ""}
slides_data[57] = {"title": "Отчётность – генерация", "content": ""}
slides_data[58] = {"title": "Отчётность – экспорт", "content": ""}
slides_data[70] = {"title": "Тонкие клиенты – обзор", "content": ""}
slides_data[71] = {"title": "Тонкие клиенты – Windows", "content": ""}
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
    8: list(range(70, 90)),                                          # Тонкие клиенты (70-89)
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