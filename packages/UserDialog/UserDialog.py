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
def message(msg):
    print(msg)
    print('press enter to continue', end='')
    input()

def validate(reply, validSet):
    for elem in validSet:
        if reply == elem:
            return True
    return False

