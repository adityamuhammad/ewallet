def enum(**enums):
    return type('Enum', (), enums)

Transaction_Type = enum(DEBIT='debit', KREDIT='credit')