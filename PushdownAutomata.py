from typing import Any


def valid_transition(transition: dict, valid_states: list[str], alphabet: str) -> bool:
    for alpha, dest_info in transition.items():
        if alpha not in list(alphabet):
            print(f"Invalid transition character: {alpha}")
            return False

        if type(dest_info) is str and dest_info not in valid_states:
            print(f"Destination {dest_info} not in states array")
            return False

        elif type(dest_info) is dict:
            if dest_info.get("stack") is not None:
                for transition_info in dest_info.get("stack").values():
                    destination = transition_info.get("to")
                    if destination not in valid_states:
                        print(f"Destination state {destination} not in states array")
                        return False

            default_dest = dest_info.get("to")
            if default_dest is not None and default_dest not in valid_states:
                print(f"Destination state {repr(default_dest)} not in states array")
                return False

    return True


class PushdownAutomata:
    def __init__(self, definition: dict[str, Any], debug=False):
        try:
            self.__debug = debug
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

            for state, value in self.__transitions.items():
                if state not in self.__states:
                    raise Exception(f"'{state}' is not in 'states'")

                if state in self.__end:
                    raise Exception(
                        f"'{state}' is defined as an end state and should not have any transitions"
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
            if self.__debug:
                print(f"Transitioning from {self.__current} via char '{self.word[0]}'")
            self.transition()

        if self.__current in self.__final:
            print(f"'{word}' is accepted\n")
        else:
            print(
                f"""\
'{word}' is not accepted
"""
            )

            if self.__debug:
                print(
                    """\
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
            # pop the top of the stack
            self.__stack = self.__stack[:-1]
        # we have stack-based transitions
        elif type(transition_info) is dict:
            using_stack = False
            stack_vals = transition_info.get("stack")
            if stack_vals is not None:
                for value, transition in stack_vals.items():
                    if self.__stack[:-1] == value:
                        self.__stack = self.__stack[: -transition.get("pop") or 1]
                        self.__stack.extend(transition.get("push") or [])
                        self.__current = transition.get("to")
                        using_stack = True
                        break

            if not using_stack:
                self.__stack = self.__stack[: -transition_info.get("pop") or 1]
                self.__stack.extend(transition_info.get("push") or [])
                self.__current = transition_info.get("to")

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
