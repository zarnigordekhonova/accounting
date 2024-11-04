
import re

def is_valid_vin(vin: str) -> bool:
    if len(vin) != 17:
        return False

    vin_pattern = re.compile(r'^[A-HJ-NPR-Z0-9]{17}$', re.IGNORECASE)
    if not vin_pattern.match(vin):
        return False
    return True
