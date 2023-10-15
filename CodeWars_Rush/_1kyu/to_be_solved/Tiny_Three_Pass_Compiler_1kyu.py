import ast
import re


class Compiler(object):

    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))                            # 36.6 98

    @staticmethod
    def tokenize(program):
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]

    def pass1(self, program) -> ast.AST:
        """Returns an un-optimized AST"""
        tokens = self.tokenize(program)
        print(f'tokens: {tokens}')
        ast_ = ast.parse(...)
        return ast_

    def pass2(self, ast_: ast):
        """Returns an AST with constant expressions reduced"""
        ...

    def pass3(self, ast_: ast):
        """Returns assembly instructions"""
        ...


s = f'[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)'  # s_ = f'x*y + 3'
c = Compiler()
print(f'compilation res: {c.compile(s)}')
