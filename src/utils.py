def midi_to_pitch(note):
    return (2 ** ((note - 69) / 12)) * 440


note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
note_names = note_names * 10
for i, name in zip(range(12, len(note_names)), note_names):
    print(name, midi_to_pitch(i))
