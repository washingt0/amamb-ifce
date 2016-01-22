def eval(expr, context):
	"""Resolve uma expressao `expr` utilizando os
	argumentos contidos na lista `context`.
	"""
	stack = []
	for token in expr :
		if token >= 42 and token <= 47 :
			t2 = stack.pop()
			t1 = stack.pop()
			if token == 43 :
				# adicao
				result = t1 + t2
			elif token == 45 :
				# subtracao
				result = t1 - t2
			elif token == 42 :
				# multiplicacao
				result = t1 * t2
			elif token == 47 :
				# divisao
				result = t1 / t2
			# empilha resultado
			stack.append(result)
		elif token >= 0 and token <= 9 :
			stack.append(context[token])

	return stack.pop()

def compile(tokens):
	"""Gera uma expressao a partir da string `tokens`.
	Retorna tupla contendo a expressao compilada em RPN,
	uma string de formato para exibicao legivel da expressao
	e a quantidade de argumentos que a expressao necessita.
	"""
	# definicao da ordem de precedencia dos operadores
	OP_PRECED = {
		43: 1, # adicao
		45: 1, # subtracao
		42: 2, # multiplicacao
		47: 3, # divisao
	}
	stack = []
	rpn_expr = []
	format_expr = ''
	length = 0
	for ch in tokens :
		token = ord(ch)
		# token de operador
		if token >= 42 and token <= 47 :
			# desempilha operadores precedentes na expressao
			while len(stack) > 0 :
				op = stack.pop()
				if not (OP_PRECED[op] >= OP_PRECED[token]) :
					stack.append(op)
					break
				rpn_expr.append(op)
			# empilha operador
			stack.append(token)
			format_expr += ch
		# token de argumento
		elif token >= 48 and token <= 57 :
			arg = token - 49
			if arg >= length :
				length = arg + 1
			rpn_expr.append(arg)
			format_expr += ' {%d} ' % arg
	# desempilha operadores restantes na expressao
	while len(stack) > 0 :
		rpn_expr.append(stack.pop())

	return rpn_expr, format_expr, length
