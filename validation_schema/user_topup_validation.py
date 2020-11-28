user_topup_validation_schema = {
    'amount': {
        'type': 'integer',
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
    'type': {
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
