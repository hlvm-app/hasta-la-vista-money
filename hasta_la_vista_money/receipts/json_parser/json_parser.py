def parse_json(json_data: dict, key: str) -> list[dict] | int | str | None:
    """
    Модуль разбора json данных.

    Функция для разбора json данных. Принимает словарь и ключ для поиска значения в переданном словаре.

    :param json_data: dict
        Словарь с данными.
    :param key: str
        Ключ для поиска в словаре.
    :return: list[dict] | int | str | None
        Словарь внутри списка, либо None
    """
    if isinstance(json_data, dict):
        for value in json_data.values():
            if isinstance(value, dict):
                result = parse_json(value, key)
                if result is not None:
                    return result
            elif (
                isinstance(value, list)
                and len(value) > 0
                and isinstance(value[0], dict)
            ):
                result = parse_json(value[0], key)
                if result is not None:
                    return result
            elif key in json_data:
                return json_data[key]
    return None
