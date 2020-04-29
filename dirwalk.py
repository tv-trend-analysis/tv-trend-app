import os


def showslist():
    shows = []
    for r, d, files in os.walk("data"):
        for filename in files:
            if filename.endswith(".csv"):
                filename = filename.rsplit('.', 1)[0]
                shows.append(filename)

    return shows


