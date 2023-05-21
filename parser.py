
#todo Package grammar what type will be package because identifier is noot correct , uses token type,
#todo type is a datatype for example in pdf, tokentype of string , tokentype Integer , real,char in function datatype

import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *
from modules.Lexer import *



# class token to hold string and token type

errors = None
Tokens=[]
def find_token(text):
    lex=Lexer(text)
    lexemes,errors=lex.make_tokens()
    global Tokens
    Tokens=lexemes

def Parse():
    pos = 0
    Children = []
    Header_dict = Header(pos)
    Children.append(Header_dict["node"])
    Decl_Section = DeclSection(Header_dict["index"])
    Children.append(Decl_Section["node"])
    # block_main = MainBlock(Decl_Section["index"])
    # Children.append(block_main["node"])
    Node = Tree('Program', Children) # given non-terminal and its children
    return Node

def Header(pos):
    children = []
    out = dict()
    out_PID = ProgramID(pos)
    children.append(out_PID["node"])
    out_Uses = Uses(out_PID["index"])
    children.append(out_Uses["node"])
    node = Tree("header", children)
    out["node"] = node
    out["index"] = out_Uses["index"]
    return out
    # pass

def ProgramID(pos):
    children=[]
    out=dict()
    out_program=Match(Token_type.Program,pos)
    children.append(out_program["node"])
    out_id = Match(Token_type.Identifier, out_program["index"])
    children.append(out_id["node"])
    out_semi = Match(Token_type.Semicolon, out_id["index"])
    children.append(out_semi["node"])
    node = Tree("ProgramID", children)
    out["node"] = node
    out["index"] = out_semi["index"]
    return out

def Uses(pos):

    out=dict()
    children=[]
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Uses:
            out_uses = Match(Token_type.Uses, pos)
            children.append(out_uses["node"])
            out_packagelist = PackageList(out_uses["index"])
            children.append(out_packagelist["node"])
            out_semicolon= Match(Token_type.Semicolon,out_packagelist["index"])
            children.append(out_semicolon["node"])
            node = Tree("Uses", children)
            out["node"] = node
            out["index"] = out_semicolon["index"]
            pos= out["index"]
            return out
        else:
            out["node"] = ["Epsilon"]
            out["index"] = pos
            return out
    else:
        out["node"] = ["Epsilon"]
        out["index"] = pos
        return out

def PackageList(pos):
    children = []
    out = dict()
    out_package= Match(Token_type.Identifier, pos)
    children.append(out_package["node"])
    out_packagelistAST = PackageList2(out_package["index"])
    children.append(out_packagelistAST["node"])
    node = Tree("PackageList", children)
    out["node"] = node
    out["index"] = out_packagelistAST["index"]
    return out

def PackageList2(pos):
    temp = Tokens[pos].to_dict()
    out = dict()
    children = []
    if temp["token_type"] == Token_type.Comma:
        out_comma = Match(Token_type.Comma, pos)
        children.append(out_comma["node"])
        out_package = Match(Token_type.Identifier, out_comma["index"])
        children.append(out_package["node"])
        out_packagelist2 = PackageList2(out_package["index"])
        children.append(out_packagelist2["node"])
        node = Tree("PackageList2", children)
        out["node"] = node
        out["index"] = out_packagelist2["index"]
        pos=out["index"]
        return out
    else:
        out["node"]=["Epsilon"]
        out["index"]=pos
        return out

def DeclSection(pos):
    children = []
    out = dict()
    out_decl = Declarations(pos)
    children.append(out_decl["node"])
    node = Tree("Declaration Section", children)
    out["node"] = node
    out["index"] = out_decl["index"]
    return out

