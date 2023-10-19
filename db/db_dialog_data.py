from src.utils import save_data, load_data


def get_api_lobject(tg_id, type_value):
    try:
        result = load_data(f'{tg_id}_{type_value}')
    except:
        result = None
    return result


def update_data(tg_id, type_value, data):
    try:
        result = save_data(data, f'{tg_id}_{type_value}')
    except:
        result = None
    return result


