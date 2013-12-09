#Based on http://pythonvision.org/basic-tutorial

import argparse
import interpret_features as interpret
import identify_features as identify
import util
from PIL import Image

#Return the arguments
def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Import data from an image')
    parser.add_argument('-i', dest = 'input_file', 
            help='the image to import', default='data/sample_chart_easy.png')
    return vars(parser.parse_args())

if __name__ == "__main__":
    args = initialize_argument_parser()
    input_file = args["input_file"]
    image=util.imread(input_file)
    #util.display_graph(image)
    #print image
    image_labels, feature_count = identify.identify_features(image)
    print 'feature_count:', feature_count
    feature_types = identify.identify_feature_types(image, image_labels, feature_count)
    image_analyzer = interpret.analyzer(identify.nongrayscale_raw(image), image_labels, feature_types)
    #test_image = Image.open('data/sample_chart.png')
    test_image = util.numpy_to_pil(image)
    box = (200,5,300,50)
    #print util.ocr_cropped(test_image, box)
    #print util.ocr(test_image)

    #util.display_graph(image_analyzer.get_data_centers())
    #print image_analyzer.get_objects()
    #print image_analyzer.get_data_centers()
