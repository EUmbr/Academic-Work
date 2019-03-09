def parse(text, sign):
    c = 0
    a = []
    s = ''
    for i in text:
        if i == '(':
            c -= 1
        if i == ')':
            c += 1
        if i == sign and c == 0:
            a.append(s)
            s = ''
        else:
            s += i
    a.append(s)

    for i in range(len(a)):
        while a[i][0] == '(' and a[i][-1] == ')' and check(a[i][1:-1]) is True:
            a[i] = a[i][1:-1]

    for i in range(len(a)):
        if check_parse(a[i], sign):
            a[i] = parse(a[i], sign)

    a = norm(a)

    return a


def norm(a):
    norm_list = []
    for i in a:
        if type(i) == list:
            for j in i:
                norm_list.append(j)
        else:
            norm_list.append(i)
    return norm_list


def check_parse(text, sign):
    c = 0
    for i in text:
        if i == '(':
            c -= 1
        if i == ')':
            c += 1
        if i == sign and c == 0:
            return True
    return False


def check_sign(text):
    c = 0
    for i in text:
        if i == '(':
            c -= 1
        if i == ')':
            c += 1
        if i == '+' and c == 0:
            return '+'
        elif i == '*' and c == 0:
            return '*'
    return 0


def check(string):
    stack = []
    for i in string:
        if i == '(':
            stack.append(i)
        if i == ')':
            if len(stack) == 0:
                return False
            if stack[-1] == '(':
                stack = stack[:-1]
            else:
                return False
    return (not stack)


print(parse('(a*b+b*(c+d+e)*c+f)*(c*d+k)', '*'))
