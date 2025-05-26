import json


class State:
    __counter = 0

    def __init__(self, id: None) -> None:
        if id is None:
            self.id = State._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, 'State'] = {}

    def add_transition(self, symbol: str, state: 'State') -> None:
        self.transitions[symbol] = state

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class DFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list['State'] = []
        self.alphabet: list['str'] = []
        self.final_states: list['State'] = []

    @staticmethod
    def deserialize_json(json_str: str) -> 'DFA':
        fa = DFA()
        json_fa = json.loads(json_str)

        fa.alphabet = json_fa["alphabet"]

        for state_str in json_fa["states"]:
            fa.add_state(int(state_str[2:]))

        fa.init_state = fa.get_state_by_id(json_fa["initial_state"][2:])

        for final_str in json_fa["final_states"]:
            fa.add_final_state(fa.get_state_by_id(final_str[2:]))

        for state_str in json_fa["states"]:
            for symbol in fa.alphabet:
                fa.add_transition(fa.get_state_by_id(state_str[2:]), fa.get_state_by_id(json_fa[state_str][symbol][2:]),
                                  symbol)

        return fa

    def serialize_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }

        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for symbol in self.alphabet:
                fa[f"q_{state.id}"][symbol] = f"q_{state.transitions[symbol].id}"

        return json.dumps(fa)

    def add_state(self, id: int | None = None) -> State:
        state = State(id)
        self.states.append(state)
        return state

    def add_transition(self, from_state: State, to_state: State, input_symbol: str) -> None:
        from_state.add_transition(input_symbol, to_state)

    def assign_initial_state(self, state: State) -> None:
        self.init_state = state

    def assign_alphabet(self, alphabets: list[str]):
        self.alphabet = alphabets

    def add_final_state(self, state: State) -> None:
        self.final_states.append(state)

    def get_state_by_id(self, id) -> State | None:
        int_id = int(id)
        for state in self.states:
            if state.id == int_id:
                return state

    def is_final(self, state: State) -> bool:
        if state in self.final_states:
            return True
        return False

    def is_accept(self, word: str):
        q:State = self.init_state
        for a in word:
            q = q.transitions[a]
        if q in self.final_states:
            return True
        return False


