# Matches GB followed by 9/12 digits or GB followed by GD/HA and 3 digits
UK_VAT_VALIDATION_REGEX = "^(GB)?([0-9]{9}([0-9]{3})?|(GD|HA)[0-9]{3})$"

# Matches GB followed by 12 or 15 numbers, eg GB123456789000
UK_EORI_VALIDATION_REGEX = "^(GB)([0-9]{12})$|^(GB)([0-9]{15})$"
