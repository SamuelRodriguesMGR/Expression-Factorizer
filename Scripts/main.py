
# Написать программу, которая по заданной формуле строит дерево и
# производит вычисления с помощью построенного дерева. 
# Формула задана в традиционной инфиксной записи, в ней могут быть скобки, максимальная
# степень вложенности которых ограничивается числом 10. 

# Аргументами могут быть целые числа и переменные, задаваемые однобуквенными именами.
# Допустимые операции: +, -, *, /. Унарный минус допустим. 

# С помощью построенного дерева формулы упростить формулу, заменяя в ней все
# поддеревья, соответствующие формулам (f1*f3±f2*f3) и (f1*f2±f1*f3) на
# поддеревья, соответствующие формулам ((f1±f2)*f3) и (f1*(f2±f3)).

import os
os.system("clear") 

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value  
        self.left = left    
        self.right = right
    
    def __str__(self):
        """Строковое представление узла и его потомков"""
        if self.left is None and self.right is None:
            return str(self.value)
        return f"({self.left} {self.value} {self.right})"

class Expression:
    def __init__(self) -> None:
        pass

    def tokenize(self, expression):
        """Разбивает строку выражения на токены (числа, переменные, операторы, скобки)"""
        tokens = []
        i = 0
        n = len(expression)
        
        while i < n:
            if expression[i] == ' ':
                i += 1
                continue
            
            if expression[i] in '+-*/()': # мат выражения
                tokens.append(expression[i])
                i += 1
            elif expression[i].isalpha(): # буквы
                tokens.append(expression[i])
                i += 1
            elif expression[i].isdigit(): # числа
                num = ''
                while i < n and expression[i].isdigit():
                    num += expression[i]
                    i += 1
                tokens.append(num)
            else:
                raise ValueError(f"Неизвестный символ: {expression[i]}")
        
        return tokens

    def parse_add_sub(self, tokens):
        """Парсит операции сложения и вычитания"""
        node = self.parse_mul_div(tokens)
        
        while tokens and tokens[0] in '+-':
            op = tokens.pop(0)
            node = Node(op, node, self.parse_mul_div(tokens))
        
        return node

    def parse_mul_div(self, tokens):
        """Парсит операции умножения и деления"""
        node = self.parse_unary(tokens)
        
        while tokens and tokens[0] in '*/':
            op = tokens.pop(0)
            node = Node(op, node, self.parse_unary(tokens))
        
        return node

    def parse_unary(self, tokens):
        """Обрабатывает минус"""
        if tokens[0] == '-':
            tokens.pop(0)
            return Node('-', Node(0), self.parse_primary(tokens))
        return self.parse_primary(tokens)

    def parse_primary(self, tokens):
        """Обрабатывает числа, переменные и выражения в скобках"""
        token = tokens.pop(0)
        
        if token == '(':
            node = self.parse_add_sub(tokens)
            if not tokens or tokens[0] != ')':
                raise ValueError("Ожидается закрывающая скобка")
            tokens.pop(0)
            return node
        
        return Node(token)

    def simplify(self, node):
        """Упрощает выражение, применяя алгебраические преобразования"""
        if node is None:
            return None
        
        # Рекурсивно упрощаем поддеревья
        node.left = self.simplify(node.left)
        node.right = self.simplify(node.right)
        
        # Паттерн 1: (f1*f3 ± f2*f3) -> (f1 ± f2)*f3
        if node.value in '+-' and isinstance(node.left, Node) and isinstance(node.right, Node):
            if node.left.value == '*' and node.right.value == '*':
                # Проверяем 4 возможные комбинации общих множителей
                combinations = [
                    (node.left.right, node.right.right),  # f3 == f3
                    (node.left.left, node.right.right),   # f1 == f3
                    (node.left.left, node.right.left),    # f1 == f2
                    (node.left.right, node.right.left)    # f3 == f2
                ]
                
                for left_part, right_part in combinations:
                    if str(left_part) == str(right_part):
                        common = left_part
                        new_left = Node(node.value, 
                                       node.left.left if left_part == node.left.right else node.left.right,
                                       node.right.left if right_part == node.right.right else node.right.right)
                        return Node('*', new_left, common)
        
        # Паттерн 2: (f1*f2 ± f1*f3) -> f1*(f2 ± f3)
        if node.value in '+-' and isinstance(node.left, Node) and isinstance(node.right, Node):
            if node.left.value == '*' and node.right.value == '*':
                # Проверяем общие множители слева и справа
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
        """ Основной метод для обработки выражения """
        tokens = self.tokenize(expr)
        tree = self.parse_add_sub(tokens)
        print(f"Исходное выражение: {expr}")
        print(f"Дерево выражения: {tree}")

        simplified = self.simplify(tree)
        print(f"Упрощенное дерево: {simplified}\n")
        return simplified


if __name__ == "__main__":
    exp_processor = Expression()
    test_expressions = [
        "a*b + a*c",        
        "x*y - z*y",        
        "a*(b + c) - a*d",  
        "2*(x + 3) + 4*(x + 3)", 
        "a*b + c*d"        
    ]
    
    for expr in test_expressions:
        exp_processor.run(expr)