import docx2txt
from datetime import datetime
from models import Document, Line
from os.path import basename


def get_typist(typist_str):
    return typist_str.replace("\t", "").split(":")[1]


def get_date(date_str):
    dt_str = date_str.replace('\t', '').split(":")[1]
    d = datetime.strptime(dt_str, "%d/%m/%Y")
    return d.date()


def get_mp3_file_name(file_str):
    return file_str.replace("\t", "").split(":")[1]


def get_duration(duration_str):
    times = duration_str.split("\t")[1].lstrip().split(":")
    secs = int(times[0]) * 60 * 60 + int(times[1]) * 60 + 19
    return secs


def load_docx(filename):
    chars = docx2txt.process(filename)
    lines = chars.split("\n")
    return lines


def create_document(user, filename):
    lines = load_docx(filename)
    filename = basename(filename)
    mp3_file = get_mp3_file_name(lines[0])
    duration = get_duration(lines[1])
    file_date = get_date(lines[2])
    typist = get_typist(lines[3])

    document, created = Document.objects.get_or_create(
        filename=filename, mp3_filename=mp3_file, duration=duration,
        date=file_date, typist=typist, owner=user)

    if created:
        line_num = 1
        for line in lines[4:]:
            if line != "":
                if line == "END AUDIO":
                    break
                Line.objects.create(document=document, text=line,
                                    line_num=line_num)
                line_num += 1

    return document