class NFAState(State):
    __counter = 0

    def __init__(self, id: None) -> None:
        super().__init__(id)
        if id is None:
            self.id = NFAState._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, list['NFAState']] = {}

    def add_transition(self, symbol: str, nfastate: 'NFAState') -> None:
        if symbol in self.transitions.keys():
            self.transitions[symbol] += [nfastate]
        else:
            self.transitions[symbol] = [nfastate]

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class NFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list['NFAState'] = []
        self.alphabet: list['str'] = ['']
        self.final_states: list['NFAState'] = []

    @staticmethod
    def deserialize_json(json_str: str) -> 'NFA':
        fa = NFA()
        json_fa = json.loads(json_str)

        fa.alphabet += json_fa["alphabet"]

        for state_str in json_fa["states"]:
            fa.add_state(int(state_str[2:]))

        fa.init_state = fa.get_state_by_id(json_fa["initial_state"][2:])

        for final_str in json_fa["final_states"]:
            fa.add_final_state(fa.get_state_by_id(final_str[2:]))

        for state_str in json_fa["states"]:
            for symbol in fa.alphabet:
                fa.add_transition(fa.get_state_by_id(state_str[2:]), fa.get_state_by_id(json_fa[state_str][symbol][2:]),
                                  symbol)

        return fa

    def add_state(self, id: int | None = None) -> NFAState:
        state = NFAState(id)
        self.states.append(state)
        return state

    def add_transition(self, from_state: NFAState, to_state: NFAState, input_symbol: str) -> None:
        from_state.add_transition(input_symbol, to_state)

    def assign_initial_state(self, state: NFAState) -> None:
        self.init_state = state

    def add_final_state(self, state: NFAState) -> None:
        self.final_states.append(state)

    def get_state_by_id(self, id) -> NFAState | None:
        int_id = int(id)
        for state in self.states:
            if state.id == int_id:
                return state

    def is_final(self, state: NFAState) -> bool:
        if state in self.final_states:
            return True
        return False

    @staticmethod
    def convert_DFA_instanse_to_NFA_instanse(dfa_machine: 'DFA') -> 'NFA':
        nfa_machine = NFA()
        for state in dfa_machine.states:
            nfa_machine.add_state(state.id)

        nfa_machine.alphabet += dfa_machine.alphabet

        nfa_machine.assign_initial_state(nfa_machine.get_state_by_id(dfa_machine.init_state))

        for state1 in dfa_machine.states:
            for sy in state1.transitions.keys():
                nfa_machine.add_transition(nfa_machine.get_state_by_id(state1.id),
                                           nfa_machine.get_state_by_id(state1.id), sy)

        for f_state in dfa_machine.final_states:
            nfa_machine.add_final_state(nfa_machine.get_state_by_id(f_state.id))

    @staticmethod
    def union(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        total_machine = NFA()
        total_machine.add_state(-1)
        total_machine.assign_initial_state(total_machine.get_state_by_id(-1))
        total_machine.add_transition(total_machine.get_state_by_id(-1), machine1.init_state, '')
        total_machine.add_transition(total_machine.get_state_by_id(-1), machine2.init_state, '')
        total_machine.add_state(-2)
        total_machine.add_final_state(total_machine.get_state_by_id(-2))

        for state1 in machine1.states:
            total_machine.add_state(state1.id)

        for state1 in machine1.states:
            for sy in state1.transitions.keys():
                for st in state1.transitions[sy]:
                    total_machine.add_transition(total_machine.get_state_by_id(state1.id),
                                                 total_machine.get_state_by_id(st.id), sy)

        for state2 in machine2.states:
            total_machine.add_state(len(machine1.states) + state2.id)

        for state2 in machine2.states:
            for sy in state2.transitions.keys():
                for st in state2.transitions[sy]:
                    total_machine.add_transition(total_machine.get_state_by_id(len(machine1.states) + state2.id),
                                                 total_machine.get_state_by_id(len(machine1.states) + st.id), sy)

        for f_state1 in machine1.final_states:
            total_machine.add_transition(total_machine.get_state_by_id(f_state1.id), total_machine.get_state_by_id(-2),
                                         '')

        for f_state2 in machine2.final_states:
            total_machine.add_transition(total_machine.get_state_by_id(f_state2.id), total_machine.get_state_by_id(-2),
                                         '')

        return total_machine

    @staticmethod
    def concat(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        total_machine = NFA()

        for state1 in machine1.states:
            total_machine.add_state(state1.id)

        for state1 in machine1.states:
            for sy in state1.transitions.keys():
                for st in state1.transitions[sy]:
                    total_machine.add_transition(total_machine.get_state_by_id(state1.id),
                                                 total_machine.get_state_by_id(st.id), sy)
        total_machine.assign_initial_state(total_machine.get_state_by_id(machine1.init_state.id))
        for state2 in machine2.states:
            total_machine.add_state(len(machine1.states) + state2.id)

        for state2 in machine2.states:
            for sy in state2.transitions.keys():
                for st in state2.transitions[sy]:
                    total_machine.add_transition(total_machine.get_state_by_id(len(machine1.states) + state2.id),
                                                 total_machine.get_state_by_id(len(machine1.states) + st.id), sy)

        for f_state1 in machine2.final_states:
            total_machine.add_transition(total_machine.get_state_by_id(f_state1.id), machine2.init_state, '')

        for f_state2 in machine2.final_states:
            total_machine.add_final_state(total_machine.get_state_by_id(f_state2.id))
        return total_machine

    @staticmethod
    def star(machine: 'NFA') -> 'NFA':
        total_machine = NFA()

        for state1 in machine.states:
            total_machine.add_state(state1.id)

        for state1 in machine.states:
            for sy in state1.transitions.keys():
                for st in state1.transitions[sy]:
                    total_machine.add_transition(total_machine.get_state_by_id(state1.id),
                                                 total_machine.get_state_by_id(st.id), sy)

        total_machine.assign_initial_state(total_machine.get_state_by_id(machine.init_state.id))

        for f_state in machine.final_states:
            total_machine.add_final_state(total_machine.get_state_by_id(f_state.id))

        for f_state in total_machine.final_states:
            total_machine.add_transition(f_state, total_machine.init_state, '')
            total_machine.add_transition(total_machine.init_state, f_state, '')

        return total_machine

    def serialize_to_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }

        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for symbol in self.alphabet:
                for st in state.transitions[symbol]:
                    if symbol in fa[f"q_{state.id}"].keys():
                        fa[f"q_{state.id}"][symbol] += [f"q_{st.id}"]
                    else:
                        fa[f"q_{state.id}"][symbol] = [f"q_{st.id}"]

        return json.dumps(fa)
