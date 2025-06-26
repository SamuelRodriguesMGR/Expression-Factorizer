
# Написать программу, которая по заданной формуле строит дерево и
# производит вычисления с помощью построенного дерева. 
# Формула задана в традиционной инфиксной записи, в ней могут быть скобки, максимальная
# степень вложенности которых ограничивается числом 10. 

# Аргументами могут быть целые числа и переменные, задаваемые однобуквенными именами.
# Допустимые операции: +, -, *, /. Унарный минус допустим. 

# С помощью построенного дерева формулы упростить формулу, заменяя в ней все
# поддеревья, соответствующие формулам (f1*f3±f2*f3) и (f1*f2±f1*f3) на
# поддеревья, соответствующие формулам ((f1±f2)*f3) и (f1*(f2±f3)).

from os import system
system("clear") 

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.left is None and self.right is None:
            return str(self.value)
        return f"({self.left} {self.value} {self.right})"

class Expression:
    def __init__(self) -> None:
        pass

    def tokenize(self, expression):
        tokens = []
        i = 0
        n = len(expression)
        
        while i < n:
            if expression[i] == ' ':
                i += 1
                continue
            
            if expression[i] in '+-*/()':
                tokens.append(expression[i])
                i += 1
            elif expression[i].isalpha():
                tokens.append(expression[i])
                i += 1
            elif expression[i].isdigit():
                num = ''
                while i < n and expression[i].isdigit():
                    num += expression[i]
                    i += 1
                tokens.append(num)
            else:
                raise ValueError(f"Неизвестный символ: {expression[i]}")
        
        return tokens

    def parse_add_sub(self, tokens):
        node = self.parse_mul_div(tokens)
        
        while tokens and tokens[0] in '+-':
            op = tokens.pop(0)
            node = Node(op, node, self.parse_mul_div(tokens))
        
        return node

    def parse_mul_div(self, tokens):
        node = self.parse_unary(tokens)
        
        while tokens and tokens[0] in '*/':
            op = tokens.pop(0)
            node = Node(op, node, self.parse_unary(tokens))
        
        return node

    def parse_unary(self, tokens):
        if tokens[0] == '-':
            tokens.pop(0)
            return Node('-', Node(0), self.parse_primary(tokens))
        return self.parse_primary(tokens)

    def parse_primary(self, tokens):
        token = tokens.pop(0)
        
        if token == '(':
            node = self.parse_add_sub(tokens)
            if tokens[0] != ')':
                raise ValueError("Ожидается закрывающая скобка")
            tokens.pop(0)
            return node
        
        return Node(token)

    def evaluate(self, node, variables=None):
        if variables is None:
            variables = {}
        
        if node.left is None and node.right is None:
            if isinstance(node.value, str) and node.value.isalpha():
                return variables.get(node.value, 0)
            return int(node.value)
        
        left_val = self.evaluate(node.left, variables)
        right_val = self.evaluate(node.right, variables)
        
        if node.value == '+':
            return left_val + right_val
        elif node.value == '-':
            return left_val - right_val
        elif node.value == '*':
            return left_val * right_val
        elif node.value == '/':
            return left_val / right_val
        elif node.value == 'u-':
            return -right_val

    def simplify(self, node):
        if node is None:
            return None
        
        node.left = self.simplify(node.left)
        node.right = self.simplify(node.right)
        
        # Паттерн: (f1*f3 ± f2*f3) -> (f1 ± f2)*f3
        if node.value in '+-' and isinstance(node.left, Node) and isinstance(node.right, Node):
            if node.left.value == '*' and node.right.value == '*':
                # Проверяем все возможные комбинации общих множителей
                if str(node.left.right) == str(node.right.right):
                    common = node.left.right
                    new_left = Node(node.value, node.left.left, node.right.left)
                    return Node('*', new_left, common)
                elif str(node.left.left) == str(node.right.right):
                    common = node.left.left
                    new_left = Node(node.value, node.left.right, node.right.left)
                    return Node('*', new_left, common)
                elif str(node.left.left) == str(node.right.left):
                    common = node.left.left
                    new_left = Node(node.value, node.left.right, node.right.right)
                    return Node('*', new_left, common)
                elif str(node.left.right) == str(node.right.left):
                    common = node.left.right
                    new_left = Node(node.value, node.left.left, node.right.right)
                    return Node('*', new_left, common)
        
        # Паттерн: (f1*f2 ± f1*f3) -> f1*(f2 ± f3)
        if node.value in '+-' and isinstance(node.left, Node) and isinstance(node.right, Node):
            if node.left.value == '*' and node.right.value == '*':
                if str(node.left.left) == str(node.right.left):
                    common = node.left.left
                    new_right = Node(node.value, node.left.right, node.right.right)
                    return Node('*', common, new_right)
                elif str(node.left.right) == str(node.right.right):
                    common = node.left.right
                    new_right = Node(node.value, node.left.left, node.right.left)
                    return Node('*', common, new_right)
        
        return node

    def run(self, expr):
        tokens = self.tokenize(expr)
        tree = self.parse_add_sub(tokens)
        print(f"Исходное выражение: {expr}")
        print(f"Дерево выражения: {tree}")

        
        simplified = self.simplify(tree)
        print(f"Упрощенное дерево: {simplified}\n")
        return simplified


new_exp = Expression()
new_exp.run("a*b + a*c")
new_exp.run("x*y - z*y")
new_exp.run("a*(b + c) - a*d")
new_exp.run("2*(x + 3) + 4*(x + 3)")