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
            self.states = definition["states"]
            self.initial: str = definition["initial"]
            self.end = list(definition["end"])
            self.final = list(definition["final"])
            self.stack: list = definition.get("stack", [])
            self.transitions: dict[str, Any] = definition.get("transitions", {})
            if len(self.transitions) == 0:
                raise Exception("'transitions' must not be empty")

            for key, value in self.transitions.items():
                if key not in self.states:
                    raise Exception(f"'{key}' is not in 'states'")

                if not valid_transition(value, self.states, self.alphabet):
                    exit(1)

            print(self)

        except KeyError as e:
            print(f"Could not find required value {e}")

    def run(self, word: str):
        pass

    def __str__(self):
        return f"""Alphabet: {self.alphabet}
States: {self.states}
Initial: {self.initial}
End: {self.end}
Final: {self.final}
Stack: {self.stack}
Transitions: {self.transitions}"""
