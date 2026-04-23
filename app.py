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
        "title": f"РТ-Информационные Технологии",
        "content": f"<p>Содержание слайда {i} из презентации «Горизонт-ВС».</p>"
    }

# Точные заголовки для ключевых слайдов (используются в модальном окне)
slides_data[4]  = {"title": "Высокая доступность виртуальной инфраструктуры", "content": ""}
slides_data[6]  = {"title": "Живая миграция ВМ между серверами", "content": ""}
slides_data[9]  = {"title": "Affinity и Anti-Affinity", "content": ""}
slides_data[15] = {"title": "Подключение внешних хранилищ данных NFS, iSCSI, FC, Ceph", "content": ""}
slides_data[17] = {"title": "Миграция и клонирование данных ВМ между дисковыми разделами без прерывания доступа к ВМ (SDRS)", "content": ""}
slides_data[20] = {"title": "Контакты", "content": "<p>Ирина Барламова, Денис Обиднык<br>+7 981 751 4412<br>info@rt-intech.ru<br>www.rt-intech.ru</p>"}
slides_data[22] = {"title": "Добавление ресурсов работающей ВМ без необходимости ее выключения", "content": ""}
slides_data[25] = {"title": "Снэпшоты ВМ", "content": ""}
slides_data[29] = {"title": "Поддержка Disaster Recovery", "content": ""}
slides_data[31] = {"title": "Поддержка ролевой модели", "content": ""}
slides_data[37] = {"title": "Аудит и статистика", "content": ""}
slides_data[43] = {"title": "Полный и инкрементальный бекап ВМ", "content": ""}
slides_data[47] = {"title": "Импорт ВМ", "content": ""}
slides_data[50] = {"title": "Восстановление ВМ из копии", "content": ""}
slides_data[53] = {"title": "Сохранение СГУ", "content": ""}
slides_data[56] = {"title": "ОТЧЕТНОСТЬ", "content": ""}
slides_data[59] = {"title": "ПУЛЫ рабочих столов", "content": ""}
slides_data[63] = {"title": "Туннелирование", "content": ""}
slides_data[66] = {"title": "Разграничение прав доступа", "content": ""}
slides_data[69] = {"title": "ТОНКИЕ КЛИЕНТЫ ДЛЯ РАЗНЫХ ОС", "content": ""}
slides_data[90] = {"title": "Контакты", "content": "<p>Ирина Барламова, Денис Обиднык<br>+7 981 751 4412<br>info@rt-intech.ru<br>www.rt-intech.ru</p>"}

# ------------------------------------------------------------
# Группировка разделов: ключ = номер плитки, значение = список слайдов для показа
# ------------------------------------------------------------
sections = {
    4:  [5],
    6:  [7, 8],
    9:  [10, 11, 12, 13, 14],
    15: [16],
    17: [18, 19, 20, 21],
    20: [90],                      # плитка "Контакты" показывает слайд 90
    22: [23, 24],
    25: [26, 27, 28],
    29: [30],
    31: [32, 33, 34, 35, 36],
    37: [38, 39, 40, 41, 42],
    43: [44, 45, 46],
    47: [48, 49],
    50: [51, 52],
    53: [54, 55],
    56: [57, 58],
    59: [60, 61, 62],
    63: [64, 65],
    66: [67, 68],
    69: list(range(70, 90))        # слайды 70..89
}

tiles = [4, 6, 9, 15, 17, 20, 22, 25, 29, 31, 37, 43, 47, 50, 53, 56, 59, 63, 66, 69]

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