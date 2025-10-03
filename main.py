import mido
import json
import rtmidi
import time

class Piano():
    def __init__(self) -> None:
        with open('theory.json','r') as theory_file:
            self.theory: dict = json.load(theory_file)
        self.notes: list[int] = []
        self.relative: list[int] = []
        self.inversions: list[str] = [
            "First",
            "Second",
            "Third",
            "Fourth",
            "Fifth",
            "Sixth"
        ]
        self.chord_inversions: dict = {
            "First": [],
            "Second": [],
            "Third": [],
            "Fourth": [],
            "Fifth": [],
            "Sixth": []
        }
        self.root: list[str] = []
        self.identifying: bool = False
        self.testing: bool = False
        self.selection: str = input("What type (Identifying or Testing, I/i or T/t)?: ")
        if self.selection in 'Ii':
            self.identifying = True
        elif self.selection in 'Tt':
            self.testing = True
    
    def root_note(self) -> str:
        if len(self.notes) > 0:
            for i in self.theory["Midi Conversion"].keys():
                if (self.notes[0] - self.theory["Midi Conversion"][i]) % 12 == 0 and i not in self.root:
                    self.root.append(i)
        if len(self.root) > 2:
            print(self.root)
        if len(self.root) == 1:
            return self.root[0]
        return f'{self.root[0]} or {self.root[1]}'

    def clear_root(self) -> None:
        self.root.clear()

    def clear_inversions(self) -> None:
        for i in self.inversions:
            self.chord_inversions[i] = []

    def intervals(self) -> None:
        # Could change this if statement or remove
        if len(self.relative) == 1 and len(self.notes) == 2 and self.notes[1]-self.notes[0] == 12:
            print(self.root_note(), "Perfect Octave")
        else:
            for i in self.theory["Intervals"]["Simple"].keys():                
                if self.relative[1]-self.relative[0] == self.theory["Intervals"]["Simple"][i]:
                    print(self.root_note(), self.relative, self.theory["Intervals"]["Simple"][i], i)
        self.clear_root()

    def triads(self) -> None:
        for i in self.theory["Chords"]["Triads"].keys():
            for j in self.theory["Chords"]["Triads"][i].keys():
                if self.relative == self.theory["Chords"]["Triads"][i][j]:
                    if j != "Root":
                        print(self.root_note(), j, "Inversion", i, "Triad\t", self.notes, self.relative)
                    else:
                        print(self.root_note(), j, i, "Triad\t", self.notes, self.relative)
        self.clear_root()

    def tetrads(self) -> None:
        for i in self.theory["Chords"]["Tetrads"]["Sevenths"].keys():
            for j in self.theory["Chords"]["Tetrads"]["Sevenths"][i].keys():
                if self.relative == self.theory["Chords"]["Tetrads"]["Sevenths"][i][j]:
                    if j != "Root":
                        print(self.root_note(), j, "Inversion", i, self.notes, self.relative)
                    else:
                        print(self.root_note(), j, i, self.notes, self.relative)
        self.clear_root()

    def scales(self) -> None:
        if len(self.notes) == 8 and self.notes[7]-self.notes[0] == 12:
            for i in self.theory["Scales"].keys():
                if self.relative == self.theory["Scales"][i]:
                    print(self.root_note(), i, "Scale")
        self.clear_root()
        
    def inverter(self, relative):
        self.copy: list[int] = self.relative.copy()
        self.front: int = 0
        for i in range(len(self.copy)-1):
            self.copy.append(self.copy[0]+12)
            self.copy.remove(self.copy[0])
            self.front = self.copy[0]
            for j in range(len(self.copy)):
                self.copy[j] -= self.front
            self.chord_inversions[self.inversions[i]] = self.copy.copy()
        print(self.chord_inversions)

    def identifyingMode(self) -> None:
        if len(self.notes) == 8:
            self.scales()
        match len(self.relative):
            case 2:
                self.intervals()
            case 3:
                self.triads()
            case 4:
                self.tetrads()
            # case 7:
            #     self.scales()
    
    def notes_handler(self, message: mido.Message) -> None:
        message_note = message.note
        message_velocity = message.velocity
        if message_velocity != 0:
            self.notes.append(message_note)
        elif len(self.notes) != 0:
            self.notes.remove(message_note)
        self.notes.sort()
        if len(self.notes) == 0:
            print()
        else:
            print(self.notes, "Notes")

        self.to_add: int = 0
        for i in self.notes:
            # if (i-self.notes[0])%12 == 0 and i-self.notes[0] != 0 and len(notes) == 2:
            #     self.to_add = 12
            # else:
            self.to_add = (i-self.notes[0]) % 12
            if self.to_add not in self.relative:
                self.relative.append(self.to_add)
        self.relative.sort()
        print(self.relative, "Relative")

        if self.identifyingMode and len(self.notes) <= 8:
            self.identifyingMode()
            if len(self.relative) <= 8:
                self.inverter(self.relative)
        self.relative.clear()
        self.clear_inversions()
        print()
        print(message_note, message_velocity)

def main() -> None:
    device: str = 'Recital Play:Recital Play MIDI 1 28:0'
    piano: Piano = Piano()
    print(mido.get_input_names())
    with mido.open_input(device, callback=piano.notes_handler) as inport:
        if input()=='q':
            print("Quitting")
            exit()

if __name__ == "__main__":
    main()