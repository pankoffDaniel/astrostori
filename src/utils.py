import os


def get_correct_date(date: str) -> tuple:
    """Принимает данные в формате 2020-09-05, но возвращает 2020, 9, 5."""
    year, month, day = date.split('-')
    incorrect_date_numbers = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
    if month in incorrect_date_numbers:
        month = month[-1]
    if day in incorrect_date_numbers:
        day = day[-1]
    return year, month, day


def rotate_svg_image(image_path: str, angle: str):
    """Поворачивает SVG изображение на угол angle и очищает от надписи."""
    with open(image_path, 'r') as image:
        html = image.read()
        html = html.replace('<svg ', f'<svg style="transform: rotate({angle}deg);" ')
        html = html.replace('<text x="1480.00" y="1480.00" font-family="Arial,Helvetica,sans-serif" font-size="11" text-anchor="end" stroke="none" fill="#888888" >https://in-the-sky.org</text>', '')
    with open(image_path, 'w') as image:
        image.write(html)


def delete_file_list(directory, file_type):
    """Удаляет файлы по расширению из выбранной директории."""
    directory_file_list = os.listdir(directory)
    for file_name in directory_file_list:
        if file_name.endswith(file_type):
            os.remove(os.path.join(directory, file_name))


def get_starmap_catalog_image_upload_path(instance: object, filename: str) -> str:
    """Возвращает динамический относительный путь к каталогу звездных карт."""
    return os.path.join('starmap_catalog', instance.title, filename)
