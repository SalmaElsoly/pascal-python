import pandas

from modules.Lexer import Lexer


def Scan():
    file = open("./code.pas", "r", encoding="utf-8")
    text = file.read()
    file.close()
    lex = Lexer(text)
    lexemes, error = lex.make_tokens()
    if error:
        print(error)
    else:
        df = pandas.DataFrame.from_records([t.to_dict() for t in lexemes])
        df.to_csv("output.csv")
        print(df)

Scan()
