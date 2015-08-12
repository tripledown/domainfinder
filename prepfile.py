import re

# cat cat /usr/share/dict/words > words.txt

prefix = ''
suffix = '.com'

with open('words.txt', 'r') as src:
    with open('domains.txt', 'w') as dest:
            for line in src:
                    line = re.sub('[-!@,#$.\']', '', line)
                    dest.write('%s%s%s\n' % (prefix, line.rstrip('\n'), suffix))