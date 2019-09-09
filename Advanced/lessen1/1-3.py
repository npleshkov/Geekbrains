st = ('разработка', 'сокет', 'декоратор', 'function', 'method')

for i in st:
    u = i.encode('utf-8')
    # l = bytes(i, encoding='latin-1')
    print(u.decode('utf-8'))
    # print(l.decode())

