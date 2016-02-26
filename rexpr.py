from math import sqrt

# definicao da ordem de precedencia dos operadores
OP_PRECED = {
    43: 1,  # adicao
    45: 1,  # subtracao
    42: 2,  # multiplicacao
    47: 3,  # divisao
    94: 4,  # potencia
    113: 9,  # raiz quadrada
}

# modificadores de precedencia
PRECED_MOD = {
    41: 40,
    93: 91,
    125: 123
}


def pop_token(stack):
    """Retira um token do topo da pilha de execucao.
    """
    a = -1
    t = stack.pop()
    if type(t) is tuple:
        a = t[0]
        t = t[1]
    return a, t


def eval(expr, context):
    """Resolve uma expressao `expr` utilizando os
    argumentos contidos na lista `context`.
    """
    stack = []
    for token in expr:
        if token in OP_PRECED:
            a2, t2 = pop_token(stack)
            if token != 113:  # operadores de operando unico
                a1, t1 = pop_token(stack)
            if token == 43:  # adicao
                result = t1 + t2
            elif token == 45:  # subtracao
                result = t1 - t2
            elif token == 42:  # multiplicacao
                result = t1 * t2
            elif token == 47:  # divisao
                if a1 != -1:
                    # prepara resultado exato
                    t1 = t1 * t2
                    context[a1] = t1
                # tenta evitar divisao por zero
                if t2 == 0 and a2 != -1:
                    t2 = 1
                    context[a2] = t2
                result = t1 / t2
            elif token == 94:  # potencia
                result = t1 ** t2
            elif token == 113:  # raiz quadrada
                if a2 != -1:
                    # prepara resultado exato
                    t2 **= 2
                    context[a2] = t2
                result = sqrt(t2)
            # empilha resultado
            stack.append(result)
        elif 0 <= token <= 9:
            stack.append((token, context[token]))
    a, result = pop_token(stack)
    return result, context


def compile(tokens):
    """Gera uma expressao a partir da string `tokens`.
    Retorna tupla contendo a expressao compilada em RPN,
    uma string de formato para exibicao legivel da expressao
    e a quantidade de argumentos que a expressao necessita.
    """
    stack = []
    rpn_expr = []
    format_expr = ''
    length = 0
    for ch in tokens:
        token = ord(ch)
        # token de argumento
        if 49 <= token <= 57:
            arg = token - 49
            if arg >= length:
                length = arg + 1
            rpn_expr.append(arg)
            format_expr += '{%d}' % arg
        # token de operador
        elif token in OP_PRECED:
            # desempilha operadores precedentes na expressao
            while len(stack) > 0:
                op = stack.pop()
                if (not op in OP_PRECED) or (OP_PRECED[op] < OP_PRECED[token]):
                    stack.append(op)
                    break
                rpn_expr.append(op)
            # empilha operador
            stack.append(token)
            if token == 113:
                format_expr += 'sqrt'
            else:
                format_expr += ch
        # fechamento de precedencia
        elif token in PRECED_MOD:
            # desempilha operadores ate encontrar abertura
            while len(stack) > 0:
                op = stack.pop()
                if op == PRECED_MOD[token]:
                    break
                rpn_expr.append(op)
            if token == 125:
                format_expr += ch
            format_expr += ch
        # abertura de precedencia
        elif token in PRECED_MOD.values():
            stack.append(token)
            if token == 123:
                format_expr += ch
            format_expr += ch

    # desempilha operadores restantes na expressao
    while len(stack) > 0:
        rpn_expr.append(stack.pop())

    return rpn_expr, format_expr, length
