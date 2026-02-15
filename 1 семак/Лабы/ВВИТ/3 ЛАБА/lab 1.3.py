def read_file():
    method = int(input("1-Полное чтение; 2-Построчное чтение\n Введите тип чтения: "))

    if method == 1:
        with open('example.txt', 'r') as file:
            content = file.read()
            print(content)

    if method == 2:
        with open('example.txt', 'r') as file:
            for line in file:
                print(line)
read_file()