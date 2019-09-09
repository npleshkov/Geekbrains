st = ('разработка', 'сокет', 'декоратор')

for i in st:
    t = bytes(i, encoding='utf-8')
    print(t.decode())
