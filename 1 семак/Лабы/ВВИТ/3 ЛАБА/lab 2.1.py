def write_file():
    with open('user_input.txt', 'w') as file:
        file.write(input())
write_file()