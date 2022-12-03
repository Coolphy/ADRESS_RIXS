def text_folding(list, column_number, row_number):
    list_new = [None] * column_number
    for i in range (column_number):
        j = 0
        list_new[i] = list[i]
        j = j + 1
        while i + j * column_number < len(list):
            list_new[i] = f"{list_new[i]}\t{list[i+j column_number, row_number]}"
            j = j + 1

    return list_new


list = [f"{x}" for x in range(1000)]
# print(list)

print("########")

newlist = text_folding(list, 10)
for x in newlist:
    print(x)
