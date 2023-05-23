from visual_automata.fa.dfa import VisualDFA
from modules.Tokens import *
import re
import time

def StringsDFA(text: str):
    states = {"q0", "q1", "q2", "q3", "reject"}
    input_symbols = {"'", "*"}
    transitions = {
        "q0": {"'": "q1", "*": "reject"},
        "q1": {"'": "q3", "*": "q2"},
        "q2": {"'": "q3", "*": "q2"},
        "q3": {"'": "reject", "*": "reject"},
        "reject": {"'": "reject", "*": "reject"},
    }
    dfa = VisualDFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state="q0",
        final_states={"q3"},
    )
    text = f"'{'*' * len(text)}'"
    print(dfa.table)
    dfa.show_diagram(
        text,
        view=True,
        filename="result.gv",
        horizontal=True,
        state_seperation=2,
    )


def IdentifiersDFA(text: str):
    states = {"q0", "q1", "q2", "reject"}
    input_symbols = {"c", "d"}
    transitions = {
        "q0": {"c": "q1", "d": "reject"},
        "q1": {"c": "q2", "d": "q2"},
        "q2": {"c": "q2", "d": "q2"},
        "reject": {"c": "reject", "d": "reject"},
    }
    dfa = VisualDFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state="q0",
        final_states={"q1", "q2"},
    )
    text = re.sub(r"\d", "d", text)
    text = re.sub(r"[a-zA-Z]", "c", text)
    print(dfa.table)
    dfa.show_diagram(
        text,
        view=True,
        filename="result.gv",
        horizontal=True,
        state_seperation=2,
    )


def NumbersDFA(text: str):
    states = {"q0", "q1", "q2", "q3", "q4", "reject"}
    input_symbols = {".", "d"}
    transitions = {
        "q0": {".": "q2", "d": "q1"},
        "q1": {".": "q3", "d": "q1"},
        "q2": {".": "reject", "d": "q4"},
        "q3": {".": "reject", "d": "q4"},
        "q4": {".": "reject", "d": "q4"},
        "reject": {".": "reject", "d": "reject"},
    }
    dfa = VisualDFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state="q0",
        final_states={"q1", "q3", "q4"},
    )
    text = re.sub(r"\d", "d", text)
    print(dfa.table)
    dfa.show_diagram(
        text,
        view=True,
        filename="result.gv",
        horizontal=True,
        state_seperation=2,
    )


# NumbersDFA("323.922.9.9")


def NFA(text: str):
    from automathon import NFA

    states = {"q0"}
    input_symbols = set()
    transitions = {}
    prev_state = "q0"
    for c in text:
        curr_state = f"q{len(states)}"
        states.add(curr_state)
        input_symbols.add(c)
        transitions[prev_state] = {c: {curr_state}}
        prev_state = curr_state
    automata = NFA(states, input_symbols, transitions, "q0", {prev_state})
    automata.view("result")


# NFA()


def DictionaryDFA(text: str, dictionary: dict[str, Token_type]):
    final_states_tmp = set()
    input_symbols = set()
    for key in dictionary:
        final_states_tmp.add(key)
        for c in key:
            input_symbols.add(c)
    states = {"", "reject"}
    states.update({key for key in dictionary})
    transitions = {state: {} for state in states}
    for state in states:
        for symbol in input_symbols:
            if state + symbol in states:
                transitions[state][symbol] = state + symbol
            else:
                transitions[state][symbol] = "reject"
    mapping = {"reject": "reject"}
    for idx, key in enumerate(states):
        if key != "reject":
            mapping[key] = f"q{str(idx)}"
    states.clear()
    for value in mapping.values():
        states.add(value)
    final_states = set()
    for state in final_states_tmp:
        final_states.add(mapping[state])
    keys = list(transitions.keys())
    for key in keys:
        transitions[mapping[key]] = transitions[key]
        if key != "reject":
            del transitions[key]
        for tra in transitions[mapping[key]]:
            if transitions[mapping[key]][tra] == "reject":
                continue
            transitions[mapping[key]][tra] = mapping[transitions[mapping[key]][tra]]
    dfa = VisualDFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=mapping[""],
        final_states=final_states,
    )
    print(dfa.table)
    dfa.show_diagram(
        text,
        view=True,
        fig_size=(32, 32)
    )
    time.sleep(3)
    NFA(text)


def vizualize(text: str, token_type: Token_type) -> None:
    if token_type == Token_type.Constant:
        NumbersDFA(text)
    elif token_type == Token_type.Identifier:
        IdentifiersDFA(text)
    elif token_type == Token_type.String:
        StringsDFA(text)
    elif token_type in Operators.values():
        DictionaryDFA(text, Operators)
    elif token_type in ReservedWords.values():
        DictionaryDFA(text, ReservedWords)
    elif token_type == Token_type.Dot:
        DictionaryDFA(text, {".": Token_type.Dot})

