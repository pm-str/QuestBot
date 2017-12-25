import operator

from pyparsing import (
    CaselessLiteral,
    Combine,
    Forward,
    Group,
    Literal,
    Optional,
    Word,
    ZeroOrMore,
    alphas,
    nums,
    oneOf,
)


class NumericStringParser(object):
    """Most of this code comes from the fourFn.py pyparsing example"""

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        """
        point = Literal(".")
        e = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(e + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (
                     ident + lpar + expr + rpar | fnumber).setParseAction(
                     self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)
        factor = Forward()
        factor << atom + \
                  ZeroOrMore((expop + factor).setParseAction(self.pushFirst))
        term = factor + \
               ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + \
                ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        self.bnf = expr
        self.opn = {
            "+": operator.add,
            "*": operator.mul,
            "-": operator.sub,
            "/": operator.truediv,
        }
        self.fn = {
            "!": (lambda x: not x),
            "abs": abs,
        }

    def evaluateStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op in "+*-/":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def eval(self, num_string, parseAll=True):
        self.exprStack = []
        results = self.bnf.parseString(num_string, parseAll)
        val = self.evaluateStack(self.exprStack[:])
        return val
