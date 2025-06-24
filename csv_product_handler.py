import argparse
import csv
from tabulate import tabulate


def read_csv(file):
    """Открывает CSV-файл и возвращает данные в виде списка словарей."""

    with open(file, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        return list(reader)


def filter_data(data, where):
    """Фильтрация данных на основе условия 'where'."""

    if not where:
        return data

    column, operator, value = parse_condition(where)

    filtered = []
    for row in data:
        row_value = row[column]
        
        if operator == '=':
            if str(row_value) == str(value):
                filtered.append(row)
        elif operator == '>':
            try:
                if float(row_value) > float(value):
                    filtered.append(row)
            except ValueError:
                continue
        elif operator == '<':
            try:
                if float(row_value) < float(value):
                    filtered.append(row)
            except ValueError:
                continue

    return filtered


def parse_condition(where):
    """Разбивает строку условия на столбец, оператор и значение."""

    operators = ['>', '<', '=']
    for op in operators:
        if op in where:
            column, value = where.split(op)
            return column.strip(), op, value.strip()
    raise ValueError(f"Введено неверное значение: {where}")


def aggregate_data(data, condition):
    """Рассчитывает значение (среднее, минимальное, максимальное) для указанного столбца."""

    if not condition:
        return None

    column, func = condition.split('=')
    column = column.strip()
    func = func.strip().lower()
    
    numeric_values = []
    for row in data:
        try:
            numeric_values.append(float(row[column]))
        except (ValueError, KeyError):
            continue
    
    if not numeric_values:
        return None
    
    if func == 'avg':
        result = sum(numeric_values) / len(numeric_values)
    elif func == 'min':
        result = min(numeric_values)
    elif func == 'max':
        result = max(numeric_values)
    else:
        raise ValueError(f"Введено неверное значение: {func}")
    
    return {func: result}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')  # Убрали -- перед именем аргумента
    parser.add_argument('--where', default=None)
    parser.add_argument('--aggregate', default=None)
    args = parser.parse_args()
    
    data = read_csv(args.file)
    
    if args.where:
        data = filter_data(data, args.where)
        if data:
            print(tabulate(data, headers="keys", tablefmt="grid", showindex=True))
        else:
            print("Нет данных условий")
    
    if args.aggregate:
        result = aggregate_data(data, args.aggregate)
        if result:
            print(tabulate([result], headers="keys", tablefmt="grid", showindex=True))
        else:
            print("Нет данных агрегации")
    else:
        print(tabulate(data, headers="keys", tablefmt="grid", showindex=True))


if __name__ == '__main__':
    main()
