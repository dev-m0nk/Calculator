from stack import Stack

class SimpleCalculator:
    def __init__(self):
        self.history = []
        pass

    def evaluate_expression(self, input_expression):
        expression = input_expression.replace(' ','')
        operator = None
        operand = []
        if len(expression)<3 or expression.count(' ')>0:
            self.history.append((input_expression, 'Error'))
            return 'Error'

        operators = ['+','-','*','/']
        operand1 = ''
        operand2 = ''
        operator = ''
        for char in expression:
            if char in operators:
                operator = char
                break
            else:
                operand1 += char
        operand2 = expression[len(operand1)+1:]

        if operator == "+":
            result = float(operand1) + float(operand2)
        elif operator == "-":
            if operand2 != '':
                result = float(operand1) - float(operand2)
            else:
                self.history.append((input_expression, "Error"))
                return "Error"
        elif operator == "*":
            result = float(operand1) * float(operand2)
        elif operator == "/":
            if operand2 != 0:
                result = float(operand1) / float(operand2)
            else:
                self.history.append((input_expression, "Error"))
                return "Error"

        self.history.append((input_expression, result))
        return result

    def get_history(self):
        return self.history[::-1]
    pass


calculator = SimpleCalculator()
answer = calculator.evaluate_expression("2 + 3") # answer should be 5.0
print(answer)
answer = calculator.evaluate_expression("2 +") # answer should be "Error"
print(answer)
history = calculator.get_history() # history should be [("2 +", "Error"), ("2 + 3", 5.0]
print(history)

