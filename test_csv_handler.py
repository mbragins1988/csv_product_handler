import pytest
from csv_product_handler import (read_csv, filter_data, 
                        parse_condition, aggregate_data)

# Фикстуры для тестовых данных
@pytest.fixture
def sample_csv_file(tmp_path):
    """Создает временный CSV файл для тестирования."""
    data = """name;brand;price;rating
iPhone 13;Apple;999;4.8
Galaxy S21;Samsung;799;4.6
Redmi Note 10;Xiaomi;299;4.4
Pixel 6;Google;899;4.7"""
    file_path = tmp_path / "test.csv"
    file_path.write_text(data)
    return str(file_path)

@pytest.fixture
def sample_data():
    """Возвращает данные в том же формате, что и read_csv."""
    return [
        {'name': 'iPhone 13', 'brand': 'Apple', 'price': '999', 'rating': '4.8'},
        {'name': 'Galaxy S21', 'brand': 'Samsung', 'price': '799', 'rating': '4.6'},
        {'name': 'Redmi Note 10', 'brand': 'Xiaomi', 'price': '299', 'rating': '4.4'},
        {'name': 'Pixel 6', 'brand': 'Google', 'price': '899', 'rating': '4.7'}
    ]

# Тесты для read_csv
def test_read_csv(sample_csv_file):
    data = read_csv(sample_csv_file)
    assert len(data) == 4
    assert data[0]['name'] == 'iPhone 13'
    assert data[1]['brand'] == 'Samsung'
    assert data[2]['price'] == '299'

def test_read_csv_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        read_csv("nonexistent_file.csv")

# Тесты для parse_condition
def test_parse_condition():
    col, op, val = parse_condition("price>500")
    assert col == "price"
    assert op == ">"
    assert val == "500"

    col, op, val = parse_condition("brand=Apple")
    assert col == "brand"
    assert op == "="
    assert val == "Apple"

def test_parse_condition_invalid():
    with pytest.raises(ValueError):
        parse_condition("price!500")

# Тесты для filter_data
def test_filter_data_equal(sample_data):
    filtered = filter_data(sample_data, "brand=Apple")
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'iPhone 13'

def test_filter_data_greater_than(sample_data):
    filtered = filter_data(sample_data, "price>800")
    assert len(filtered) == 2
    assert all(float(row['price']) > 800 for row in filtered)

def test_filter_data_less_than(sample_data):
    filtered = filter_data(sample_data, "price<500")
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'Redmi Note 10'

def test_filter_data_no_condition(sample_data):
    filtered = filter_data(sample_data, None)
    assert len(filtered) == len(sample_data)

# Тесты для aggregate_data
def test_aggregate_data_avg(sample_data):
    result = aggregate_data(sample_data, "price=avg")
    assert pytest.approx(result['avg']) == 749.0

def test_aggregate_data_min(sample_data):
    result = aggregate_data(sample_data, "price=min")
    assert result['min'] == 299.0

def test_aggregate_data_max(sample_data):
    result = aggregate_data(sample_data, "price=max")
    assert result['max'] == 999.0

def test_aggregate_data_invalid_column(sample_data):
    result = aggregate_data(sample_data, "invalid=avg")
    assert result is None

def test_aggregate_data_invalid_func(sample_data):
    with pytest.raises(ValueError):
        aggregate_data(sample_data, "price=invalid")

# Интеграционные тесты
def test_integration_filter_then_aggregate(sample_data):
    filtered = filter_data(sample_data, "price>800")
    result = aggregate_data(filtered, "price=avg")
    assert pytest.approx(result['avg']) == (999 + 899) / 2

def test_empty_data_aggregate():
    result = aggregate_data([], "price=avg")
    assert result is None
