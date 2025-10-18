from theory import Theory
from typing import Callable
import mido

class Piano():
    def __init__(self) -> None:
        self.theory: Theory = Theory()
        self.notes: list[int] = []
        self.relative: list[int] = []
        self.inversions: list[str] = [
            "1st",
            "2nd",
            "3rd",
            "4th",
            "5th",
            "6th"
        ]
        self.chord_inversions: dict[str, list[int]] = {
            "1st": [],
            "2nd": [],
            "3rd": [],
            "4th": [],
            "5th": [],
            "6th": []
        }
        # self.identifying: bool = False
        # self.testing: bool = False
        # self.selection: str = input("What type (Identifying or Testing, I/i or T/t)?: ")
        # if self.selection in 'Ii':
        #     self.identifying = True
        # elif self.selection in 'Tt':
        #     self.testing = True
    
    def root_note(self, inversion: str = "") -> str:
        """Returns the root note for intervals/chords/scales"""
        # 21 is A(0) on 88 key piano
        if inversion != "":
            # Works only with standard chords voicings, i.e. one of each note
            return self.theory.get_root_notes()[(self.notes[-(self.inversions.index(inversion)+1)]-21)%12]
        return self.theory.get_root_notes()[(self.notes[0]-21)%12]

    def intervals(self) -> str:
        """Returns the intervals between any 2 notes"""
        return self.theory.get_intervals()[(self.notes[1]-self.notes[0])%12]

    def identify(self, get_chords: Callable[[], dict[str, list[int]]], specific_chord: Callable[[str], list[int]], type_of_chord: str) -> str:
        """Identifies which chord or scale a user is playing"""
        for chord in get_chords():
            if self.relative == specific_chord(chord):
                return f'{self.root_note()} {chord} {type_of_chord}'
        
        possible_inversions: dict[str, list[int]] = self.inverter()
        inversions: str = ""
        for inversion in possible_inversions:
            for chord in get_chords():
                if possible_inversions.get(inversion) == specific_chord(chord):
                    inversions += f'{inversion} Inversion {self.root_note(inversion)} {chord} {type_of_chord}, '
        if inversions != "":
            return inversions
        return "Not a chord or scale"
    
    def tetrads(self) -> str:
        sixths: str = self.identify(self.theory.get_sixths, self.theory.get_specific_sixth, "Sixth")
        sevenths: str = self.identify(self.theory.get_sevenths, self.theory.get_specific_seventh, "Seventh")
        if sixths != "Not a chord or scale":
            if "Inversion" in sixths and "Inverison" not in sevenths and sevenths != "Not a chord or scale":
                return sevenths
            return sixths
        elif sevenths != "Not a chord or scale":
            return sevenths
        return "Not a chord or scale" 
    
    def identifyingMode(self) -> str:
        """Identifies which function to call based on the number of notes being pressed"""
        match len(self.relative):
            case 1 | 2:
                if len(self.notes) == 2:
                    return self.intervals()
                return self.root_note()
            case 3:
                return f'{self.identify(self.theory.get_triads, self.theory.get_specific_triad, "Triad")}'
            case 4:
                return f'{self.tetrads()}'
            case 7:
                if len(self.notes) == 8:
                    return f'{self.identify(self.theory.get_scales, self.theory.get_specific_scale, "Scale")}'
                return "No Scale"
            case _:
                return "Could not identify"
    
    def clear_inversions(self) -> None:
        """Clears all inversions"""
        for inversion in self.inversions:
            self.chord_inversions[inversion] = []

    def inverter(self) -> dict[str, list[int]]:
        """Gets all inversions of a given chord"""
        self.chord_inversions[""] = self.relative
        relative_copy: list[int] = self.relative.copy()
        rel_copy_len: int = len(relative_copy)
        front: int = 0
        for i in range(rel_copy_len-1):
            relative_copy.append(relative_copy[0]+12)
            relative_copy.remove(relative_copy[0])
            front = relative_copy[0]
            for j in range(rel_copy_len):
                relative_copy[j] -= front
            self.chord_inversions[self.inversions[:rel_copy_len-1][rel_copy_len-2-i]] = relative_copy.copy()
        return self.chord_inversions

    def notes_handler(self, message: mido.Message) -> None:
        """Gets relative and absolute notes and calls the appropriate functions"""
        message_note: int = message.note
        message_velocity: int = message.velocity
        
        if message_velocity != 0:
            self.notes.append(message_note)
        elif len(self.notes) != 0:
            self.notes.remove(message_note)
        self.notes.sort()

        if len(self.notes) == 0:
            print()
        else:
            print(self.notes, "Notes")

        to_add: int = 0
        for note in self.notes:
            to_add = (note-self.notes[0]) % 12
            if to_add not in self.relative:
                self.relative.append(to_add)
        self.relative.sort()

        if len(self.relative) != 0:
            print(self.relative, "Relative")

        if len(self.notes) != 0 and len(self.notes) <= 8:
            print(self.identifyingMode())
        
        self.relative.clear()
        self.clear_inversions()
        print()

    def connect(self, device: str) -> None:
        """Connect to a given midi keyboard"""
        with mido.open_input(device, callback=self.notes_handler) as inport:
            print(f'Using {inport}')
            if input() == 'q':
                print("Quitting")
                exit()