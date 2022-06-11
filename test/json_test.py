import json

def manage_accountCode():
    pass

if __name__ == '__main__':
    new_account="test_user"
    new_code="324234234123ASC"

    with open('../access_code.json', 'r') as f:
        json_data = json.load(f)

    json_data[new_account]=new_code

    with open('../access_code.json', 'w') as f:
        json.dump(json_data,f)

