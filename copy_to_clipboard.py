#coding: utf-8

import base64
import re

import pyperclip

"""
Windows10 + Thunderbirdユーザーのための、メールヘッダー抜粋スクリプト。
Thunderbird は To, CC, Subject, Date のペインを簡単にコピペできない。

CRMを使っているとそのようなテキストをコピペした場合がある。
そんなときはソースから取るしかなかったが、ソースは BASE64 MIME エンコーディングのままで人間的ではなかった。

targetという名前でメールのソースを保存後（CTRL+U, CTRL+S）に実行すると、そのような文字列をデコードして、
To, CC, Subject, Date を含む人間的なテキストをクリップボードへコピーする。

動作環境:
    Windows 10
    Python 3 (Anaconda)
        pip install pyperclip
    Thunderbird
"""

def main():
    lines = open("target").readlines()
    read = False
    wanted = []
    for line in lines:
        if (not line.startswith(" ")) and (not line.startswith("\t")):
            read = False
        if line.startswith("From: ") or\
        line.startswith("To: ") or\
        line.startswith("CC: ") or\
        line.startswith("Subject: ") or\
        line.startswith("Date: "):
            read = True
        if read:
            wanted.append(line)

    wanted = map(lambda line: line.strip(), wanted)
    replaced = []
    ptn4decode = re.compile(".*\=\?(?P<encoding>.+)\?(?P<BOM>.+)\?(?P<base64string>.+)\?\=.*")
    ptn4replace = re.compile(".*(?P<base64mime>\=\?.*\?\=).*")
    for line in wanted:
        m1 = ptn4decode.match(line)
        m2 = ptn4replace.match(line)
        if (m1 is not None) and (m2 is not None):
            d1 = m1.groupdict()
            d2 = m2.groupdict()
            base64bytes = d1["base64string"].encode(d1["encoding"])
            string_ = base64.b64decode(base64bytes).decode(d1["encoding"])
        replaced.append(line.replace(d2["base64mime"], string_))
    s = "".join(replaced)
    s = s.replace("To: ", "\nTo: ")
    s = s.replace("CC: ", "\nCC: ")
    s = s.replace("Subject: ", "\nSubject: ")
    s = s.replace("Date: ", "\nDate: ")
    print(s)
    pyperclip.copy(s)
    print("\nがクリップボードへコピーされました。")

if __name__ == "__main__":
    main()
    input("press enter to exit")
