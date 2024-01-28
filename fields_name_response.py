import ast

def generate_field_names(data):
    """
    Generate field names from the provided data.

    Args:
    - data (dict): The data.

    Returns:
    - list: A list of field names.
    """
    field_names = []
    for key, value in data.items():
        print(key, value)
        if isinstance(value, list):
            nested_fields = list(value[0].keys())
            field_names.append({key: nested_fields})
        else:
            field_names.append(key)
    return field_names

def get_list_of_currency(data):
    """
    Get a list of 'currency' values from the 'exchangeRate' list.

    Args:
    - data (dict): The data.

    Returns:
    - list: A list of 'currency' values.
    """
    list_of_currency = []
    if 'exchangeRate' in data and isinstance(data['exchangeRate'], list):
        for entry in data['exchangeRate']:
            if 'currency' in entry:
                list_of_currency.append(entry['currency'])
    return list_of_currency

# Example usage:
if __name__ == '__main__':
    with open('example_response.txt', 'r') as file:
        file_content = file.read()
        response_data = ast.literal_eval(file_content)

    # Generate field names
    field_names = generate_field_names(response_data)
    print("Field Names:", field_names)

    # Get list of 'currency' values
    list_of_currency = get_list_of_currency(response_data)
    print("List of Currency:", list_of_currency)
