st = ('разработка', 'сокет', 'декоратор', 'function', 'method')

for i in st:
    data = i.encode('utf-8').decode('latin-1').encode('latin-1').decode('utf-8')
    print('data type ', type(data), 'data ', data)
    bytes_data_u = data.encode('utf-8')
    print('bytes_data_u type ', type(bytes_data_u))
    print(bytes_data_u.decode('utf-8'))