def Declarations (pos):
    children = []
    out = dict()
    if(pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if (temp["token_type"]==Token_type.Var or temp["token_type"]==Token_type.Const or temp["token_type"]==Token_type.Type ):
            out_option = DeclarationOptions(pos)
            children.append(out_option["node"])
            out_Declaration= Declarations(out_option["index"])
            children.append(out_Declaration["node"])
            node = Tree("Declarations ", children)
            out["node"] = node
            out["index"] = out_Declaration["index"]
    else :
        out["node"] = ["Epsilon"]
        children.append(out["node"])
        out["index"] = pos
        node = Tree("Declarations", children)
        # out["node"] = ["Epsilon"]
        # out["index"] = pos
    return out


def DeclarationOptions(pos):
    children=[]
    out = dict()
    temp=Tokens[pos].to_dict()
    if temp["token_type"] == Token_type.Var:
        out_var=VarDeclarationSection(pos)
        children.append(out_var["node"])
        node = Tree("Declaration Options", children)
        out["node"] = node
        out["index"] = out_var["index"]
    if temp["token_type"] == Token_type.Type:
        out_type=TypeDeclaration(pos)
        children.append(out_type["node"])
        node = Tree("Declaration Options", children)
        out["node"] = node
        out["index"] = out_type["index"]
    if temp["token_type"] == Token_type.Const:
        out_const=ConstDeclarationSection(pos)
        children.append(out_const["node"])
        node = Tree ("Declaration Options", children)
        out["node"]=node
        out["index"]=out_const["index"]
    return out

# def ProcedureDeclarationSection(pos):
#     temp = Tokens[pos].to_dict()
#     out = dict()
#     children = []
#
#     if temp["token_type"] == Token_type.Function or temp["token_type"] == Token_type.Procedure:
#         out_VarDecl = VarDeclaration(pos)
#         out_AAST = FPDec2(pos)
#         children.append(out_AAST["node"])
#         out_ProcDecAST = ProcedureDeclarationSection2(out_AAST["index"])
#         children.append(out_ProcDecAST["node"])
#         node = Tree("ProcedureDeclarationSection", children)
#         out["node"] = node
#         out["index"] = out_ProcDecAST["index"]
#         return out
#     else:
#         out["node"] = ["Epsilon"]
#         out["index"] = pos
#         return out

# def ProcedureDeclarationSection2(pos):
#     temp = Tokens[pos].to_dict()
#     out = dict()
#     children = []
#     if temp["token_type"] == Token_type.Function:
#         out_funcReserved= Match(Token_type.Function,pos)
#         children.append(out_funcReserved["node"])
#         out_function = FunctionDecS(out_funcReserved["index"])
#         children.append(out_function["node"])
#         out_p = ProcedureDeclarationSection2(out_function["index"])
#         children.append(out_function["node"])
#         node = Tree("ProcedureDeclarationSection2", children)
#         out["node"] = node
#         out["index"] = out_function["index"]
#         return out
#     else:
#         out_procedure = ProcedureDecS(pos)
#         children.append(out_procedure["node"])
#         out_p = ProcedureDeclarationSection2(out_procedure["index"])
#         children.append(out_procedure["node"])
#         node = Tree("ProcedureDeclarationSection2", children)
#         out["node"] = node
#         out["index"] = out_procedure["index"]
#         return out

# def FPDec2(pos):
#     temp = Tokens[pos].to_dict()
#     out = dict()
#     children = []
#     out_function = FunctionDecS(pos)
#     children.append(out_function["node"])
#     node = Tree("FPDec2", children)
#     out["node"] = node
#     out["index"] = out_function["index"]
#     return out
#
#     out_procedure = ProcedureDecS(pos)
#     children.append(out_procedure["node"])
#     node = Tree("FPDec2", children)
#     out["node"] = node
#     out["index"] = out_procedure["index"]
#     return out

# def ProcedureDecS(pos):
#     children = []
#     out = dict()
#     out_PH = ProcedureHeader(pos)
#     children.append(out_PH["node"])
#     out_FP = FPDecl(out_PH["index"])
#     children.append(out_FP["node"])
#     out_PB = ProcedureBlock(out_FP["index"])
#     children.append(out_PB["node"])
#     node = Tree("ProcedureDecS", children)
#     out["node"] = node
#     out["index"] = out_PB["index"]
#     return out
#def ProcedureHeader(pos):
#def ProcedureBlock(pos):

# def FunctionDecS(pos):
#     children = []
#     out = dict()
#     out_FuncH = FunctionHeader(pos)
#     children.append(out_FuncH["node"])
#     out_FPDecl = FPDecl(out_FuncH["index"])
#     children.append(out_FPDecl["node"])
#     out_FuncBl = FunctionBlock(out_FPDecl["index"])
#     children.append(out_FuncBl["node"])
#     node = Tree("FunctionDecs", children)
#     out["node"] = node
#     out["index"] =out_FuncBl["index"]
#     return out

def FunctionHeader(pos):
    children = []
    out = dict()
    out_function = Match(Token_type.Function, pos)
    children.append(out_function["node"])
    out_FunctionName = FunctionName(out_function["index"])
    children.append(out_FunctionName["node"])
    out_bracket = Match(Token_type.OpenParenthesis , out_FunctionName["index"])
    children.append(out_bracket["node"])
    out_ArgIdList = ArgumentsIdList(out_bracket["index"])
    children.append(out_ArgIdList["node"])
    out_bracket2 = Match(Token_type.CloseParenthesis, out_ArgIdList["index"])
    children.append(out_bracket2["node"])
    out_colon = Match(Token_type.Colon, out_bracket2["index"])
    children.append(out_colon["node"])
    out_dataType1 = DataType(out_colon["index"])
    children.append(out_dataType1["node"])
    out_semicolon = Match(Token_type.Semicolon, out_dataType1["index"])
    children.append(out_semicolon["node"])
    node = Tree("FunctionHeader", children)
    out["node"] = node
    out["index"] =out_semicolon["index"]
    return out

def FunctionName(pos):
    children = []
    out = dict()
    out_iden = Match(Token_type.Identifier , pos)
    children.append(out_iden["node"])
    node = Tree("FunctionName", children)
    out["node"] = node
    out["index"] = out_iden["index"]
    return out
def FPDecl(pos):
    children = []
    out = dict()
    out_VarDec = VarDeclarationSection (pos)
    children.append(out_VarDec["node"])
    node = Tree("FPDecl", children)
    out["node"] = node
    out["index"] =  out_VarDec["index"]
    return out
def FunctionBlock( pos):
    children = []
    out = dict()
    out_begin = Match(Token_type.Begin, pos)
    children.append(out_begin["node"])
    out_FuncStat= FunctionStatments(out_begin["index"])
    children.append(out_FuncStat["node"])
    out_end = Match(Token_type.End, out_FuncStat["index"])
    children.append(out_end["node"])
    out_semicolon = Match(Token_type.Semicolon, out_end["index"])
    children.append(out_semicolon["node"])
    node = Tree("FunctionBlock", children)
    out["node"] = node
    out["index"] = out_semicolon["index"]
    return out

# def ArgumentsIdList(pos):
#     children = []
#     out = dict()
#     out_option = Option(pos)
#     children.append(out_option["node"])
#     out_paramlist=ParametersList(out_option["index"])
#     children.append(out_paramlist["node"])
#     out_colon = Match(Token_type.Colon, out_paramlist["index"])
#     children.append(out_colon["node"])
#     out_dataType1 = DataType(out_colon["index"])
#     children.append(out_dataType1["node"])
#     out_defValue = DefaultValue(out_dataType1["index"])
#     children.append(out_defValue["node"])


#VarDecls       → var VarDecl  |var VarDecl | ε
#VarDecl        →  VarIdList : Datatype; VarDecl | ε


def VarDeclarationSection (pos):
    print("VarDeclarationSection pos:",pos)
    temp = Tokens[pos].to_dict()
    print("VarDeclarationSection lex:",temp["Lex"])
    children = []
    out = dict()
    if temp["token_type"]==Token_type.Var:
        out_var=Match(Token_type.Var,pos)
        children.append(out_var["node"])
        out_variable_declaration = VarDeclaration(out_var["index"])
        children.append(out_variable_declaration["node"])
        node = Tree("VarDeclarationSection", children)
        out["node"] = node
        out["index"] = out_variable_declaration["index"]

    else:
        out["node"] = ["Epsilon"]
        children.append(out["node"])
        node = Tree("VarDeclarationSection", children)
        out["index"] = pos
    return out


def VarDeclaration (pos):
    out = dict()
    children = []
    out_id = VariableIDList(pos)
    children.append(out_id["node"])
    out_colon = Match(Token_type.Colon, out_id["index"])
    children.append(out_colon["node"])
    out_datatype = DataType(out_colon["index"])
    children.append(out_datatype["node"])
    out_semi = Match(Token_type.Semicolon, out_datatype["index"])
    children.append(out_semi["node"])
    print("ablooooooooo")
    print("semi index:",out_semi["index"])
    out_var2=VarDeclaration2(out_semi["index"])
    print("out varDec2 nodee: ", out_var2["node"])
    #if (out_var2["node"]!=["Epsilon"]):
    children.append(out_var2["node"])
    node = Tree("VarDeclaration", children)
    out["node"] = node
    out["index"] = out_var2["index"]
   # else :
    #    out["node"] = ["Epsilon"]
     #   out["index"] = out_semi["index"]
    return out

#todo :  lzm main block yb2a mmwgod w ila error message lzm tzhar


def VarDeclaration2(pos):
    out = dict()
    children = []
    print ("VarDEC222 : ",len(Tokens),pos)
    if(pos<len(Tokens)):
        print("Entereddd")
        temp = Tokens[pos].to_dict()
        print("Token VD2:",temp["Lex"])
        if temp["token_type"]==Token_type.Identifier:
            out_ID=Match(Token_type.Identifier,pos)
            children.append(out_ID["node"])
            out_var = VarDeclaration(pos)
            children.append(out_var["node"])
            node = Tree("VarDeclaration2", children)
            out["node"] = node
            out["index"] = out_var["index"]
        # else:
        #     out["node"] = ["Error"]
        #     out["index"] = pos
        else:
            out["node"] = ["Epsilon"]
            out["index"] = pos
            children.append(out["node"])
            node = Tree("VarDeclaration2", children)
    else:
        out["node"] = ["Epsilon"]
        out["index"] = pos
        children.append(out["node"])
        node = Tree("VarDeclaration2", children)
    return out

def VariableIDList (pos):
    temp = Tokens[pos].to_dict()
    children = []
    out = dict()
    print("VariableIDList",pos,temp["Lex"])
    out_identifier = Match(Token_type.Identifier, pos)
    children.append(out_identifier["node"])
    out_VariableIDList2  = VariableIDList2(out_identifier["index"])
    children.append(out_VariableIDList2["node"])
    node = Tree("VariableIDList", children)
    out["node"] = node
    out["index"] = out_VariableIDList2["index"]
    return out

def VariableIDList2 (pos):
    temp = Tokens[pos].to_dict()
    out = dict()
    children = []
    print("VariableIDList2 pos",pos,temp["Lex"])
    if temp["token_type"] == Token_type.Comma:
        out_comma=Match(Token_type.Comma,pos)
        children.append(out_comma["node"])
        out_id = Match(Token_type.Identifier,out_comma["index"])
        children.append(out_id["node"])
        out_VariableIdList2 = VariableIDList2(out_id["index"])
        children.append(out_VariableIdList2["node"])
        node = Tree("VarDeclarationIDList2", children)
        out["node"] = node
        out["index"] = out_VariableIdList2["index"]
        return out
    else:
        out["node"] = ["Epsilon"]
        out["index"] = pos
        children.append(out["node"])
        node = Tree("VarDeclarationIDList2", children)
        return out


def TypeDeclaration(pos):
    children=[]
    out=dict()
    out_type=Match(Token_type.Type,pos)
    children.append(out_type["node"])
    out_identifier=Match(Token_type.Identifier,out_type["index"])
    children.append(out_identifier["node"])
    out_equal=Match(Token_type.EqualOp,out_identifier["index"])
    children.append(out_equal["node"])
    out_datatype=DataType(out_equal["index"])
    children.append(out_datatype["node"])
    out_semicolon = Match(Token_type.Semicolon, out_datatype["index"])
    children.append(out_semicolon["node"])
    node = Tree("TypeDeclaration", children)
    out["node"] = node
    out["index"] = out_semicolon["index"]
    pos=out["index"]
    return out


def ConstDeclarationSection(pos):
    out = dict()
    children = []
    if (pos < len (Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Const:
            out = dict()
            out_const = Match(Token_type.Const, pos)
            children.append(out_const["node"])
            out_ConstID = ConstID(out_const["index"])
            children.append(out_ConstID["node"])
            node = Tree("ConstDeclarationSection", children)
            out["node"] = node
            out["index"] = out_ConstID["index"]
    else:
        out["node"] = ["Epsilon"]
        children.append(out["node"])
        node = Tree("ConstDeclarationSection", children)
        out["index"] = pos
    return out
def ConstID(pos):
    children = []
    out = dict()
    out_ID=Match(Token_type.Identifier,pos)
    children.append(out_ID["node"])
    out_Eq=Match(Token_type.EqualOp,out_ID["index"])
    children.append(out_Eq["node"])
    out_Constant=Constant(out_Eq["index"])
    children.append(out_Constant["node"])
    out_semi=Match(Token_type.Semicolon,out_Constant["index"])
    children.append(out_semi["node"])
    out_ConstId2=ConstID2(out_semi["index"])
    children.append(out_ConstId2["node"])
    node = Tree("ConstID", children)
    out["node"] = node
    out["index"] = out_ConstId2["index"]
    return out

def Constant(pos):
    temp = Tokens[pos].to_dict()
    out = dict()
    children = []
    if temp["token_type"] == Token_type.Constant:
        out = dict()
        out_const = Match(Token_type.Constant, pos)
        children.append(out_const["node"])
        node = Tree("Constant", children)
        out["node"] = node
        out["index"] = out_const["index"]
        return out
    elif temp["token_type"] == Token_type.Boolean:
        out = dict()
        out_bool = Match(Token_type.Boolean, pos)
        children.append(out_bool["node"])
        node = Tree("Constant", children)
        out["node"] = node
        out["index"] = out_bool["index"]
        pos = out["index"]
        return out
    else:
        out = dict()
        out_string = Match(Token_type.String, pos)
        children.append(out_string["node"])
        node = Tree("Constant", children)
        out["node"] = node
        out["index"] = out_string["index"]
        return out

def ConstID2(pos):

    out = dict()
    children = []
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Identifier:
            out_id = Match(Token_type.Identifier, pos)
            children.append(out_id["node"])
            out_equals = Match(Token_type.EqualOp,out_id["index"])
            children.append(out_equals["node"])
            out_ConstID = Constant(out_equals["index"])
            children.append(out_ConstID["node"])
            out_semi = Match(Token_type.Semicolon, out_ConstID["index"])
            children.append(out_semi["node"])
            out_ConstID = ConstID2(out_semi["index"])
            children.append(out_ConstID["node"])
            node = Tree("ConstID2", children)
            out["node"] = node
            out["index"] = out_ConstID["index"]
            return out
        else:
            out["node"] = ["Epsilon"]
            children.append(out["node"])
            node = Tree("ConstID2", children)
            out["index"] = pos
            return out
#todo : dh kda kda lzm hyt4al 34n mynf3sh el code y accept declsection bs mn 8er b2et el amin block program fa dh just for testing
    else:
        out["node"] = ["Epsilon"]
        children.append(out["node"])
        node = Tree("ConstID2", children)
        out["index"] = pos
        return out

def DataType(pos):
    temp = Tokens[pos].to_dict()
    out = dict()
    children=[]
    if temp["token_type"] == Token_type.Integer:
        out_integer = Match(Token_type.Integer, pos)
        children.append(out_integer["node"])
        node = Tree("DataType", children)
        out["node"] = node
        out["index"] = out_integer["index"]


    elif temp["token_type"] == Token_type.Real:
        out_real = Match(Token_type.Real, pos)
        children.append(out_real["node"])
        node = Tree("DataType", children)
        out["node"] = node
        out["index"] = out_real["index"]

    elif temp["token_type"] == Token_type.Char:
        out_char = Match(Token_type.Char, pos)
        children.append(out_char["node"])
        node = Tree("DataType", children)
        out["node"] = node
        out["index"] = out_char["index"]


    elif temp["token_type"] == Token_type.String:
        out_string = Match(Token_type.String, pos)
        children.append(out_string["node"])
        node = Tree("DataType", children)
        out["node"] = node
        out["index"] = out_string["index"]


    elif temp["token_type"] == Token_type.Boolean:
        out_bool = Match(Token_type.Boolean, pos)
        children.append(out_bool["node"])
        node = Tree("DataType", children)
        out["node"] = node
        out["index"] = out_bool["index"]


    return out
# def FunctionStatments(pos):
#     out=dict()
#     children=[]
#     out_functionstatment= FunctionStatment(pos)
#     children.append(out_functionstatment["node"])
#     out_functionstatmentsAST=FunctionStatments2(out_functionstatment["index"])
#     children.append(out_functionstatmentAST["node"])
#     node = Tree("FunctionStatments",children)
#     out["node"] = node
#     out["index"] = out_FunctionStatmentsAST["index"]
#     return out

# def FunctionStatments2(pos):
#     temp = Tokens[pos].to_dict()
#     out = dict()
#     children = []
#     if temp["token_type"] == Token_type.Semicolon:
#         out_semicolon = Match(Token_type.Semicolon, pos)
#         children.append(out_semicolon["node"])
#         out_FunctionStatment = FunctionStatment(out_semicolon["index"])
#         children.append( out_FunctionStatment["node"])
#         out_FunctionStatmentsAST = FunctionStatments2(out_FunctionStatment["index"])
#         children.append(out_FunctionStatmentsAST["node"])
#         node = Tree("FunctionStatments2", children)
#         out["node"] = node
#         out["index"] = out_FunctionStatmentsAST["index"]
#         pos = out["index"]
#         return out
#     else:
        # out["node"] = ["Epsilon"]
        # out["index"] = pos
        # return out

# def FunctionStatment(pos):

def Match(a, pos):  # given token type and index and give dict(node,key)
    output = dict()
    if (pos < len(Tokens)):  # to prevent out of range
        Temp = Tokens[pos].to_dict()
        if(Temp['token_type'] == a):
            pos += 1
            output["node"] = [Temp['Lex']]
            output["index"] = pos
            return output
        else:
            output["node"] = ["error"]
            output["index"] = pos + 1
            #errors.append("Syntax error : " + Temp['Lex'] + " Expected dot")
            return output
    else:
        output["node"] = ["error"]
        output["index"] = pos + 1
        return output

# GUI
root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Scanner Phase')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def Scan():

    x1 = entry1.get()
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    # print(df)

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node = Parse()

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()
    # clear your list

    # label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    # canvas1.create_window(200, 210, window=label3)

    # label4 = tk.Label(root, text="Token_type"+x1, font=('helvetica', 10, 'bold'))
    # canvas1.create_window(200, 230, window=label4)


button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)
root.mainloop()

"""### """





