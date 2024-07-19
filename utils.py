def process_entry(entry):
    """
    Обрабатывает одну запись и преобразует байтовые строки в строки.
    """
    processed_entry = {}
    for attr, values in entry.items():
        if isinstance(values[0], bytes):
            processed_entry[attr] = values[0].decode("utf-8")
        else:
            processed_entry[attr] = values[0]
    return processed_entry


def process_search_results_user_by_uid(results):
    if results:
        dn, entry = results[0]
        return process_entry(entry)
    return None


def process_search_results_users_list(results):
    """
    Обрабатывает результаты поиска и преобразует
    байтовые строки в строки при необходимости.
    """
    users = []
    for dn, entry in results:
        if dn:
            users.append(process_entry(entry))
    return users


def encode_attributes(attributes):
    """Преобразует строк в байтовые строки."""
    encoded_attributes = {}
    for key, value in attributes.items():
        if isinstance(value, list):
            encoded_attributes[key] = [v.encode("utf-8") for v in value]
        else:
            encoded_attributes[key] = value.encode("utf-8")
    return encoded_attributes
