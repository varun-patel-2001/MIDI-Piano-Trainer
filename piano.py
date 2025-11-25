from theory import Theory
from typing import Callable
import mido

class Piano():
    def __init__(self) -> None:
        self.theory: Theory = Theory()
        self.notes: list[int] = []
        self.relative: list[int] = []
        # self.inversions: list[str] = [
        #     "1st",
        #     "2nd",
        #     "3rd",
        #     "4th",
        #     "5th",
        #     "6th"
        # ]
        # self.chord_inversions: dict[str, list[int]] = {
        #     "1st": [],
        #     "2nd": [],
        #     "3rd": [],
        #     "4th": [],
        #     "5th": [],
        #     "6th": []
        # }
        # self.identifying: bool = False
        # self.testing: bool = False
        # self.selection: str = input("What type (Identifying or Testing, I/i or T/t)?: ")
        # if self.selection in 'Ii':
        #     self.identifying = True
        # elif self.selection in 'Tt':
        #     self.testing = True
    
    # def root_note(self, inversion: str = "") -> str:
    def root_note(self) -> str:
        """
        Returns the root note for intervals/chords/scales

        This works by getting the lowest played note and subtracting A(0) from it
        A(0) is the lowest key in an 88 key piano and is the MIDI number 22 when the note is played
        Modulo 12 is there because there are 12 keys in an octave
        """
        root_notes: list[str] = self.theory.get_root_notes()
        # if inversion != "":
        #     root_index = -1 * (self.inversions.index(inversion)+1)
        return root_notes[(self.notes[0] - 21) % 12]

    def intervals(self) -> str:
        """Returns the intervals between any 2 notes"""
        intervals: list[str] = self.theory.get_intervals()
        return intervals[(self.notes[1]-self.notes[0])%12]
    
    # def clear_inversions(self) -> None:
    #     """Clears all inversions"""
    #     for inversion in self.inversions:
    #         self.chord_inversions[inversion] = []

    # def inverter(self, chord: list[int] | None = None) -> dict[str, list[int]]:
    #     """Gets all inversions of a given chord"""
    #     # self.chord_inversions[""] = self.relative
    #     relative_copy: list[int] = []
    #     if chord:
    #         relative_copy = chord.copy()
    #     else:
    #         relative_copy = self.relative.copy()
    #     rel_copy_len: int = len(relative_copy)
    #     front: int = 0
    #     for i in range(rel_copy_len-1):
    #         relative_copy.append(relative_copy[0]+12)
    #         relative_copy.remove(relative_copy[0])
    #         relative_copy.sort()
    #         front = relative_copy[0]
    #         for j in range(rel_copy_len):
    #             relative_copy[j] -= front
    #         self.chord_inversions[self.inversions[:rel_copy_len-1][rel_copy_len-2-i]] = relative_copy.copy()
    #     return self.chord_inversions

    # def indentify_inversion(self, get_chords: Callable[[], dict[str, list[int]]], specific_chord: Callable[[str], list[int]], type_of_chord: str, base_chord: list[int]) -> str:
    #     """Helper function that is used to identify inversions of a chord"""
    #     possible_inversions: dict[str, list[int]] = self.inverter(base_chord)
    #     inversions: str = ""
    #     for inversion in possible_inversions:
    #         for chord in get_chords():
    #             if possible_inversions.get(inversion) == specific_chord(chord):
    #                 inversions += f'{inversion} Inversion {self.root_note(inversion)} {chord} {type_of_chord}, '
    #     return inversions
    
    # def identify_complex(self, get_chords: Callable[[], dict[str, list[int]]], specific_chord: Callable[[str], list[int]], type_of_chord: str, base_chord: list[int]) -> str:
    #     """Can identify the base chord in an addition or omittion chord, e.g. the C major component in C Major add 9"""
    #     for chord in get_chords():
    #         if base_chord == specific_chord(chord):
    #             return f'{self.root_note()} {chord} {type_of_chord}'
    #     return "Not a chord"

    def identify_helper(self, chord: str, type_of_chord: str) -> str:
        """Helper method for identify(), useful for omit chords"""
        if "*" in chord:
            return f'{self.root_note()} {chord.replace("*",type_of_chord)}'
        if type_of_chord == "Omittion":
            return f'{self.root_note()} {chord}'
        return f'{self.root_note()} {chord} {type_of_chord}'

    def identify(
        self, 
        get_chords: Callable[[], dict[str, list[int]]], 
        specific_chord: Callable[[str], list[int]], 
        type_of_chord: str, 
        base_chord: list[int] | None = None
        ) -> str:
        """Identifies which chord or scale a user is playing"""
        if not base_chord:
            base_chord = self.relative
        for chord in get_chords():
            if base_chord == specific_chord(chord):
                return self.identify_helper(chord, type_of_chord)
        if type_of_chord == "Scale":
            return "Not a Scale"
        # inversions: str = self.indentify_inversion(get_chords, specific_chord, type_of_chord, base_chord)
        # if inversions != "":
        #     return inversions
        return "Not a chord"
    
    def add_chords(self, base_length: int, added_notes: list[int] | None = None) -> list[str]:
        """Identifies the added notes in the chord"""
        addition_notes: dict[int, str] = self.theory.get_additions()
        additions: list[str] = []
        if not added_notes:
            added_notes = self.relative[base_length:]
        for note in added_notes:
            if note in addition_notes:
                additions.append(f'{self.theory.get_specific_addition(note)}, ')
        return additions

    def omit_one_note(self, chord: list[int] | None) -> str:
        """Identifies if a chord base has one omitted note"""
        return self.identify(self.theory.get_omit_one_note, self.theory.get_specific_omit_one_note, "Omittion", chord)

    def omit_two_notes(self, chord: list[int] | None) -> str:
        """Identifies if a chord base has two omitted notes"""
        return self.identify(self.theory.get_omit_two_notes, self.theory.get_specific_omit_two_notes, "Omittion", chord)
            
    def omittion_helper(self, omitted_one_note: list[int], omitted_two_notes: list[int], type_of_chord: str) -> str:
        """Helper function to return if a base has 0,1, or 2 omittions"""
        possible_omittion_one_note: str = self.omit_one_note(omitted_one_note)
        possible_omittion_two_note: str = self.omit_two_notes(omitted_two_notes)
        if possible_omittion_two_note != "Not a chord" and type_of_chord in possible_omittion_two_note:
            return possible_omittion_two_note
        if possible_omittion_one_note != "Not a chord" and type_of_chord in possible_omittion_one_note:
            return possible_omittion_one_note
        return "Not a chord"

    def possible_sixth_chord(self, chord: list[int], omitted_one_note: list[int], omitted_two_notes: list[int]) -> str:
        """Identifies if a given chord is a sixth chord with or without omittions"""
        omittion: str = self.omittion_helper(omitted_one_note, omitted_two_notes, "Sixth")
        if omittion != "Not a chord":
            return omittion
        return self.identify(self.theory.get_sixths, self.theory.get_specific_sixth, "Sixth", chord)

    def possible_seventh_chord(self, chord: list[int], omitted_one_note: list[int], omitted_two_notes: list[int]) -> str:
        """Identifies if a given chord is a seventh chord with or without omittions"""
        omittion: str = self.omittion_helper(omitted_one_note, omitted_two_notes, "Seventh")
        if omittion != "Not a chord":
            return omittion
        return self.identify(self.theory.get_sevenths, self.theory.get_specific_seventh, "Seventh", chord)
    
    def triads_two_omittions(self, chord: list[int]) -> str:
        """
        Used by triads() to see if subsequence is a chord with omitted notes
        Useful for chords such as Major Seventh no Third, Fifth add Eleventh
        """
        two_omittions: str = self.omit_two_notes(chord[:2])
        addition: str = ""
        additions: dict[int, str] = self.theory.get_additions()

        if two_omittions != "Not a chord" and chord[2] in additions:
            addition= self.theory.get_specific_addition(chord[2])
            if "Seventh" in two_omittions and addition == "Ninth":
                two_omittions = two_omittions.replace("Seventh",addition)
            else:
                two_omittions += f' add {self.theory.get_specific_addition(chord[2])}'
        return two_omittions

    def triads(self, chord: list[int] | None = None) -> str:
        """Identifies which type of chord the specific triad is"""
        if not chord:
            chord = self.relative
        
        two_omittions: str = self.triads_two_omittions(chord)
        if two_omittions != "Not a chord":
            return two_omittions
        
        one_omittion: str = self.omit_one_note(chord)
        if one_omittion != "Not a chord":
            return one_omittion
        
        return self.identify(self.theory.get_triads, self.theory.get_specific_triad, "Triad", chord)

    def triads_case(self, possible_sixth: str, possible_seventh: str, base_triad: str, chord: list[int]) -> str:
        """Identifies chords that are a triad and additions"""
        triad_additions: str = ""
        if possible_sixth == "Not a chord" and possible_seventh == "Not a chord" and base_triad != "Not a chord":
            additions: list[str] = self.add_chords(3, chord[3:])
            if len(additions) == 0:
                return "Not a chord"
            for addition in additions:
                triad_additions += addition
            return f'{base_triad} add {triad_additions[:-2]}'
        return "Not a chord"
    
    def tetrads_additions(self, possible_sixth: str, possible_seventh: str, chord: list[int]) -> list[str]:
        """Gets the additions in a tetrad"""
        if "," in possible_seventh or "," in possible_sixth:
            return self.add_chords(2, chord[2:])
        if "no" in possible_seventh or "no" in possible_sixth:
            return self.add_chords(3, chord[3:])
        return self.add_chords(4, chord[4:])

    def sixths_case(self, possible_sixth: str, tetrads_additions: list[str]) -> str:
        """Handles the sixths case, with or without additions"""
        sixth_out: str = ""
        if "Ninth, " in tetrads_additions:
            possible_sixth = possible_sixth.replace("Sixth","Sixth/Ninth")
            tetrads_additions.remove("Ninth, ")
        if "Eleventh, " in tetrads_additions and "Sixth/Ninth" in possible_sixth:
            possible_sixth = possible_sixth.replace("Sixth/Ninth","Sixth/Eleventh")
            tetrads_additions.remove("Eleventh, ")
        if len(tetrads_additions) != 0:
            sixth_out += f'{possible_sixth} add '
            for addition in tetrads_additions:
                sixth_out += addition
            sixth_out = sixth_out[:-2]
        else:
            sixth_out = possible_sixth
        return sixth_out
    
    def sevenths_case(self, possible_seventh: str, tetrads_additions: list[str]) -> str:
        """Handles the sevenths case, with or without additions"""
        seventh_out: str = ""
        if "Ninth, " in tetrads_additions:
            possible_seventh = possible_seventh.replace("Seventh","Ninth")
            tetrads_additions.remove("Ninth, ")
        if "Eleventh, " in tetrads_additions and "Ninth" in possible_seventh:
            possible_seventh = possible_seventh.replace("Ninth","Eleventh")
            tetrads_additions.remove("Eleventh, ")
        if "Thirteenth, " in tetrads_additions and "Eleventh" in possible_seventh:
            possible_seventh = possible_seventh.replace("Eleventh","Thirteenth")
            tetrads_additions.remove("Thirteenth, ")
        if len(tetrads_additions) != 0:
            seventh_out += f'{possible_seventh} add '
            for addition in tetrads_additions:
                seventh_out += addition
            seventh_out = seventh_out[:-2]
        else:
            seventh_out = possible_seventh
        return seventh_out

    def tetrads(self, chord: list[int] | None = None) -> str:
        """Identifies which type of chord the specific tetrad is"""
        if not chord:
            chord = self.relative
        
        base_triad: str = self.triads(chord[:3])

        possible_sixth: str = self.possible_sixth_chord(chord[:4], chord[:3], chord[:2])

        possible_seventh: str = self.possible_seventh_chord(chord[:4], chord[:3], chord[:2])
        
        ## Triads Case
        triads_case = self.triads_case(possible_sixth, possible_seventh, base_triad, chord)
        if triads_case != "Not a chord":
            return triads_case
        
        ## Add notes to tetrads
        tetrads_additions: list[str] = self.tetrads_additions(possible_sixth, possible_seventh, chord)

        ## Sixths Case
        if possible_sixth != "Not a chord":
            return self.sixths_case(possible_sixth, tetrads_additions)
        
        ## Sevenths Case
        if possible_seventh != "Not a chord":
            return self.sevenths_case(possible_seventh, tetrads_additions)

        return "Could not identify"

    def identifyingMode(self) -> str:
        """Identifies which function to call based on the number of notes being pressed"""
        match len(self.relative):
            case 1:
                return self.root_note()
            case 2:
                return self.intervals()
            case 3:
                return self.triads()
            case 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12:
                return self.tetrads()
            case _:
                return "Could not identify"
    
    def notes_handler(self, message: mido.messages.messages.Message) -> None:
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
            to_add = (note-self.notes[0]) % 24
            if to_add not in self.relative:
                self.relative.append(to_add)
        self.relative.sort()

        if len(self.relative) != 0:
            print(self.relative, "Relative")

        if len(self.notes) != 0:
            print(self.identifyingMode())
        
        self.relative.clear()
        # self.clear_inversions()
        print()

    def connect(self, device: str) -> None:
        """Connect to a given midi keyboard"""
        with mido.open_input(device, callback=self.notes_handler) as inport:
            print(f'Using {inport}')
            if input() == 'q':
                print("Quitting")
                exit()