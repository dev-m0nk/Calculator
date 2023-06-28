from stack import Stack
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]

    def __str__(self):
        return " ".join(str(item) for item in self.items[::-1])

    def size(self):
        return len(self.items)


from simple_calculator import SimpleCalculator


class AdvancedCalculator(SimpleCalculator):
    def __init__(self):
        super().__init__()
        self.tokens = []

    def evaluate_expression(self, input_expression):
        self.tokens = self.tokenize(input_expression)
        result = self.evaluate_list_tokens(self.tokens)
        self.history.append((input_expression, result))
        return result

    def tokenize(self, input_expression):
        expression = "".join(input_expression.split())
        tokens = Stack()
        start = 0
        for i in range(len(expression)):
            if expression[i] in ["+", "-", "*", "/", "{", "}", "(", ")"]:
                a = self.int_if_num(expression[start:i])
                if a != "":
                    tokens.push(a)
                tokens.push(expression[i])
                start = i + 1
        a = self.int_if_num(expression[start:])
        if a != "":
            tokens.push(a)
        return tokens.items

    def check_brackets(self, list_tokens):
        bracket = {"{": 1, "}": 1, "(": 2, ")": 2}
        open_bracket = Stack()
        check = True
        for i in list_tokens:
            if i in ["{", "("]:
                if not open_bracket.is_empty():
                    if bracket[i] == 1 and bracket[open_bracket.peek()] == 2:
                        check = False
                open_bracket.push(i)
            elif i in ["}", ")"]:
                if open_bracket.is_empty():
                    check = False
                else:
                    if bracket[open_bracket.peek()] != bracket[i]:
                        check = False
                    open_bracket.pop()
        return check and open_bracket.is_empty()

    def evaluate_list_tokens(self, list_tokens):
        operator = ["/", "*", "-", "+"]
        if not self.check_brackets(list_tokens):
            return "Error"
        else:
            open_b = {0: "(", 1: "{"}
            close_b = {0: ")", 1: "}"}
            for i in [0, 1]:
                while list_tokens.count(open_b[i]) != 0:
                    start = self.last_ind(list_tokens, open_b[i]) + 1
                    end = list_tokens.index(close_b[i])
                    if start > 1:
                        if list_tokens[start - 2] not in operator + ["{", "("]:
                            return "Error"
                    if end < len(list_tokens) - 1:
                        if list_tokens[end + 1] not in operator + ["}", ")"]:
                            return "Error"
                    simple_expr = list_tokens[start:end]
                    temp_res = self.evaluate_simple_expr(simple_expr)
                    if temp_res == "Error":
                        return temp_res
                    list_tokens = list_tokens[:start - 1] + [temp_res] + list_tokens[end + 1:]
        if len(list_tokens) != 1:
            return self.evaluate_simple_expr(list_tokens)
        return list_tokens[0]

    def evaluate_simple_expr(self, list_simple_expr):
        if len(list_simple_expr) == 0:
            return "Error"
        for i in ["/", "*", "-", "+"]:
            while list_simple_expr.count(i) != 0:
                r = list_simple_expr.index(i)
                if r != 0 and r != len(list_simple_expr) - 1:
                    op1 = list_simple_expr[r - 1]
                    op2 = list_simple_expr[r + 1]
                    if not (isinstance(op1, int) or isinstance(op2, int)):
                        return "Error"
                    temp_result = self.calculate(op1, i, op2)
                    list_simple_expr = list_simple_expr[:r - 1] + [temp_result] + list_simple_expr[r + 2:]
                else:
                    return "Error"
        return list_simple_expr[0]

    def get_history(self):
        return self.history

    def calculate(self, operand1, operator, operand2):
        if operator == "+":
            return operand1 + operand2
        elif operator == "-":
            return operand1 - operand2
        elif operator == "*":
            return operand1 * operand2
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            return operand1 / operand2
        else:
            return "Error"

    def int_if_num(self, chr):
        try:
            return int(chr)
        except ValueError:
            return chr

    def last_ind(self, list_tok, e):
        n = len(list_tok)
        for i in range(n):
            if list_tok[n - 1 - i] == e:
                return n - 1 - i
