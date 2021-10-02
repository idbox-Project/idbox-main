import idbEnvlib
from settings import define
language=__import__(define.languageSelect)

while True:
    print('='*20)
    print(language.WelcomeText)
    print(language.SelectPlug)
    print('='*20)
    adb