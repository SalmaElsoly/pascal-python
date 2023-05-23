
#todo Package grammar what type will be package because identifier is not correct , uses token type,
#todo type is a datatype for example in pdf, tokentype of string , tokentype Integer , real,char in function datatype
#todo comments
#todo in option in procedure declaration var does not work
import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *
from modules.Lexer import *
from modules.Tokens import *

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
    #Header_dict = Header(pos)
    #Children.append(Header_dict["node"])
    #Decl_Section = DeclSection(pos)
    #Children.append(Decl_Section["node"])
    block_main = MainBlock(pos)
    Children.append(block_main["node"])
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

        else:
            children.append(["Epsilon"])
            node = Tree("Uses", children)
            out["node"] = node
            out["index"] = pos

    else:
        children.append(["Epsilon"])
        node = Tree("Uses", children)
        out["node"] = node
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
        children.append(["Epsilon"])
        node = Tree("PackageList2", children)
        out["node"] = node
        out["index"] = pos


def DeclSection(pos):
    children = []
    out = dict()
    #out_decl = Declarations(pos)
   # children.append(out_decl["node"])
    out_proc=ProcedureDeclarationSection(pos)
    children.append(out_proc["node"])
    node = Tree("Declaration Section", children)
    out["node"] = node
    out["index"] = out_proc["index"]
    return out
