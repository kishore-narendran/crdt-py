status_codes = {
    'success': {'message': 'success', 'code': 0},
    'failure': {'message': 'failure', 'code': 1},
    'existing_key': {'message': 'success', 'code': 2,
                     'description': 'An existing element with the same key found'},
    'data_type_mismatch': {'message': 'failure', 'code': 2,
                           'description': 'the key corresponds to another data type'},
    'missing_key_or_state': {'message': 'failure', 'code': 3,
                             'description': 'Key/State of counter was missing or malformed'},
    'key_not_found': {'message': 'failure', 'code': 4,
                      'description': 'Key/State of counter not found in key/value store'}

}
