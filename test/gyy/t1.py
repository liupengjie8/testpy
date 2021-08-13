import json

json_str = '{"a16": "29", "b11c": "1"}'
json_obj = json.loads(json_str)
a16 = json_obj['a16']
b11c = json_obj['b11c']
print(a16)
print(b11c)
print(b11c != '1')
print(a16 == '0')
print(a16 > '28')
print(a16 == '')

