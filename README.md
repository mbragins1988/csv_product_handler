# CSV_PRODUCT_HANDLER

### Описание 
Скрипт Python обработки CSV-файла, поддерживающий операции: 
фильтрация с операторами «больше», «меньше» и «равно»
агрегация с расчетом среднего (avg), минимального (min) и максимального (max) значения.

### Как запустить проект

Клонировать репозиторий:

```
git clone git@github.com:mbragins1988/csv_product_handler.git   
```

Перейти в папку csv_product_handler

```
cd csv_product_handler
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```
для Windows
```
source venv/Scripts/activate
```
для Mac
```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip3 install -r requirements.txt
```

В директории csv_product_handler запустить скрипт для агрегации (среднее, максимальное, минимальное):

```
python csv_product_handler.py<"путь к csv-файлу"> --affregate "<название поля>=<значение>"
```

В директории csv_product_handler запустить скрипт для условий (больше, меньше, равно):

```
python csv_product_handler.py<"путь к csv-файлу"> --where "<название поля>=<значение>" 
```

Например

```
python csv_product_handler.py "C:\Users\mbrag\OneDrive\Desktop\csv_product_handler\test.csv" --aggregate "price=avg" 
```
```
python csv_product_handler.py "C:\Users\mbrag\OneDrive\Desktop\csv_product_handler\test.csv" --where "price>500"     
```

### Стек технологий:
- Python 3.8.10

### Авторы проекта
Михаил Брагин
