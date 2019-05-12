import py_midicsv


def convert_to_csv(file, output_name):
    """
    This functions converts a midi file to a csv file to help make comparisons easier
    :param file: string
    path to file to be converted
    :param output_name: string
    the chosen name of output file
    """
    csv_string = py_midicsv.midi_to_csv(file)
    with open(output_name, 'w') as file:
        for line in csv_string:
            file.write(line)
