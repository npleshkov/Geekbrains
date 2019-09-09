st = ('разработка', 'сокет', 'декоратор', 'function', 'method')

for i in st:
    u = bytes(i, encoding='utf-8')
    # l = bytes(i, encoding='latin-1')
    print(u.decode())
    # print(l.decode())

    
    
