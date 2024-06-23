

def error_handler(e):
    error_messages = {}
    for field, errors in e.items():
        error_messages["error"] = "("+field+ ") " + errors[0]
    return error_messages