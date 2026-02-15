def write_file():
    method = int(input("1-Запись с нуля; 2-Запись с конца\n Введите тип записи: "))

    if method == 1:
        with open('user_input.txt', 'w') as file:
            file.write(input())
    if method == 2:
        with open('user_input.txt', 'a') as file:
            file.write(input())
write_file()