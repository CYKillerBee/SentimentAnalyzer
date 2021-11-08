import re
import string

def text_cleaner(textData):
    # remove tab, new line, ans back slice
    textData = textData.replace('\\t', " ").replace('\\n', " ").replace('\\u', " ").replace('\\', "")
    # remove non ASCII (emoticon, chinese word, .etc)
    textData = textData.encode('ascii', 'replace').decode('ascii')
    # remove mention, link, hashtag
    textData = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", textData).split())
    # remove incomplete URL
    textData = textData.replace("http://", " ").replace("https://", " ")
    # remove non-English characters
    textData = re.sub("([^\x00-\x7F])+", " ", textData)
    # remove number
    textData = re.sub(r"\d+", "", textData)
    # remove punctuation
    textData = textData.translate(str.maketrans("", "", string.punctuation))
    # remove whitespace leading & trailing
    textData = textData.strip()
    # remove multiple whitespace into single whitespace
    textData = re.sub('\s+', ' ', textData)


    return textData
