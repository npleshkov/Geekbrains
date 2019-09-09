st = ('разработка', 'сокет', 'декоратор', 'function', 'method')

for i in st:
    bytes_data_u = i.encode('utf-8')
    #bytes_data_l = i.encode('latin-1')

    print(bytes_data_u.decode('utf-8'))
    #print(bytes_data_l.decode('latin-1'))

