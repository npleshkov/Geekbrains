st = ('разработка', 'сокет', 'декоратор')

for i in st:
    t = bytes(i, encoding='utf-8')
    print(t.decode())

# for i in st:
#
#     # print(f' Тип {type(b'i')},  длина строки {len(i)}')
#     if 'Some string' == b''i'':
#         print('1')
#     else:
#         print(2)
#
