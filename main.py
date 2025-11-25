from piano import Piano

def main() -> None:
    device: str = 'Recital Play:Recital Play MIDI 1 36:0'
    piano: Piano = Piano()
    # print(mido.get_input_names())
    piano.connect(device)

if __name__ == "__main__":
    main()