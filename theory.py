class Theory():
    def __init__(self) -> None:
        self.root_notes: list[str] = [
            "A",
            "A♯ or B♭",
            "B",
            "C",
            "C♯ or D♭",
            "D",
            "D♯ or E♭",
            "E",
            "F",
            "F♯ or G♭",
            "G",
            "G♯ or A♭"
        ]
        self.scales: dict[str, list[int]] = {
            "Major": [0,2,4,5,7,9,11],
            "Natural Minor": [0,2,3,5,7,8,10],
            "Harmonic Minor": [0,2,3,5,7,8,11],
            "Melodic Minor Ascending": [0,2,3,5,7,9,11],
            "Melodic Minor Descending": [0,2,4,5,7,9,10]
        }
        self.modes: dict[str, list[int]] = {
            "Ionian": [2,2,1,2,2,2,1],
            "Dorian": [2,1,2,2,2,1,2],
            "Phrygian": [1,2,2,2,1,2,2],
            "Lydian": [2,2,2,1,2,2,1],
            "Mixolydian": [2,2,1,2,2,1,2],
            "Aeolian": [2,1,2,2,1,2,2],
            "Locrian": [1,2,2,1,2,2,2]
        }
        self.intervals: list[str] = [
            "Perfect Octave",
            "Minor Second",
            "Major Second",
            "Minor Third",
            "Major Third",
            "Perfect Fourth",
            "Tritone",
            "Perfect Fifth",
            "Minor Sixth",
            "Major Sixth",
            "Minor Seventh",
            "Major Seventh"
        ]
        self.triads: dict[str, list[int]] = {
            "Major": [0,4,7],
            "Minor": [0,3,7],
            "Augmented": [0,4,8],
            "Diminished": [0,3,6],
            "Suspended Second": [0,2,7],
            "Suspended Fourth": [0,5,7],
            "Minor Augmented Fifth": [0,3,8],
            "Major Diminished Fifth": [0,4,6]
        }
        self.sixths: dict[str, list[int]] = {
            "Major": [0,4,7,9],
            "Minor": [0,3,7,9],
            "Major Augmented Fifth": [0,4,8,9],
            "Minor Augmented Fifth": [0,3,8,9]
        }
        self.sevenths: dict[str, list[int]] = {
            "Major": [0,4,7,11],
            "Dominant": [0,4,7,10],
            "Augmented": [0,4,8,10],
            "Dominant Flat Fifth": [0,4,6,10],
            "Minor Major": [0,3,7,11],
            "Minor": [0,3,7,10],
            "Minor Augmented Fifth": [0,3,8,10],
            "Half Diminished": [0,3,6,10],
            "Diminished": [0,3,6,9],
            "Dominant Suspended Second": [0,2,7,10],
            "Dominant Suspended Fourth": [0,5,7,10]
        }
        self.additions: dict[int, str] = {
            13: "Flat Ninth",
            14: "Ninth",
            15: "Sharp Ninth",
            17: "Eleventh",
            18: "Sharp Eleventh",
            20: "Flat Thirteenth",
            21: "Thirteenth",
            22: "Sharp Thirteenth"
        }
    
    def get_root_notes(self) -> list[str]:
        return self.root_notes

    def get_specific_scale(self, scale: str) -> list[int]:
        return self.scales[scale]

    def get_scales(self) -> dict[str, list[int]]:
        return self.scales
    
    def get_modes(self) -> dict[str, list[int]]:
        return self.modes
    
    def get_intervals(self) -> list[str]: 
        return self.intervals

    def get_specific_triad(self, triad: str) -> list[int]:
        return self.triads[triad]
    
    def get_triads(self) -> dict[str, list[int]]:
        return self.triads
    
    def get_specific_sixth(self, sixth: str) -> list[int]:
        return self.sixths[sixth]

    def get_sixths(self) -> dict[str, list[int]]:
        return self.sixths
    
    def get_specific_seventh(self, seventh: str) -> list[int]:
        return self.sevenths[seventh]

    def get_sevenths(self) -> dict[str, list[int]]:
        return self.sevenths
    
    def get_specific_addition(self, addition: int) -> str:
        return self.additions[addition]
    
    def get_additions(self) -> dict[int, str]:
        return self.additions