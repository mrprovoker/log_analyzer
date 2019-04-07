from sklearn.externals import joblib
import pickle as pickle
import argparse

# https://github.com/rory/apache-log-parser
import apache_log_parser

arguments = None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', required=True, choices=('apache', 'nginx'), help="Log type")
    parser.add_argument('-f', '--format', required=True, help="Log format")
    parser.add_argument('-p', '--path', required=True, help="Log file path")
    return parser.parse_args()


def analyze(data):
    classifier = joblib.load("./class.dmp")
    vectorizer = pickle.load(open("vect.pk", "rb"))

    transform_data = vectorizer.transform(data)
    predict = classifier.predict(transform_data)

    return predict


def apache():
    url_for_analyze = []

    line_parser = apache_log_parser.make_parser(arguments.format)
    file = open(arguments.path)
    file_lines = file.readlines()

    for line in file_lines:
        log_line = line_parser(line)
        url_for_analyze.append(log_line['request_url'])

    result = analyze(url_for_analyze)

    print('Found bad url:')
    for i in range(len(result)):
        r = result[i]

        if r == 1:
            print(url_for_analyze[i])


if __name__ == '__main__':
    arguments = parse_args()

    if arguments.type == 'apache':
        apache()

