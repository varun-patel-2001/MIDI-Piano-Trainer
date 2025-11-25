from typing import Callable
from itertools import combinations
import unittest
from unittest.mock import patch
from piano import Piano

class TestPiano(unittest.TestCase):
    def setUp(self):
        self.piano= Piano()

    def simple_helper(self, chord: str, type_of_chord: str):
        if type_of_chord != "":
            if "*" in chord:
                return f'C {chord.replace("*",type_of_chord)}'
            return f'C {chord} {type_of_chord}'
        return f'C {chord}'

    def simple(self, function: Callable[[list[int] | None], str], chords: dict[str, list[int]], type_of_chord: str):
        out_string: str = ""
        for chord in chords:
            with patch.object(Piano, 'root_note', return_value='C'), self.subTest(chord = chord):
                out_string = self.simple_helper(chord, type_of_chord)
                self.assertEqual(function(chords.get(chord)), out_string)
    
    def out_string(self, chord: str, out_chord: str, added_notes: list[str], addition_string: str):
        if len(added_notes) != 0:
            if "*" in chord:
                return f'C {chord.replace("*",out_chord)} add {addition_string[:-2]}'
            return f'C {chord} {out_chord} add {addition_string[:-2]}'
        
        if "*" in chord:
            return f'C {chord.replace("*",out_chord)}'
        return f'C {chord} {out_chord}'

    def add_notes_naming(self, addition: tuple[int, ...], additions: dict[int, str], chord_string: str):
        added_notes: list[str] = []
        for note in addition:
            added_notes.append(f'{additions.get(note)}, ')
        out_chord = chord_string
        if "Ninth, " in added_notes:
            if chord_string == "Seventh":
                out_chord = "Ninth"
            elif chord_string == "Sixth":
                out_chord = "Sixth/Ninth"
            if chord_string != "Triad":
                added_notes.remove("Ninth, ")
        if "Eleventh, " in added_notes:
            if out_chord == "Ninth":
                out_chord = "Eleventh"
            elif out_chord == "Sixth/Ninth":
                out_chord = "Sixth/Eleventh"
            if out_chord not in ["Triad","Sixth","Seventh"]:
                added_notes.remove("Eleventh, ")
        if "Thirteenth, " in added_notes and out_chord == "Eleventh":
            out_chord = "Thirteenth"
            added_notes.remove("Thirteenth, ")
        
        return out_chord, added_notes

    def combinator(
        self, 
        function: Callable[[list[int] | None], str], 
        chord: str, 
        chords: dict[str, list[int]], 
        additions: dict[int, str], 
        chord_string: str, 
        number_of_additions: int
        ):
        addition_string: str = ""
        out_chord: str = ""
        out_string: str = ""
        for addition in combinations(additions, number_of_additions):
            added_chord: list[int] = chords[chord].copy()
            added_chord += list(addition)
            out_chord, added_notes = self.add_notes_naming(addition, additions, chord_string)
            for added_note in added_notes:
                addition_string += added_note
            with self.subTest(chord = chord, addition = addition):
                out_string = self.out_string(chord, out_chord, added_notes, addition_string)
                self.assertEqual(function(added_chord), out_string, f'{added_chord} {added_notes} {out_chord}')
            addition_string = ""
            out_string = ""
            out_chord = ""
            added_notes.clear()

    def add_notes(
        self, 
        function: Callable[[list[int] | None], str], 
        chords: dict[str, list[int]], 
        additions: dict[int, str], 
        chord_string: str, 
        number_of_additions: int
        ):
        with patch.object(Piano, 'root_note', return_value='C'):
            for chord in chords:
                self.combinator(function, chord, chords, additions, chord_string, number_of_additions)


    def test_triads(self):
        triads: dict[str, list[int]] = {
            "Major": [0,4,7],
            "Minor": [0,3,7],
            "Augmented": [0,4,8],
            "Diminished": [0,3,6],
            "Suspended Second": [0,2,7],
            "Suspended Fourth": [0,5,7],
            "Minor * Augmented Fifth": [0,3,8],
            "Major * Diminished Fifth": [0,4,6]
        }
        self.simple(self.piano.triads, triads, "Triad")

    def test_sixths(self):
        sixths: dict[str, list[int]] = {
            "Major": [0,4,7,9],
            "Minor": [0,3,7,9],
            "Major * Augmented Fifth": [0,4,8,9],
            "Minor * Augmented Fifth": [0,3,8,9]
        }
        self.simple(self.piano.tetrads, sixths, "Sixth")
    
    def test_sevenths(self):
        sevenths: dict[str, list[int]] = {
            "Major": [0,4,7,11],
            "Dominant": [0,4,7,10],
            "Dominant * Flat Fifth": [0,4,6,10],
            "Minor Major": [0,3,7,11],
            "Minor": [0,3,7,10],
            "Minor * Augmented Fifth": [0,3,8,10],
            "Half Diminished": [0,3,6,10],
            "Diminished": [0,3,6,9],
            "Augmented": [0,4,8,10],
            "Dominant * Suspended Second": [0,2,7,10],
            "Dominant * Suspended Fourth": [0,5,7,10]
        }
        self.simple(self.piano.tetrads, sevenths, "Seventh")
    
    def test_triad_add_notes(self):
        triads: dict[str, list[int]] = {
            "Major": [0,4,7],
            "Minor": [0,3,7],
            "Augmented": [0,4,8],
            "Diminished": [0,3,6],
            "Suspended Second": [0,2,7],
            "Suspended Fourth": [0,5,7],
            "Minor * Augmented Fifth": [0,3,8],
            "Major * Diminished Fifth": [0,4,6]
        }
        additions: dict[int, str] = {
            13: "Flat Ninth",
            14: "Ninth",
            15: "Sharp Ninth",
            17: "Eleventh",
            18: "Sharp Eleventh",
            20: "Flat Thirteenth",
            21: "Thirteenth",
            22: "Sharp Thirteenth"
        }
        for number_of_additions in range(1,len(additions)+1):
            self.add_notes(self.piano.tetrads, triads, additions, "Triad", number_of_additions)
    
    def test_sixths_add_notes(self):
        sixths: dict[str, list[int]] = {
            "Major": [0,4,7,9],
            "Minor": [0,3,7,9],
            "Major * Augmented Fifth": [0,4,8,9],
            "Minor * Augmented Fifth": [0,3,8,9]
        }
        additions: dict[int, str] = {
            13: "Flat Ninth",
            14: "Ninth",
            15: "Sharp Ninth",
            17: "Eleventh",
            18: "Sharp Eleventh",
            20: "Flat Thirteenth",
            21: "Thirteenth",
            22: "Sharp Thirteenth"
        }
        for number_of_additions in range(1,len(additions)+1):
            self.add_notes(self.piano.tetrads, sixths, additions, "Sixth", number_of_additions)

    def test_sevenths_add_notes(self):
        sevenths: dict[str, list[int]] = {
            "Major": [0,4,7,11],
            "Dominant": [0,4,7,10],
            "Dominant * Flat Fifth": [0,4,6,10],
            "Minor Major": [0,3,7,11],
            "Minor": [0,3,7,10],
            "Minor * Augmented Fifth": [0,3,8,10],
            "Half Diminished": [0,3,6,10],
            "Diminished": [0,3,6,9],
            "Augmented": [0,4,8,10],
            "Dominant * Suspended Second": [0,2,7,10],
            "Dominant * Suspended Fourth": [0,5,7,10]
        }
        additions: dict[int, str] = {
            13: "Flat Ninth",
            14: "Ninth",
            15: "Sharp Ninth",
            17: "Eleventh",
            18: "Sharp Eleventh",
            20: "Flat Thirteenth",
            21: "Thirteenth",
            22: "Sharp Thirteenth"
        }
        for number_of_additions in range(1,len(additions)+1):
            self.add_notes(self.piano.tetrads, sevenths, additions, "Seventh", number_of_additions)
    
    def test_base_one_omittion(self):
        base_omittions_one_note: dict[str, list[int]] = {
            "Diminished Seventh no Flat Third": [0,6,9],
            "Half Diminished Seventh no Flat Third": [0,6,10],
            "Minor Seventh no Fifth": [0,3,10],
            "Dominant Seventh no Third": [0,7,10],
            "Dominant Seventh no Fifth": [0,4,10],
            "Augmented Seventh no Third": [0,8,10],
            "Dominant Seventh Suspended Fourth no Fifth": [0,5,10],
            "Minor Major Seventh no Fifth": [0,3,11],
            "Major Seventh no Fifth": [0,4,11],
            "Major Seventh no Third": [0,7,11],
            "Major Sixth no Fifth": [0,4,9]
        }
        self.simple(self.piano.triads, base_omittions_one_note, "")
    
    def test_base_one_omittion_add_notes(self):
        base_sevenths_omittions_one_note: dict[str, list[int]] = {
            "Diminished * no Flat Third": [0,6,9],
            "Half Diminished * no Flat Third": [0,6,10],
            "Minor * no Fifth": [0,3,10],
            "Dominant * no Third": [0,7,10],
            "Dominant * no Fifth": [0,4,10],
            "Augmented * no Third": [0,8,10],
            "Dominant * Suspended Fourth no Fifth": [0,5,10],
            "Minor Major * no Fifth": [0,3,11],
            "Major * no Fifth": [0,4,11],
            "Major * no Third": [0,7,11]
        }
        base_sixths_omittions_one_note: dict[str, list[int]] = {
            "Major * no Fifth": [0,4,9]
        }
        additions: dict[int, str] = {
            13: "Flat Ninth",
            14: "Ninth",
            15: "Sharp Ninth",
            17: "Eleventh",
            18: "Sharp Eleventh",
            20: "Flat Thirteenth",
            21: "Thirteenth",
            22: "Sharp Thirteenth"
        }
        for number_of_additions in range(1,len(additions)+1):
            self.add_notes(self.piano.tetrads, base_sevenths_omittions_one_note, additions, "Seventh", number_of_additions)
            self.add_notes(self.piano.tetrads, base_sixths_omittions_one_note, additions, "Sixth", number_of_additions)
    
    def test_base_two_omittions_add_single_note(self):
        base_omittions_two_notes: dict[str, list[int]] = {
            "Diminished * no Flat Third, Flat Fifth": [0,9],
            "Dominant * no Third, Fifth": [0,10],
            "Major * no Third, Fifth": [0,11],
        }
        additions: dict[int, str] = {
            13: "Flat Ninth",
            14: "Ninth",
            15: "Sharp Ninth",
            17: "Eleventh",
            18: "Sharp Eleventh",
            20: "Flat Thirteenth",
            21: "Thirteenth",
            22: "Sharp Thirteenth"
        }
        for _ in range(1,len(additions)+1):
            self.add_notes(self.piano.triads, base_omittions_two_notes, additions, "Seventh", 1)

    def test_base_two_omittions_add_multiple_notes(self):
        base_omittions_two_notes: dict[str, list[int]] = {
            "Diminished * no Flat Third, Flat Fifth": [0,9],
            "Dominant * no Third, Fifth": [0,10],
            "Major * no Third, Fifth": [0,11],
        }
        additions: dict[int, str] = {
            13: "Flat Ninth",
            14: "Ninth",
            15: "Sharp Ninth",
            17: "Eleventh",
            18: "Sharp Eleventh",
            20: "Flat Thirteenth",
            21: "Thirteenth",
            22: "Sharp Thirteenth"
        }
        for number_of_additions in range(2,len(additions)+1):
            self.add_notes(self.piano.tetrads, base_omittions_two_notes, additions, "Seventh", number_of_additions)

if __name__ == '__main__':
    unittest.main()