import pandas as pd
from munkres import Munkres, print_matrix
import numpy as np



matrix_pd = pd.DataFrame(columns=['105', '106', '107', '416б', '416б-1', '416а,б', '422', '3091', 'ГАСС', 'ИАС, 202', 'БАТО, 213']
                         ,
                         index=['Лебедев М.В.', 'Красненко А.Г.', 'Морозов И.О.', 'Корнеев Р.Л.', 'Чернов Д.А.', 'Автеньев Д.Г.', 'Шабалин К.Н.', 'Пачко Г.М.', 'Гладковская А.Ю.', 'Попова И.О.' ],
                         data=np.random.randint(0, 15, size=(10, 11)))




w = len(matrix_pd.columns)
h = len(matrix_pd.index)
print('Изначальная ширина - ' + str(w) + '          и Высота - ' + str(h))


for i in range(w - h):
    matrix_pd.loc['Empty slot ' + str(i)] = 0
for j in range(h - w):
    matrix_pd['Empty slot ' + str(j)] = 0


matrix_np = matrix_pd.values

print('''------------------------------------
          Исходная матрица''')
print_matrix(matrix_np)
print('''------------------------------------
       Переворачиваем матрицу''')

max = np.max(matrix_np)
matrix_np = np.array(list(map(lambda el: max - el, matrix_np)))

m = Munkres()

print_matrix(matrix_np)
print('''------------------------------------
    Производим венгерский флекс''')

index = m.compute(matrix_np)

total = 0
triplets = []
for row, column in index:
    value = matrix_pd.iloc[row, column]
    total += value
    triplets.append([matrix_pd.index[row], matrix_pd.columns[column], matrix_pd.iloc[row, column], 'Какой-то массив Тем'])
    print(f'({row}, {column}) -> {total}')
print(f'\ntotal profit = {total} \n')





matrix_triplets = pd.DataFrame(columns=('Учитель', 'Кабинет', 'Количество доступных тем', 'Доступные темы'), data=triplets).sort_values('Количество доступных тем').reset_index(drop=True)
#matrix_triplets['Доступные темы'].apply(check_for_intersections, axis=1, raw=True, result_type=None)

print(str(matrix_triplets) + '\n')


iteration_array = matrix_triplets.itertuples(index=True)
#for triplet in iteration_array:

    #print(triplet)

#Цикл не подойдет, нужна рекурсия