def ProcedureDeclarationSection(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"]==Token_type.Function or temp["token_type"]==Token_type.Procedure:
            out_FP=FunctionOrProcedure(pos)
            children.append(out_FP["node"])
            out_Proc2=ProcedureDeclarationSection2(out_FP["index"])
            children.append(out_Proc2["node"])
            node = Tree("ProcedureDeclarationSection", children)
            out["node"]=node
            out["index"]=out_Proc2["index"]
        #todo here will be the declaration of the error instead of Epsilon
        else:
            children.append(["Epsilon"])
            node = Tree("ProcedureDeclarationSection", children)
            out["node"] = node
            out["index"] = pos
    else:
        children.append(["Epsilon"])
        node = Tree("ProcedureDeclarationSection", children)
        out["node"] = node
        out["index"] = pos
    return out

def FunctionOrProcedure(pos): #Function/Procedure
    children = []
    out = dict()

    temp = Tokens[pos].to_dict()
    if temp["token_type"]==Token_type.Procedure:
        out_ProcDecS=ProcedureDec(pos)
        children.append(out_ProcDecS["node"])
        node = Tree("FP", children)
        out["node"] = node
        out["index"] = out_ProcDecS["index"]

    elif temp["token_type"]==Token_type.Function:
        out_Function_Decleration = FunctionDeclarationSection(pos)
        children.append(out_Function_Decleration["node"])
        node = Tree("FP", children)
        out["node"] = node
        out["index"] = out_Function_Decleration["index"]
    # todo : error to be implemented here
    else:
        children.append(["Epsilon"])
        node = Tree("FunctionOrProcedure", children)
        out["node"] = node
        out["index"] = pos
    return out
def ProcedureDec(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        out_PH=ProcedureHeader(pos)
        children.append(out_PH["node"])
        out_var = VarDeclarationSection(out_PH["index"])
        children.append(out_var["node"])
        out_PB=ProcedureBlock(out_var["index"])
        children.append(out_PB["node"])
        node = Tree("ProcedureDec", children)
        out["node"]=node
        out["index"]=out_PB["index"]

    return out
def ProcedureBlock(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Begin:
            out_begin=Match(Token_type.Begin,pos)
            children.append(out_begin["node"])
            out_statement= Statements(out_begin["index"])
            children.append(out_statement["node"])
            out_end=Match(Token_type.End,out_statement["index"])
            children.append(out_end["node"])
            out_semi=Match(Token_type.Semicolon,out_end["index"])
            children.append(out_semi["node"])
            node = Tree("ProcedureBlock", children)
            out["node"] = node
            out["index"] = out_semi["index"]

    return out

def ProcedureHeader(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Procedure:
            out_p = Match(Token_type.Procedure, pos)
            children.append(out_p["node"])
            out_Name = ProcedureName(out_p["index"])
            children.append(out_Name["node"])
            out_ArgOption=ArgumentOption(out_Name["index"])
            children.append(out_ArgOption["node"])
            out_semi=Match(Token_type.Semicolon,out_ArgOption["index"])
            children.append(out_semi["node"])
            node = Tree("ProcedureHeader", children)
            out["node"] = node
            out["index"] = out_semi["index"]
    return out
def ArgumentIDList(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        out_option=OptionArg(pos)
        children.append(out_option["node"])
        out_PL=ParametersList(out_option["index"])
        children.append(out_PL["node"])
        out_Colon = Match(Token_type.Colon,out_PL["index"])
        children.append(out_Colon["node"])
        out_DataType=DataType(out_Colon["index"])
        children.append(out_DataType["node"])
        out_def=DefaultValue(out_DataType["index"])
        children.append(out_def["node"])
        out_argsEnd=ArgsEnd(out_def["index"])
        children.append(out_argsEnd["node"])
        node = Tree("ArgumentIDList", children)
        out["node"] = node
        out["index"] = out_argsEnd["index"]
    return out
def ArgsEnd(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Semicolon:
            out_semi=Match(Token_type.Semicolon,pos)
            children.append(out_semi["node"])
            out_args = ArgumentIDList(out_semi["index"])
            children.append(out_args["node"])
            node = Tree("ArgumentIDList", children)
            out["node"] = node
            out["index"] = out_args["index"]
        else:
            children.append(["Epsilon"])
            node = Tree("ArgsEnd", children)
            out["node"] = node
            out["index"] = pos
    else:
        children.append(["Epsilon"])
        node = Tree("ArgsEnd", children)
        out["node"] = node
        out["index"] = pos
    return out

def DefaultValue(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.EqualOp:
            out_eq = Match(Token_type.EqualOp, pos)
            children.append(out_eq["node"])
            out_const = Match(Token_type.Constant,out_eq["index"])
            children.append(out_const["node"])
            node = Tree("DefaultValue", children)
            out["node"] = node
            out["index"] = out_const["index"]
        else:
            children.append(["Epsilon"])
            node = Tree("DefaultValue", children)
            out["node"] = node
            out["index"] = pos

    else:
        children.append(["Epsilon"])
        node = Tree("DefaultValue", children)
        out["node"] = node
        out["index"] = pos
    return out

def ParametersList(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Identifier:
            out_id=Match(Token_type.Identifier,pos)
            children.append(out_id["node"])
            out_PL2=ParametersList2(out_id["index"])
            children.append(out_PL2["node"])
            node = Tree("ParametersList", children)
            out["node"] = node
            out["index"] = out_PL2["index"]
        elif temp["token_type"] == Token_type.Constant :
            out_Const = Match(Token_type.Constant, pos)
            children.append(out_Const["node"])
            out_PL2 = ParametersList2(out_Const["index"])
            children.append(out_PL2["node"])
            node = Tree("ParametersList", children)
            out["node"] = node
            out["index"] = out_PL2["index"]

    return out
def ParametersList2(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Comma:
            out_Comma = Match(Token_type.Comma, pos)
            children.append(out_Comma["node"])
            out_PL=ParametersList(out_Comma["index"])
            children.append(out_PL["node"])
            node = Tree("ParametersList2", children)
            out["node"] = node
            out["index"] = out_PL["index"]
        else:
            children.append(["Epsilon"])
            node = Tree("ParametersList2", children)
            out["node"] = node
            out["index"] = pos
    else:
        children.append(["Epsilon"])
        node = Tree("ParametersList2", children)
        out["node"] = node
        out["index"] = pos
    return out


def OptionArg(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Const:
            out_const = Match(Token_type.Const,pos)
            children.append(out_const["node"])
            node = Tree("OptionArg", children)
            out["node"] = node
            out["index"] = out_const["index"]
        elif temp["token_type"] == Token_type.Var:
            out_var = Match(Token_type.Var,pos)
            children.append(out_var["node"])
            node = Tree("OptionArg", children)
            out["node"] = node
            out["index"] = out_var["index"]
        else:
            children.append(["Epsilon"])
            node = Tree("OptionArg", children)
            out["node"] = node
            out["index"] = pos

    else:
        children.append(["Epsilon"])
        node = Tree("OptionArg", children)
        out["node"] = node
        out["index"] = pos
    return out

def ProcedureName(pos):
    children = []
    out = dict()
    temp = Tokens[pos].to_dict()
    out_id=Match(Token_type.Identifier,pos)
    children.append(out_id["node"])
    node = Tree("ProcedureName", children)
    out["node"]=node
    out["index"]=out_id["index"]
    return out


def ProcedureDeclarationSection2(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"]==Token_type.Procedure:
            out_pd=ProcedureDec(pos)
            children.append(out_pd["node"])
            out_pd2=ProcedureDeclarationSection2(out_pd["index"])
            children.append(out_pd2["node"])
            node = Tree("ProcedureDeclarationSection2", children)
            out["node"] = node
            out["index"] = out_pd2["index"]
        elif temp["token_type"]==Token_type.Function:
            out_fd = FunctionDeclarationSection(pos)
            children.append(out_fd["node"])
            out_pd2 = ProcedureDeclarationSection2(out_fd["index"])
            children.append(out_pd2["node"])
            node = Tree("ProcedureDeclarationSection2", children)
            out["node"] = node
            out["index"] = out_pd2["index"]
        else:
            children.append(["Epsilon"])
            node = Tree("ProcedureDeclarationSection2", children)
            out["node"] = node
            out["index"] = pos
    else:
        children.append(["Epsilon"])
        node = Tree("ProcedureDeclarationSection2", children)
        out["node"] = node
        out["index"] = pos
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
        else:

            children.append(["Epsilon"])
            node = Tree("Declarations", children)
            out["index"] = pos
            out["node"] = node
    else :
        children.append(["Epsilon"])
        node = Tree("Declarations", children)
        out["index"] = pos
        out["node"] = node
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

def FunctionDeclarationSection(pos):
    children = []
    out = dict()
    out_Function_Header = FunctionHeader(pos)
    children.append( out_Function_Header["node"])
    out_FPDecl = VarDeclarationSection(out_Function_Header["index"])
    children.append(out_FPDecl["node"])
    out_Func_Block = FunctionBlock(out_FPDecl["index"])
    children.append(out_Func_Block["node"])
    node = Tree("FunctionDecSection", children)
    out["node"] = node
    out["index"] =out_Func_Block["index"]
    return out

def FunctionHeader(pos):
    children = []
    out = dict()
    out_function = Match(Token_type.Function, pos)
    children.append(out_function["node"])
    out_FunctionName = FunctionName(out_function["index"])
    children.append(out_FunctionName["node"])
    out_ArgIdListOption = ArgumentOption(out_FunctionName["index"])
    children.append(out_ArgIdListOption["node"])
    out_colon = Match(Token_type.Colon, out_ArgIdListOption["index"])
    children.append(out_colon["node"])
    out_dataType = DataType(out_colon["index"])
    children.append(out_dataType["node"])
    out_semicolon = Match(Token_type.Semicolon, out_dataType["index"])
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

def FunctionBlock( pos):
    children = []
    out = dict()
    out_begin = Match(Token_type.Begin, pos)
    children.append(out_begin["node"])
    out_statements = Statements(out_begin["index"])
    children.append(out_statements["node"])
    out_end = Match(Token_type.End, out_statements["index"])#todo don't forget to change the index
    children.append(out_end["node"])
    out_semicolon = Match(Token_type.Semicolon, out_end["index"])
    children.append(out_semicolon["node"])
    node = Tree("FunctionBlock", children)
    out["node"] = node
    out["index"] = out_semicolon["index"]
    return out

def ArgumentOption (pos):
    temp = Tokens[pos].to_dict()
    children = []
    out = dict()
    if temp["token_type"] == Token_type.OpenParenthesis:
        out_Oparenthesis = Match(Token_type.OpenParenthesis, pos)
        children.append(out_Oparenthesis["node"])
        out_Arguments=ArgumentIDList(out_Oparenthesis["index"])
        children.append(out_Arguments["node"])
        out_Cparenthesis = Match(Token_type.CloseParenthesis,out_Arguments["index"])
        children.append(out_Cparenthesis["node"])
        node = Tree("ArgumentOption", children)
        out["node"] = node
        out["index"] = out_Cparenthesis["index"]
    else :
        children.append(["Epsilon"])
        node = Tree("ArgumentOption", children)
        out["node"] = node
        out["index"] = pos
    return out
def VarDeclarationSection (pos):
    temp = Tokens[pos].to_dict()
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
        children.append(["Epsilon"])
        node = Tree("VarDeclarationSection", children)
        out["node"] = node
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
    children.append(out_var2["node"])
    node = Tree("VarDeclaration", children)
    out["node"] = node
    out["index"] = out_var2["index"]

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
            out_var = VarDeclaration(pos)
            children.append(out_var["node"])
            node = Tree("VarDeclaration2", children)
            out["node"] = node
            out["index"] = out_var["index"]
        else:
            out["index"] = pos
            children.append(["Epsilon"])
            node = Tree("VarDeclaration2", children)
            out["node"] = node
    else:
        out["index"] = pos
        children.append(["Epsilon"])
        node = Tree("VarDeclaration2", children)
        out["node"] = node
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
    else:
        out["index"] = pos
        children.append(["Epsilon"])
        node = Tree("VarDeclarationIDList2", children)
        out["node"] = node
    return out


def TypeDeclaration(pos):
    children = []
    out = dict()
    out_var = VariableIDList(pos)
    children.append(out_var["node"])
    out_eq = Match(Token_type.EqualOp, out_var["index"])
    children.append(out_eq["node"])
    out_datatype = DataType(out_eq["index"])
    children.append(out_datatype["node"])
    out_semicolon = Match(Token_type.Semicolon, out_datatype["index"])
    children.append(out_semicolon["node"])
    out_typed=TypeDeclaration2(out_semicolon["index"])
    children.append(out_typed["node"])
    node = Tree("TypeDeclaration", children)
    out["node"] = node
    out["index"] = out_typed["index"]
    return out
def TypeDeclaration2(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"]==Token_type.Identifier:
            out_type = TypeDeclaration(pos)
            children.append(out_type["node"])
            node = Tree("TypeDeclaration2", children)
            out["node"] = node
            out["index"] = out_type["index"]
        else:
            out["index"] = pos
            children.append(["Epsilon"])
            node = Tree("TypeDeclaration2", children)
            out["node"] = node
    else:
        out["index"] = pos
        children.append(["Epsilon"])
        node = Tree("TypeDeclaration2", children)
        out["node"] = node
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
        children.append(["Epsilon"])
        node = Tree("ConstDeclarationSection", children)
        out["node"] = node
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
            children.append(["Epsilon"])
            node = Tree("ConstID2", children)
            out["index"] = pos
            out["node"] = node
            return out
#todo : dh kda kda lzm hyt4al 34n mynf3sh el code y accept declsection bs mn 8er b2et el amin block program fa dh just for testing
    else:
        children.append(["Epsilon"])
        node = Tree("ConstID2", children)
        out["index"] = pos
        out["node"] = node
        return out

def MainBlock(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"]==Token_type.Begin:
            out_begin=Match(Token_type.Begin,pos)
            children.append(out_begin["node"])
            out_statement = Statements(out_begin["index"])
            children.append(out_statement["node"])
            out_end=Match(Token_type.End,out_statement["index"])
            children.append(out_end["node"])
            out_dot=Match(Token_type.Dot,out_end["index"])
            children.append(out_dot["node"])
            node = Tree("MainBlock", children)
            out["node"] = node
            out["index"] = out_dot["index"]

    return out


def Statements(pos):
    children = []
    out = dict()
    temp = Tokens[pos].to_dict()
    out_statement=Statement(pos)
    children.append(out_statement["node"])
    out_statementAux=Statement2(out_statement["index"])
    children.append(out_statementAux["node"])
    node = Tree("Statements", children)
    out["node"] = node
    out["index"] = out_statementAux["index"]
    return out
def Statement (pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if (temp["token_type"] == Token_type.Read or temp["token_type"] == Token_type.Write
            or temp["token_type"] == Token_type.WriteLn or temp["token_type"] == Token_type.ReadLn or temp["token_type"] == Token_type.Identifier ):
            out_Atomic_Statements=AtomicStatements(pos)
            children.append(out_Atomic_Statements["node"])
            node = Tree("Statement", children)
            out["node"] = node
            out["index"] = out_Atomic_Statements["index"]
        elif temp["token_type"] == Token_type.If:
            out_If=IF(pos)
            children.append(out_If["node"])
            node = Tree("Statement", children)
            out["node"] = node
            out["index"] = out_If["index"]
        elif temp["token_type"] == Token_type.While :
            out_While = Match(Token_type.While,pos)
            children.append(out_While["node"])
            out_cond = Condition(out_While["index"])
            children.append(out_cond["node"])
            out_do = Match(Token_type.Do,out_cond["index"])
            children.append(out_do["node"])
            out_MultipleStatementBlock=MultipleStatementBlockIF(out_do["index"])
            children.append(out_MultipleStatementBlock["node"])
            node = Tree("Statement", children)
            out["node"] = node
            out["index"] =out_MultipleStatementBlock["index"]
        elif temp["token_type"] == Token_type.Repeat:
            out_repeat=Match(Token_type.Repeat,pos)
            children.append(out_repeat["node"])
            out_Statements=Statements(out_repeat["index"])
            children.append(out_Statements["node"])
            out_until = Match(Token_type.Until,out_Statements["index"])
            children.append(out_until["node"])
            out_condition= Condition(out_until["index"])
            children.append(out_condition["node"])
            node = Tree("Statement", children)
            out["node"] = node
            out["index"] = out_condition["index"]
        elif temp["token_type"] == Token_type.For:
            out_for=Match(Token_type.For,pos)
            children.append(out_for["node"])
            out_id=Match(Token_type.Identifier,out_for["index"])
            children.append(out_id["node"])
            out_colon=Match(Token_type.Colon,out_id["index"])
            children.append(out_colon["node"])
            out_equal = Match(Token_type.EqualOp, out_colon["index"])
            children.append(out_equal["node"])
            out_const=Match(Token_type.Constant, out_equal["index"])
            children.append(out_const["node"])
            out_to=Match(Token_type.To,   out_const["index"])
            children.append(out_to["node"])
            out_const = Match(Token_type.Constant, out_to["index"])
            children.append(out_const ["node"])
            out_do = Match(Token_type.Do,out_const ["index"])
            children.append(out_do["node"])
            out_MultipleStatementBlock = MultipleStatementBlockIF(out_do["index"])
            children.append(out_MultipleStatementBlock["node"])
            node = Tree("Statement", children)
            out["node"] = node
            out["index"] = out_MultipleStatementBlock["index"]
        else :
            children.append(["Epsilon"])
            out ["index"]=pos
            node = Tree("Statement", children)
            out["node"] = node
    print(out["node"])
    return out
def Statement2 (pos):
    children = []
    out = dict()
    if pos < len(Tokens):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Semicolon:
            out_semiColon= Match(Token_type.Semicolon,pos)
            children.append(out_semiColon["node"])
            out_Statement = Statement(out_semiColon["index"])
            children.append(out_Statement["node"])
            out_StatementAux = Statement2(out_Statement["index"])
            children.append(out_StatementAux["node"])
            node = Tree("StatementsAdditional", children)
            out["node"] = node
            out["index"] = out_StatementAux["index"]

        else:
            children.append(["Epsilon"])
            node = Tree("StatementsAdditional", children)
            out["node"] = node
            out["index"] = pos

    return out
def IF (pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"]==Token_type.If:
            out_if=Match(Token_type.If,pos)
            children.append(out_if["node"])
            out_condition=Condition(out_if["index"])
            children.append(out_condition["node"])
            out_then=Match(Token_type.Then,out_condition["index"])
            children.append(out_then["node"])
            out_IfStatOption= ifStatOption(out_then["index"])
            children.append(out_IfStatOption["node"])
            node = Tree("IF", children)
            out["node"] = node
            out["index"] =out_IfStatOption["index"]
    return out
def AtomicStatements(pos):
    temp = Tokens[pos].to_dict()
    children = []
    out = dict()

    if temp["token_type"] == Token_type.Identifier:
        out_fp = FPCallOrAssi(pos)
        children.append(out_fp["node"])
        node = Tree("AtomicStatements", children)
        out["node"] = node
        out["index"] = out_fp["index"]
        return out
    elif temp["token_type"] == Token_type.WriteLn:
        out_writeln = Match(Token_type.WriteLn, pos)
        children.append(out_writeln["node"])
        out_op = Match(Token_type.OpenParenthesis, out_writeln["index"])
        children.append(out_op["node"])
        out_Content=Content(out_op["index"])
        children.append(out_Content["node"])
        out_clos = Match(Token_type.CloseParenthesis, out_Content["index"])
        children.append(out_clos["node"])
        node = Tree("AtomicStatements", children)
        out["node"] = node
        out["index"] = out_clos["index"]
        return out
    elif temp["token_type"] == Token_type.Write:
        out_write = Match(Token_type.Write, pos)
        children.append(out_write["node"])
        out_op = Match(Token_type.OpenParenthesis, out_write["index"])
        children.append(out_op["node"])
        out_cont = Content(out_op["index"])
        children.append(out_cont["node"])
        out_clos = Match(Token_type.CloseParenthesis, out_cont["index"])
        children.append(out_clos["node"])
        node = Tree("AtomicStatements", children)
        out["node"] = node
        out["index"] = out_clos["index"]
        return out
    elif temp["token_type"] == Token_type.ReadLn:
        out_readln = Match(Token_type.ReadLn, pos)
        children.append(out_readln["node"])
        out_op = Match(Token_type.OpenParenthesis, out_readln["index"])
        children.append(out_op["node"])
        out_p = ParametersList(out_op["index"])
        children.append(out_p["node"])
        out_clos = Match(Token_type.CloseParenthesis, out_p["index"])
        children.append(out_clos["node"])
        node = Tree("AtomicStatements", children)
        out["node"] = node
        out["index"] = out_clos["index"]
        return out
    elif temp["token_type"] == Token_type.Read:
        out_read = Match(Token_type.Read, pos)
        children.append(out_read["node"])
        out_op = Match(Token_type.OpenParenthesis, out_read["index"])
        children.append(out_op["node"])
        out_p = ParametersList(out_op["index"])
        children.append(out_p["node"])
        out_clos = Match(Token_type.CloseParenthesis, out_p["index"])
        children.append(out_clos["node"])
        node = Tree("AtomicStatements", children)
        out["node"] = node
        out["index"] = out_clos["index"]
        return out

def MultipleStatementBlockIF(pos):
    temp = Tokens[pos].to_dict()
    out = dict()
    children = []
    if temp["token_type"] == Token_type.Begin:
        out_begin = Match(Token_type.Begin, pos)
        children.append(out_begin["node"])
        out_statements = Statements(out_begin["index"])
        children.append(out_statements["node"])
        out_end = Match(Token_type.End, out_statements["index"])
        children.append(out_end["node"])
        node = Tree("MultipleStatementBlockIF", children)
        out["node"] = node
        out["index"] = out_end["index"]
        return out
    else:
        out = dict()
        out_atomicst = AtomicStatements(pos)
        children.append(out_atomicst["node"])
        node = Tree("MultipleStatementBlockIF", children)
        out["node"] = node
        out["index"] = out_atomicst["index"]
        return out

def ifStatOption(pos):
    children = []
    out = dict()
    out_mult=MultipleStatementBlockIF(pos)
    children.append(out_mult["node"])
    out_statB=StatementBlock(out_mult["index"])
    children.append(out_statB["node"])
    node = Tree("ifStatOption", children)
    out["node"] = node
    out["index"] = out_statB["index"]
    return out
def AssignedValue(pos):
    children=[]
    out = dict()
    temp=Tokens[pos].to_dict()
    if temp["token_type"]==Token_type.Constant:
        out_const = Match(Token_type.Constant, pos)
        children.append(out_const["node"])
        node = Tree("AssignedValue", children)
        out["node"] = node
        out["index"] = out_const["index"]
    elif temp["token_type"]==Token_type.Identifier:
        out_identifier = Match(Token_type.Identifier, pos)
        children.append(out_identifier["node"])
        node = Tree("AssignedValue", children)
        out["node"] = node
        out["index"] = out_identifier["index"]
    elif temp["token_type"]==Token_type.String:
        out_string=Match(Token_type.String,pos)
        children.append(out_string["node"])
        node = Tree("AssignedValue", children)
        out["node"] = node
        out["index"] = out_string["index"]
    else:
        out_exp = Expression(pos)
        children.append(out_exp["node"])
        node = Tree("AssignedValue", children)
        out["node"] = node
        out["index"] = out_exp["index"]
    return out
def BoolOp(pos):
    children=[]
    out = dict()
    temp=Tokens[pos].to_dict()
    if temp["token_type"] == Token_type.GreaterThanOp:
        out_greater=Match(Token_type.GreaterThanOp,pos)
        children.append(out_greater["node"])
        node = Tree("BoolOp", children)
        out["node"] = node
        out["index"] = out_greater["index"]
    elif temp["token_type"] == Token_type.LessThanOp:
        out_less=Match(Token_type.LessThanOp,pos)
        children.append(out_less["node"])
        node = Tree("BoolOp", children)
        out["node"] = node
        out["index"] = out_less["index"]
    elif temp["token_type"] == Token_type.EqualOp:
        out_equal=Match(Token_type.EqualOp,pos)
        children.append(out_equal["node"])
        node = Tree("BoolOp", children)
        out["node"] = node
        out["index"] = out_equal["index"]
    elif temp["token_type"] == Token_type.GreaterThanOrEqualOp:
        out_greaterOrEq=Match(Token_type.GreaterThanOrEqualOp,pos)
        children.append(out_greaterOrEq["node"])
        node = Tree("BoolOp", children)
        out["node"] = node
        out["index"] = out_greaterOrEq["index"]
    elif temp["token_type"] == Token_type.SmallerThanOrEqualOp:
        out_smallerOrEq=Match(Token_type.SmallerThanOrEqualOp,pos)
        children.append(out_smallerOrEq["node"])
        node = Tree("BoolOp", children)
        out["node"] = node
        out["index"] = out_smallerOrEq["index"]
    elif temp["token_type"] == Token_type.NotEqualOp:
        out_notEq=Match(Token_type.NotEqualOp,pos)
        children.append(out_notEq["node"])
        node = Tree("BoolOp", children)
        out["node"] = node
        out["index"] = out_notEq["index"]
    elif temp["token_type"] == Token_type.Not:
        out_not=Match(Token_type.Not,pos)
        children.append(out_not["node"])
        node = Tree("BoolOp", children)
        out["node"] = node
        out["index"] = out_not["index"]
    elif temp["token_type"] == Token_type.And:
        out_and=Match(Token_type.And,pos)
        children.append(out_and["node"])
        node = Tree("BoolOp", children)
        out["node"] = node
        out["index"] = out_and["index"]
    elif temp["token_type"] == Token_type.Or:
        out_or=Match(Token_type.Or,pos)
        children.append(out_or["node"])
        node = Tree("BoolOp", children)
        out["node"] = node
        out["index"] = out_or["index"]
    elif temp["token_type"] == Token_type.Xor:
        out_xor=Match(Token_type.Xor,pos)
        children.append(out_xor["node"])
        node = Tree("BoolOp", children)
        out["node"] = node
        out["index"] = out_xor["index"]

    return out
def MultOp(pos):
    children = []
    out = dict()
    temp = Tokens[pos].to_dict()
    if temp["token_type"] == Token_type.MultiplyOp:
        out_multi=Match(Token_type.MultiplyOp,pos)
        children.append(out_multi["node"])
        node = Tree("MultOp", children)
        out["node"] = node
        out["index"] = out_multi["index"]
    elif temp["token_type"] == Token_type.DivideOp:
        out_divide=Match(Token_type.DivideOp,pos)
        children.append(out_divide["node"])
        node = Tree("MultOp", children)
        out["node"] = node
        out["index"] = out_divide["index"]
    return out
def AddOp(pos):
    children = []
    out = dict()
    temp = Tokens[pos].to_dict()
    if temp["token_type"] == Token_type.PlusOp:
        out_plus = Match(Token_type.PlusOp, pos)
        children.append(out_plus["node"])
        node = Tree("AddOp", children)
        out["node"] = node
        out["index"] = out_plus["index"]
    elif temp["token_type"] == Token_type.MinusOp:
        out_minus = Match(Token_type.MinusOp, pos)
        children.append(out_minus["node"])
        node = Tree("AddOp", children)
        out["node"] = node
        out["index"] = out_minus["index"]
    return out

def Expression(pos):
    children=[]
    out=dict()
    out_term=Term(pos)
    children.append(out_term["node"])
    out_exp=Exp(out_term["index"])
    children.append(out_exp["node"])
    node = Tree("Expression",children)
    out["node"]=node
    out["index"]=out_exp["index"]
    return out

def Exp(pos):
    children=[]
    out=dict()
    if (pos < len(Tokens)):
        temp=Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.PlusOp or temp["token_type"] == Token_type.MinusOp:
            out_addop=AddOp(pos)
            children.append(out_addop["node"])
            out_term=Term(out_addop["index"])
            children.append(out_term["node"])
            out_exp=Exp(out_term["index"])
            children.append(out_exp["node"])
            node = Tree("Exp",children)
            out["node"]=node
            out["index"]=out_exp["index"]
        else:
            children.append(["Epsilon"])
            node = Tree("Exp", children)
            out["index"] = pos
            out["node"] = node
    else:
        children.append(["Epsilon"])
        node = Tree("Exp", children)
        out["index"] = pos
        out["node"] = node
    return out

def Term(pos):
    children=[]
    out=dict()
    out_factor=Factor(pos)
    children.append(out_factor["node"])
    out_ter=Term2(out_factor["index"])
    children.append(out_ter["node"])
    node = Tree("Term",children)
    out["node"]=node
    out["index"]=out_ter["index"]
    return out

def Term2(pos):
    children=[]
    out=dict()
    if (pos < len(Tokens)):
        temp=Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.MultiplyOp or temp["token_type"] == Token_type.DivideOp:
            out_multop=MultOp(pos)
            children.append(out_multop["node"])
            out_factor=Factor(out_multop["index"])
            children.append(out_factor["node"])
            out_ter=Term2(out_factor["index"])
            children.append(out_ter["node"])
            node = Tree("Ter",children)
            out["node"]=node
            out["index"]=out_ter["index"]
            return out
        else:
            children.append(["Epsilon"])
            node = Tree("Term2", children)
            out["index"] = pos
            out["node"] = node
            return out
    else:
        children.append(["Epsilon"])
        node = Tree("Term2", children)
        out["index"] = pos
        out["node"] = node
        return out

def Factor(pos):
    children=[]
    out=dict()
    temp=Tokens[pos].to_dict()
    if temp["token_type"] ==Token_type.Identifier:
        out_identifier=Match(Token_type.Identifier,pos)
        children.append(out_identifier["node"])
        node=Tree("Factor",children)
        out["node"]=node
        out["index"]=out_identifier["index"]
    elif temp["token_type"]==Token_type.Constant:
        out_const = Match(Token_type.Constant, pos)
        children.append(out_const["node"])
        node = Tree("Factor", children)
        out["node"] = node
        out["index"] = out_const["index"]
    elif temp["token_type"]==Token_type.OpenParenthesis:
        out_openparen=Match(Token_type.OpenParenthesis,pos)
        children.append(out_openparen["node"])
        out_experssion=Expression(out_openparen["index"])
        children.append(out_experssion["node"])
        out_closeparen=Match(Token_type.CloseParenthesis,out_experssion["index"])
        children.append(out_closeparen["node"])
        node = Tree("Factor",children)
        out["node"]=node
        out["index"]=out_closeparen["index"]
    #todo else here to be for errors
    return out

def FPCallOrAssi(pos):
    children=[]
    out=dict()
    out_identifier=Match(Token_type.Identifier,pos)
    children.append(out_identifier["node"])
    out_fpcallorassi2=FPCallOrAssi2(out_identifier["index"])
    children.append(out_fpcallorassi2["node"])
    node=Tree("FPCallOrAssi",children)
    out["node"]=node
    out["index"]=out_fpcallorassi2["index"]
    return out

def FPCallOrAssi2(pos):
    children=[]
    out=dict()
    if (pos < len(Tokens)):
        temp=Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Colon:
            out_colon=Match(Token_type.Colon,pos)
            children.append(out_colon["node"])
            out_eq=Match(Token_type.EqualOp,out_colon["index"])
            children.append(out_eq["node"])
            out_fpcallorassi3=FPCallOrAssi3(out_eq["index"])
            children.append(out_fpcallorassi3["node"])
            node=Tree("FPCallOrAssi2",children)
            out["node"]=node
            out["index"]=out_fpcallorassi3["index"]
            return out
        elif temp["token_type"]==Token_type.OpenParenthesis:
            out_open=Match(Token_type.OpenParenthesis,pos)
            children.append(out_open["node"])
            out_parameterlist=ParametersList(out_open["index"])
            children.append(out_parameterlist["node"])
            out_close=Match(Token_type.CloseParenthesis,out_parameterlist["index"])
            children.append(out_close["node"])
            node=Tree("FPCallOrAssi2",children)
            out["node"]=node
            out["index"]=out_close["index"]
            return out
        else:
            children.append(["Epsilon"])
            node = Tree("FPCallOrAssi2", children)
            out["index"] = pos
            out["node"] = node
            return out
    else:
        children.append(["Epsilon"])
        node = Tree("FPCallOrAssi2", children)
        out["index"] = pos
        out["node"] = node
        return out
def FPCallOrAssi3(pos):
    children=[]
    out=dict()
    temp=Tokens[pos].to_dict()
    if temp["token_type"] == Token_type.Identifier:
        out_identifier=Match(Token_type.Identifier,pos)
        children.append(out_identifier["node"])
        var = Tokens[out_identifier["index"]].to_dict()
        print(var["token_type"])
        if (var["token_type"]==Token_type.PlusOp or var["token_type"]==Token_type.MinusOp):
            out_exp=Exp(out_identifier["index"])
            children.append(out_exp["node"])
            node = Tree("FPCallOrAssi3",children)
            out["node"]=node
            out["index"]=out_exp["index"]
        elif (var["token_type"]==Token_type.MultiplyOp or var["token_type"] == Token_type.DivideOp):
            out_term2=Term2(out_identifier["index"])
            children.append(out_term2["node"])
            node = Tree("FPCallOrAssi3", children)
            out["node"] = node
            out["index"] = out_term2["index"]
        else :
            out_fpcall4=FPCallOrAssi4(out_identifier["index"])
            children.append(out_fpcall4["node"])
            node = Tree("FPCallOrAssi3", children)
            out["node"] = node
            out["index"] = out_fpcall4["index"]
    elif (temp["token_type"]==Token_type.Constant or temp["token_type"]==Token_type.String):
        out_assigned=AssignedValue(pos)
        children.append(out_assigned["node"])
        node=Tree("FPCallOrAssi3",children)
        out["node"]=node
        out["index"]=out_assigned["index"]
    #todo error place here
    #else :

    return out

def FPCallOrAssi4(pos):
    children = []
    out = dict()
    if (pos < len(Tokens)):
        temp = Tokens[pos].to_dict()
        if temp["token_type"]==Token_type.OpenParenthesis:
            out_open=Match(Token_type.OpenParenthesis,pos)
            children.append(out_open["node"])
            out_parameterlist=ParametersList(out_open["index"])
            children.append(out_parameterlist["node"])
            out_close=Match(Token_type.CloseParenthesis,out_parameterlist["index"])
            children.append(out_close["node"])
            node=Tree("FPCallOrAssi4",children)
            out["node"]=node
            out["index"]=out_close["index"]
            return out
        else:
            children.append(["Epsilon"])
            node = Tree("FPCallOrAssi4", children)
            out["index"] = pos
            out["node"] = node
    else:
        children.append(["Epsilon"])
        node = Tree("FPCallOrAssi4", children)
        out["index"] = pos
        out["node"] = node
    return out



def StatementBlock(pos):
    temp = Tokens[pos].to_dict()
    children = []
    out = dict()
    if temp["token_type"] == Token_type.Else:
        out_else = Match(Token_type.Else, pos)
        children.append(out_else["node"])
        out_mult = MultipleStatementBlockIF(out_else["index"])
        children.append(out_mult["node"])
        node = Tree("StatementBlock", children)
        out["node"] = node
        out["index"] = out_mult["index"]
        return out
    else :
        children.append(["Epsilon"])
        node = Tree("StatementBlock", children)
        out["node"] = node
        out["index"] = pos
        return out
    #todo error here
    #else :
    return out
def Condition(pos):
    children=[]
    out=dict()
    temp = Tokens[pos].to_dict()
    if temp["token_type"] == Token_type.OpenParenthesis:
        out_openparen=Match(Token_type.OpenParenthesis,pos)
        children.append(out_openparen["node"])
        out_condition=Condition(out_openparen["index"])
        children.append(out_condition["node"])
        out_closeparen=Match(Token_type.CloseParenthesis,out_condition["index"])
        children.append(out_closeparen["node"])
        out_cond2=Condition2(out_closeparen["index"])
        children.append(out_cond2["node"])
        node=Tree("Condition",children)
        out["node"]=node
        out["index"]=out_cond2["index"]
    elif temp["token_type"] == Token_type.Identifier:
        out_exp=Expression(pos)
        children.append(out_exp["node"])
        out_boolop=BoolOp(out_exp["index"])
        children.append(out_boolop["node"])
        out_exp=Expression(out_boolop["index"])
        children.append(out_exp["node"])
        node=Tree("Condition",children)
        out["node"]=node
        out["index"]=out_exp["index"]
    #else:
    return out
def Condition2(pos):
    children=[]
    out=dict()
    temp = Tokens[pos].to_dict()
    if (temp["token_type"]== Token_type.GreaterThanOp or temp["token_type"]== Token_type.GreaterThanOrEqualOp or
        temp["token_type"] == Token_type.LessThanOp or temp["token_type"]== Token_type.SmallerThanOrEqualOp or
        temp["token_type"] == Token_type.EqualOp or temp["token_type"]== Token_type.NotEqualOp or
        temp["token_type"] == Token_type.And or temp["token_type"]== Token_type.Or or temp["token_type"]== Token_type.Not
        or temp["token_type"]== Token_type.Xor):
        out_boolOp=BoolOp(pos)
        children.append(out_boolOp["node"])
        out_open=Match(Token_type.OpenParenthesis,out_boolOp["index"])
        children.append(out_open["node"])
        out_condition = Condition(out_open["index"])
        children.append(out_condition["node"])
        out_closeparen = Match(Token_type.CloseParenthesis, out_condition["index"])
        children.append(out_closeparen["node"])
        out_cond2 = Condition2(out_closeparen["index"])
        children.append(out_cond2["node"])
        node=Tree("Condition2",children)
        out["node"]=node
        out["index"]=out_cond2["index"]
    else:
        children.append(["Epsilon"])
        node = Tree("Condition2", children)
        out["index"] = pos
        out["node"] = node
    return out
def Content(pos):
    children = []
    out = dict()
    temp = Tokens[pos].to_dict()
    if temp["token_type"] == Token_type.String:
        out_string=Match(Token_type.String,pos)
        children.append(out_string["node"])
        out_content2=Content2(out_string["index"])
        children.append(out_content2["node"])
        node = Tree("Content",children)
        out["node"]=node
        out["index"]=out_content2["index"]
    elif temp["token_type"] == Token_type.Identifier:
        out_identifier=Match(Token_type.Identifier,pos)
        children.append(out_identifier["node"])
        out_content2=Content2(out_identifier["index"])
        children.append(out_content2["node"])
        node = Tree("Content",children)
        out["node"]=node
        out["index"]=out_content2["index"]
    elif temp["token_type"] == Token_type.Constant:
        out_const=Match(Token_type.Constant,pos)
        children.append(out_const["node"])
        out_content2=Content2(out_const["index"])
        children.append(out_content2["node"])
        node = Tree("Content", children)
        out["node"] = node
        out["index"] = out_content2["index"]
    return out

def Content2(pos):
    children = []
    out = dict()
    if pos < len(Tokens):
        temp = Tokens[pos].to_dict()
        if temp["token_type"] == Token_type.Comma:
            out_comma = Match(Token_type.Comma,pos)
            children.append(out_comma["node"])
            #out_leftFactcontent=LeftFactorContent(out_comma["index"])
            #children.append(out_leftFactcontent["node"])
            out_content=Content(out_comma["index"])
            children.append(out_content["node"])
            node=Tree("Content2",children)
            out["node"]=node
            out["index"]=out_content["index"]
            return out
        else:
            children.append(["Epsilon"])
            node = Tree("Content2", children)
            out["index"] = pos
            out["node"] =node
            return out
    else:
        children.append(["Epsilon"])
        node = Tree("Content2", children)
        out["index"] = pos
        out["node"] = node
        return out
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
            output["index"] = pos
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

def make_handler(table):
    def handle_click(event):
        if make_handler.stall: return
        row_number = table.get_row_clicked(event)
        if row_number >= len(Tokens): return
        print("Clicked row number:", row_number)
        from modules.dfa import vizualize
        tok = Tokens[row_number].to_dict()
        make_handler.stall = True
        vizualize(tok["Lex"], tok["token_type"])
        from PIL import ImageTk, Image
        image_window = tk.Toplevel(root)
        image_window.title("Image Preview")
        image_path = "result.gv.png"
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(image_window, image=photo)
        label.image = photo
        label.pack()
        make_handler.stall = False
    return handle_click
make_handler.stall = False
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
    dTDaPT.bind('<ButtonRelease-1>', make_handler(dTDaPT))
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





