import shutil
from pypdf import PdfReader
import os


def process_pdf(file_path):
    reader = PdfReader(file_path)
    page = reader.pages[0]

    slovar = {
        "Банк": "",
        "Получатель": "",
        "Платежка": "",
        "Сумма": ""
    }

    lines = page.extract_text().split("\n")
    y = len(lines)

    for i in range(y):
        # ПЛАТЕЖКА + ДАТА
        if lines[i].startswith("ПЛАТЕЖНОЕ ПОРУЧЕНИЕ № "):  # Промсвязьбанк
            pay = lines[i][len("ПЛАТЕЖНОЕ ПОРУЧЕНИЕ № "):]
            for p in range(len(pay)):
                if pay[p] == " ":
                    px = p + 6
                    pay = pay[:px]
                    slovar["Платежка"] = pay
                    break
        elif lines[i].startswith("ПЛАТЁЖНОЕ ПОРУЧЕНИЕ "):  # Альфабанк
            pay = lines[i][len("ПЛАТЁЖНОЕ ПОРУЧЕНИЕ "):]
            for p in range(len(pay)):
                if pay[p] == " ":
                    px = p + 6
                    pay = pay[:px]
                    slovar["Платежка"] = pay
                    break
        slovar["Платежка"] = slovar["Платежка"].replace(" ", "_").replace(".", "-")

        # ПОЛУЧАТЕЛЬ
        if lines[i].startswith("ИНН "):
            inn_poluch = lines[i][len("ИНН "):]
            for p in range(3, len(inn_poluch)):
                if inn_poluch[p] == " ":
                    inn_poluch = inn_poluch[:p]
                    if inn_poluch.replace(" ", "") != "7725371950":
                        slovar["Получатель"] = lines[i + 1].replace('"', "").replace("ООО ", "").replace(" ", "_")
                    break

        # СУММА
        if lines[i].startswith("ПлательщикСумма "):
            slovar["Сумма"] = lines[i][len("ПлательщикСумма "):]

        if (lines[i].startswith("ИНН ")) and " Сумма " in lines[i]:
            slovar["Сумма"] = lines[i][len("ИНН "):]
        slovar["Сумма"] = slovar["Сумма"].replace(" ", "").replace("7725371950", "").replace("КПП", "").replace(
            "772601001", "").replace("Сумма", "")

        # Банк ОТПРАВИТЕЛЬ
        if lines[i] in "Сч. № 40702810401100013122":  # Альфа
            slovar["Банк"] = "Альфабанк"
        elif lines[i] in "Сч. № 40702810400000274057":  # Псб
            slovar["Банк"] = "Промсвязьбанк"

    name_file = f'пп_{slovar["Получатель"]}_{slovar["Платежка"]}={slovar["Сумма"]}.pdf'

    # Перемещение и переименование файла
    if file_path != name_file:
        shutil.copyfile(file_path, name_file)
        os.remove(file_path)

    return name_file