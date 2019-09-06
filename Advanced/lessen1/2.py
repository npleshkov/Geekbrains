st = ('class', 'function', 'method')
st = ('разработка', 'сокет', 'декоратор')

b'class'
b'function'
b'method'

print(bytes('class', encoding = 'utf-8'))

print(type(b'class'))
for i in st:
    print(i)
    print(bytes(i, encoding = 'utf-8'))
    print(type(bytes(i, encoding = 'utf-8')))
    # print(f' Тип {type(b'class')}')
