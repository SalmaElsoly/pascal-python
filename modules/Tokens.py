from enum import Enum

class Token_type(Enum):  # listing all tokens type
    And = 1
    Array = 2
    Begin = 3
    Case = 4
    Const = 5
    Div = 6
    Do = 7
    Downto = 8
    Else = 9
    End = 10
    File = 11
    For = 12
    Function = 13
    Goto = 14
    If = 15
    In = 16
    Label = 17
    Mod = 18
    Nil = 19
    Not = 20
    Of = 21
    Or = 22
    Packed = 23
    Procedure = 24
    Program = 25
    Record = 26
    Repeat = 27
    Set = 28
    Then = 29
    To = 30
    Type = 31
    Until = 32
    Var = 33
    While = 34
    With = 35
    Semicolon = 36
    EqualOp = 37
    LessThanOp = 38
    GreaterThanOp = 39
    NotEqualOp = 40
    GreaterThanOrEqualOp = 41
    SmallerThanOrEqualOp = 42
    PlusOp = 43
    MinusOp = 44
    MultiplyOp = 45
    DivideOp = 46
    Identifier = 47
    Constant = 48
    Comma = 49
    String = 50
    OpenParenthesis = 51
    CloseParenthesis = 52
    AssignmentOperator = 53
    Dot = 54
    Colon = 55
    Error = 100
    Uses = 101
    Boolean=102
    Real=103
    Integer=104
    Char=105
    Read=106
    ReadLn=107
    Write=108
    WriteLn=109
    Xor=110



# Reserved word Dictionary
ReservedWords = {
    "if": Token_type.If,
    "downto": Token_type.Downto,
    "function": Token_type.Function,
    "mod": Token_type.Mod,
    "packed": Token_type.Packed,
    "set": Token_type.Set,
    "var": Token_type.Var,
    "case": Token_type.Case,
    "goto": Token_type.Goto,
    "nil": Token_type.Nil,
    "procedure": Token_type.Procedure,
    "then": Token_type.Then,
    "while": Token_type.While,
    "const": Token_type.Const,
    "not": Token_type.Not,
    "program": Token_type.Program,
    "to": Token_type.To,
    "with": Token_type.With,
    "end": Token_type.End,
    "begin": Token_type.Begin,
    "do": Token_type.Do,
    "else": Token_type.Else,
    "and": Token_type.And,
    "div": Token_type.Div,
    "file": Token_type.File,
    "of": Token_type.Of,
    "in": Token_type.In,
    "record": Token_type.Record,
    "type": Token_type.Type,
    "array": Token_type.Array,
    "label": Token_type.Label,
    "or": Token_type.Or,
    "repeat": Token_type.Repeat,
    "until": Token_type.Until,
    "for": Token_type.For,
    "uses": Token_type.Uses,
    "boolean":Token_type.Boolean,
    "string":Token_type.String,
    "real" : Token_type.Real,
    "integer":Token_type.Integer,
    "read" : Token_type.Read,
    "readln" :Token_type.ReadLn,
    "write" :Token_type.Write,
    "writeln":Token_type.WriteLn,
    "xor":Token_type.Xor

}

Operators = {
    # Arithmetic
    "+": Token_type.PlusOp,
    "-": Token_type.MinusOp,
    "*": Token_type.MultiplyOp,
    "/": Token_type.DivideOp,
    # Relational
    "=": Token_type.EqualOp,
    "<": Token_type.LessThanOp,
    ">": Token_type.GreaterThanOp,
    ">=": Token_type.GreaterThanOrEqualOp,
    "<=": Token_type.SmallerThanOrEqualOp,
    "<>":Token_type.NotEqualOp,
    # Parenthesis
    "(": Token_type.OpenParenthesis,
    ")": Token_type.CloseParenthesis,
    # Assignment
    ":=": Token_type.AssignmentOperator,
    # General
    ";": Token_type.Semicolon,
    ",": Token_type.Comma,
    ":": Token_type.Colon,
}
