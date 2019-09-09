st = ('class', 'function', 'method')
st = ('разработка', 'сокет', 'декоратор')

data_bytes_1 = b'class'
data_bytes_2 = b'function'
data_bytes_3 = b'method'

print(bytes('class', encoding = 'utf-8'))

st = str(data_bytes_1,encoding = 'utf-8')

print(f' Тип {type(data_bytes_1)}, содержимое {str(data_bytes_1,encoding = "utf-8")},  длина строки {len(data_bytes_1)}')
# print(f'(Тип {type(b'class')} ))
for i in range (1,3):
    print(i)
    print('data_bytes_'+ (str(i)))
    print(f' Тип {type("data_bytes_"+ (str(i)))}')
    # print(type(bytes(i, encoding = 'utf-8')))
    # print(f' Тип {type(b'class')}')
