import yaml
from PushdownAutomata import PushdownAutomata

def main():
    with open("sample.yaml") as file:
        try:
            pda_def = yaml.full_load(file)
        except Exception as e:
            print(e)
            exit(1)
        pda = PushdownAutomata(pda_def)
        pda.run("baba")
        pda.run("abbaab")
        pda.run("abbaa")

if __name__ == "__main__":
    main()
