def validate_code(field, value, error):
    code_list = ['bni', 'bri', 'mandiri']
    if value not in code_list:
        error(field, "Code is invalid")

bank_transfer_validation_schema = {
    'amount': {
        'type': 'integer',
        'required': True
    },
    'code': {
        'type': 'string',
        'validator': validate_code,
        'required': True
    },
    'user_agent': {
        'type': 'string',
        'required': True
    },
    'ip': {
        'type': 'string',
        'required': True
    },
    'location': {
        'type': 'string',
        'required': True
    },
    'user_id': { 
        'type': 'integer',
        'required': True
    },
    'author': {
        'type': 'string',
        'required': True
    }
}
