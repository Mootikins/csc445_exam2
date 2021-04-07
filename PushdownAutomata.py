from typing import Any


def valid_transition(transition: dict, valid_states: list[str], alphabet: str) -> bool:
    for alpha, dest in transition.items():
        if alpha not in list(alphabet):
            print(f"Invalid transition character: {alpha}")
            return False

        if type(dest) is str and dest not in valid_states:
            print(f"Invalid transition destination: {dest}")
            return False
        elif type(dest) is dict:
            for stack_val, info in dest.items():
                if stack_val != "else":
                    for instr, vals in info.items():
                        if instr not in ["to", "push", "pop"]:
                            print(f"Invalid conditional stack transition info: {instr}")
                            return False
                        if instr == "to" and vals not in valid_states:
                            print(f"Invalid 'to' state: {vals}")
                            return False

                elif info not in valid_states:
                    print(f"Invalid 'else' state: {info}")
                    return False

    return True


class PushdownAutomata:
    def __init__(self, definition: dict[str, Any]):
        try:
            self.alphabet = definition["alphabet"]
            self.states = list(set(definition["states"]))
            if len(self.states) != len(definition["states"]):
                raise Exception("Duplicate states found")
            self.initial: str = definition["initial"]
            self.end = list(definition["end"])
            self.final = list(definition["final"])
            self.stack: list = definition.get("stack", [])
            self.transitions: dict[str, Any] = definition.get("transitions", {})
            self.current = self.initial
            if len(self.transitions) == 0:
                raise Exception("'transitions' must not be empty")

            for key, value in self.transitions.items():
                if key not in self.states:
                    raise Exception(f"'{key}' is not in 'states'")

                if not valid_transition(value, self.states, self.alphabet):
                    exit(1)
        except KeyError as e:
            print(f"Could not find required value {e}")

    def run(self, word: str):
        for alpha in list(word):
            if alpha not in self.alphabet:
                print(f"'{word}' has character not in alphabet '{self.alphabet}': {alpha}")
                return
        self.current = self.initial
        print(f"Testing word: {word}")
        self.word = word
        while len(self.word) > 0 and self.current not in self.end:
            print(f"Transitioning from {self.current} via char '{self.word[0]}'")
            self.transition()

        if self.current in self.final:
            print(f"'{word}' is accepted\n")
        else:
            print(
                f"""\
'{word}' is not accepted
\tCurrent state: {self.current}
\tRemaining text: {self.word}\n"""
            )

    def transition(self):
        char = self.word[0]
        transition = self.transitions.get(self.current)
        if transition is None:
            self.current = "error"
            return

        transition_info = transition.get(char)
        # direct transition
        if type(transition_info) is str:
            self.current = transition_info
        # we have stack-based transitions
        elif type(transition_info) is dict:
            for entry, data in transition_info.items():
                if len(self.stack) > 0 and self.stack[-1] == entry:
                    self.current = data
                    self.stack = self.stack[: -data.get("pop", 0)]
                    self.stack.extend(data.get("push", []))

            if transition_info.get("else") is None:
                self.current = "error"
            else:
                self.current = transition_info.get("else")

        self.word = self.word[1:]

    def __str__(self):
        return f"""\
Alphabet: {self.alphabet}
States: {self.states}
Initial: {self.initial}
End: {self.end}
Final: {self.final}
Stack: {self.stack}
Current: {self.current}
Transitions: {self.transitions}"""
