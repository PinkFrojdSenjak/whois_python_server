import re
import json

def get_synonims() -> dict:
    return {
        'Domain Name': ['domain name', 'domain'],
        'Registrar': ['registrar', 'person'],
        'Registrant': ['registrant', 'holder', 'creator', 'created by'],
        'Registration Date':['registration date', 'registered on', 'created', 'creation date'],
        'Expiration Date':['expiration date','expiry date', 'paid-till', 'registry expiry date', 'expire', 'expires'] 
    }

def get_registry() -> dict:
    with open('registry.json') as f:
        return json.load(f)
        
    