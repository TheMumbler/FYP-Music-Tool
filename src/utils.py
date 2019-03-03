def midi_to_pitch(note, tuning=440):
    """Takes a midi number and returns the relative frequency. Has a tuning parameter with defaults to 440"""
    return (2 ** ((note - 69) / 12)) * tuning


def note_pitch_midi(tuning=440):
    """Creates a dictionary with has information on every note from C0 to B8 such as midi value and pitch value"""
    note_info = {}
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_names = note_names * 10
    for midi_num, name in zip(range(12, len(note_names)), note_names):
        # print(name + str((i//12)-1), midi_to_pitch(i))
        # print(midi_num)
        note_info[name + str((midi_num // 12) - 1)] = [midi_to_pitch(midi_num, tuning), midi_num]
    return note_info


d = note_pitch_midi()
# for key in d:
#     print(key, d[key])
