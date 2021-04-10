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
            self.__alphabet = definition["alphabet"]
            self.__states = list(set(definition["states"]))
            if len(self.__states) != len(definition["states"]):
                raise Exception("Duplicate states found")
            self.__initial: str = definition["initial"]
            self.__end = list(definition["end"])
            self.__final = list(definition["final"])
            self.__stack: list = definition.get("stack", [])
            self.__transitions: dict[str, Any] = definition.get("transitions", {})
            self.__current = self.__initial
            if len(self.__transitions) == 0:
                raise Exception("'transitions' must not be empty")

            for key, value in self.__transitions.items():
                if key not in self.__states:
                    raise Exception(f"'{key}' is not in 'states'")

                if key in self.__end:
                    raise Exception(
                        f"'{key}' is defined as an end state and should not have any transitions"
                    )

                if not valid_transition(value, self.__states, self.__alphabet):
                    exit(1)

        except KeyError as e:
            print(f"Could not find required value {e}")

    def run(self, word: str):
        for alpha in list(word):
            if alpha not in self.__alphabet:
                print(
                    f"'{word}' has character not in alphabet '{self.__alphabet}': {alpha}"
                )
                return
        self.__current = self.__initial
        print(f"Testing word: {word}")
        self.word = word
        while len(self.word) > 0 and self.__current not in self.__end:
            print(f"Transitioning from {self.__current} via char '{self.word[0]}'")
            self.transition()

        if self.__current in self.__final:
            print(f"'{word}' is accepted\n")
        else:
            print(
                f"""\
'{word}' is not accepted
\tCurrent state: {self.__current}
\tRemaining text: {self.word}\n"""
            )

    def transition(self):
        char = self.word[0]
        transition = self.__transitions.get(self.__current)
        if transition is None:
            self.__current = "error"
            return

        transition_info = transition.get(char)
        # direct transition
        if type(transition_info) is str:
            self.__current = transition_info
        # we have stack-based transitions
        elif type(transition_info) is dict:
            using_stack = False
            for entry, data in transition_info.items():
                if (
                    len(self.__stack) > 0
                    and self.__stack[-1] == entry
                    and entry != "else"
                ):
                    self.__current = data
                    self.__stack = self.__stack[: -data.get("pop", 0)]
                    self.__stack.extend(data.get("push", []))
                    using_stack = True

            if not using_stack:
                if transition_info.get("else") is None:
                    self.__current = "error"
                else:
                    self.__current = transition_info.get("else")

        self.word = self.word[1:]

    def __str__(self):
        return f"""\
Alphabet: {self.__alphabet}
States: {self.__states}
Initial: {self.__initial}
End: {self.__end}
Final: {self.__final}
Stack: {self.__stack}
Current: {self.__current}
Transitions: {self.__transitions}"""
