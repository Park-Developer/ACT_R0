class ConfigError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class NegativeNumberError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class Number:
    def __init__(self, n):
        if n < 0:
            raise NegativeNumberError('음수는 담을 수 없습니다')


if __name__=="__main__":
    try:
        n = Number(-1)
    except NegativeNumberError as e:
        print(e)