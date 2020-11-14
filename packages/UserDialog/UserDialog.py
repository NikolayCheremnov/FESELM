#код диалогового анализа пользователем

# получение ввода пользователя в ответ на информацию
def dialog(msg, validSet):
    validity = False
    while not validity:
        print('user dialog:', msg, ': ', end='')
        reply = input()
        validity = validate(reply, validSet)
        if not validity:
            print('data is invalid, try again (available: ', validSet, ')')
        else:
            return reply

# вывод сообщения
def message(msg):
    print(msg)
    print('press enter to continue', end='')
    input()

# получение команды с параметрами
def cmdDialog(msg):
    print('user dialog:', msg, ': ', end='')
    cmd = input().split()
    return cmd

# валидация
def validate(reply, validSet):
    for elem in validSet:
        if reply == elem:
            return True
    return False
