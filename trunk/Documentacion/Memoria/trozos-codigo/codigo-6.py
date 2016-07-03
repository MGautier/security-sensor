tag_str = ((re.compile('^(.*)=')).search(str(line))).group(0)
tag_split = tag_str.split(',')
