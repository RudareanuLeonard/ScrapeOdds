import json

test_data = {
    'name': 'Bob',
    'test': {
        'test1': 'test1',
        'test2': 'test2'
    }
}

with open('test.json', 'w') as f:
    json.dump(test_data,f)