#Based on http://pythonvision.org/basic-tutorial

import argparse
import mahotas
import interpret_features as interpret
import identify_features as identify

#Return the arguments
def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Import data from an image')
    parser.add_argument('-i', dest = 'input_file', 
            help='the image to import', default='data/sample_chart_easy.png')
    return vars(parser.parse_args())

if __name__ == "__main__":
    args = initialize_argument_parser()
    input_file = args["input_file"]
    image=mahotas.imread(input_file)
    image_labels, feature_count = identify.identify_features(image)
    feature_types = identify.identify_feature_types(image, image_labels, feature_count)
    print interpret.interpret_feature(
            identify.nongrayscale_raw(image), image_labels, 1, 'data_point')