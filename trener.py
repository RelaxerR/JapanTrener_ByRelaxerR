from datetime import datetime as dt
from progress.bar import IncrementalBar
from googletrans import Translator

def PrintBlock (text, seperator=True, enterCount=0):
    c = 30
    if (len (text) < c):
        c -= len (text)
    else:
        c = 3
    if (not seperator):
        c = 0
    print ("\n" + "-" * int (c) + str (text) + "-" * int (c) + "\n" * enterCount)
def Log (text):
    if (_ALLOWLOGGING):
        now = dt.now ()
        ct = now.strftime("%H:%M:%S")

        print ("[" + str (ct) + ": " + str (text) + "]")

_ALLOWLOGGING = False
al = input ("Включить логи? (y/n): ")
if (al == "y"):
    _ALLOWLOGGING = True

PrintBlock ("Загрузка библиотек")
import pandas as pd
Log ("Loaded: pandas")

def LoadData ():
    PrintBlock ("[Загрузка данных]")
    Log ("Loading data")
    data = []
    try:
        data = pd.read_csv ("C:/Projects/Python/JapanTrener/data.csv")
        Log (data)
        Log ("data loaded")
    except:
        startData = {'symbol': [], 'true': [], 'false': []}
        data = pd.DataFrame (startData)
        Log ("data created")
    return data
def SaveData (_data):
    Log ("Saving data")
    try:
        _data.to_csv("C:/Projects/Python/JapanTrener/data.csv", index=False)
        Log ("data saved")
        return True
    except:
        Log ("data not saved")
        return False

def AddSymbol (_data, symbol):
    newSym = {'symbol': str (symbol), 'true': '0', 'false': '0'}
    data = _data.append (newSym, ignore_index=True)
    Log ("Symbol added: " + str (symbol))
    PrintBlock ("Символ добавлен")

    SaveData (data)
    return data
def DeleteSymbol (_data, symbol):
    data = _data
    try:
        if (input ('Вы уверены, что хотите удалить символ "' + str (symbol) + '"? (y/n) ') == 'y'):
            data = _data.loc[_data['symbol'] != str (symbol)]
            Log ("Symbol deleted: " + str (symbol))
            PrintBlock ("Символ удалён")

            SaveData (data)
            return data
        else:
            return data
    except:
        PrintBlock ("Не удалось найти символ")
        return data
def AddStats (_data, sym, t):
    data = _data
    try:
        i = data.index[data['symbol'] == str (sym)].tolist()[0]
        data.at[int (i), str (t)] += 1
        Log ("stats added: " + str (sym) + " | " + str (data.at[int (i), str (t)]))

        SaveData (data)
    except:
        Log ("Error adding stats")
    return data
    
def GetRandomSymbolRow (_data):
    tmp = _data.sample ()
    Log ("Getted random symbol: " + str (tmp))
    return tmp

'''
Символ:
Количество правильных ответов
Количество неправильных ответов
Количество ответов
Процент правильных ответов

Количество символов

Количество правильных ответов во всех символах
Количество неправильных ответов во всех символах
Количество ответов во всех символах
Процент правильных ответом во всех символах (средний процент правильных овтетов)
Максимальный процент правильных ответов
Минимальный процент правильных ответов
Среднее количество ответов во всех символах

Массив строк с Максимальный процент правильных ответов
Массив строк с Минимальный процент правильных ответов
Массив символов с Максимальный процент правильных ответов
Массив символов с Минимальный процент правильных ответов
Массив строк с процентом выше среднего
Массив строк с процентом ниже среднего

Дополнительно символ:
Процент всех ответов от общего
Процент верных ответов от общего
Процент неверных ответов от общего
Получить скорректированный процент правильных ответов символа от общего
'''

def GetSymRow (_data, sym):
    Log ("Trying to get row of sym " + str (sym) + " of dataframe:" + str (_data))
    if not str (sym) in list (_data['symbol']):
        Log ("failed")
        return pd.DataFrame.empty
    row = _data.loc[_data['symbol'] == str (sym)]
    Log ("sucsess: " + str (row))
    return row
def GetSymName (_row):
    row = _row
    Log ("Trying to get row symbol name: " + str (row))
    return str (row['symbol'].loc[row.index[0]])
def GetSymTrue (row):
    return int (row['true'])
def GetSymFalse (row):
    return int (row['false'])
def GetSymAnswersCount (row):
    t = int (GetSymTrue (row))
    f = int (GetSymFalse (row))
    Log ("GetSymAnswersCount: " + str (t + f))
    return t + f
def GetSymTruePercent (row):
    t = int (GetSymTrue (row))
    a = int (GetSymAnswersCount (row))
    o = 0
    if (a == 0):
        o = 0
    else:
        o = round (t / a * 100)
    Log ("GetSymTruePercent: " + str (o))
    return o

def GetSymCount (_data):
    count = 0
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        count += 1
    Log ("GetSymCount: " + str (count))
    return count

def GetAllSymTrueCount (_data):
    count = 0
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        t = int (GetSymTrue (row))
        count += t
    Log ("GetAllSymTrueCount: " + str (count))
    return count
def GetAllSymFalseCount (_data):
    count = 0
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        f = int (GetSymFalse (row))
        count += f
    Log ("GetAllSymFalseCount: " + str (count))
    return count
def GetAllSymAnswersCount (_data):
    t = int (GetAllSymTrueCount (_data))
    f = int (GetAllSymFalseCount (_data))
    Log ("GetAllSymAnswersCount: " + str (t + f))
    return t + f
def GetAllSymAvgTruePercent (_data):
    a = int (GetAllSymAnswersCount (_data))
    t = int (GetAllSymTrueCount (_data))
    Log ("GetAllSymAvgTruePercent: " + str (round (t / a * 100)))
    return round (t / a * 100)
def GetAllSymMaxTruePercent (_data):
    truePercent = 0
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        f = int (GetSymTruePercent (row))
        if (f > truePercent):
            truePercent = f
    Log ("GetAllSymMaxTruePercent: " + str (round (truePercent)))
    return round (truePercent)
def GetAllSymAvgAnswers (_data):
    a = int (GetAllSymAnswersCount (_data))
    c = int (GetSymCount (_data))
    Log ("GetAllSymAvgAnswers: " + str (round (a / c)))
    return round (a / c)
def GetAllSymMinTruePercent (_data):
    truePercent = 101
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        f = int (GetSymTruePercent (row))
        if (f < truePercent):
            truePercent = f
    Log ("GetAllSymMinTruePercent: " + str (round (truePercent)))
    return round (truePercent)

def GetRowsMaxTruePercent (_data):
    rows = []
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        sym = str (GetSymName (row))
        t = int (GetSymTruePercent (row))
        m = int (GetAllSymMaxTruePercent (_data))
        if (t >= m):
            rows.append (row)
    Log ("GetRowsMaxTruePercent: " + str (rows))
    return rows
def GetRowsMinTruePercent (_data):
    rows = []
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        t = int (GetSymTruePercent (row))
        m = int (GetAllSymMinTruePercent (_data))
        if (t <= m):
            rows.append (row)
    Log ("GetRowsMinTruePercent: " + str (rows))
    return rows
def GetSymsMaxTruePercent (_data):
    rows = GetRowsMaxTruePercent (_data)
    syms = []
    for row in rows:
        syms.append (GetSymName (row))
    Log ("GetSymsMaxTruePercent: " + str (syms))
    return syms
def GetSymsMinTruePercent (_data):
    rows = GetRowsMinTruePercent (_data)
    syms = []
    for row in rows:
        syms.append (GetSymName (row))
    Log ("GetSymsMinTruePercent: " + str (syms))
    return syms
def GetSymsOverAvgTruePercent (_data):
    Log ("GetSymsOverAvgTruePercent")
    avg = int (GetAllSymAvgTruePercent (_data))
    syms = []
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        t = int (GetSymTruePercent (row))
        if (t > avg):
            syms.append (str (GetSymName (row)))
    Log ("GetSymsOverAvgTruePercent: " + str (syms))
    return syms
def GetSymsUnderAvgTruePercent (_data):
    avg = int (GetAllSymAvgTruePercent (_data))
    syms = []
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        t = int (GetSymTruePercent (row))
        if (t < avg):
            syms.append (str (GetSymName (row)))
    Log ("GetSymsUnderAvgTruePercent: " + str (syms))
    return syms

def GetAnswersPercent (_data, row):
    s = int (GetSymAnswersCount (row))
    a = int (GetAllSymAnswersCount (_data))
    return round (s / a * 100,1)
def GetTrueAnswersPercent (_data, row):
    t = int (GetSymTrue (row))
    a = int (GetAllSymTrueCount (_data))
    return round (t / a * 100,1)
def GetFalseAnswersPercent (_data, row):
    f = int (GetSymFalse (row))
    a = int (GetAllSymFalseCount (_data))
    return round (f / a * 100,1)
def GetCorrectedTrueAnswerPercent (_data, row):
    t = int (GetSymTruePercent (row))
    a = int (GetAnswersPercent (_data, row))
    o = round (t * a / 100,2)
    Log ("----------------------------GetCorrectedTrueAnswerPercent of sym " + str (GetSymName (row)) + " t: " + str (t) + " a: " + str (a) + " out: " + str (o))
    return o
def GetAvgCorrectedTrueAnswersPercent (_data):
    allp = 0
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        allp += int (GetCorrectedTrueAnswerPercent (_data, row))
    return (allp / int (GetSymCount (_data)))
def GetRowMaxCorrectedTrueAnswersPercent (_data):
    maxp = -1
    outRow = None
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        ct = int (GetCorrectedTrueAnswerPercent (_data, row))
        if (ct > maxp):
            maxp = ct
            outRow = row
    return outRow
def GetProgressPercent (_data, myRow):
    maxRow = GetRowMaxCorrectedTrueAnswersPercent (_data)
    p = GetCorrectedTrueAnswerPercent (_data, myRow) / GetCorrectedTrueAnswerPercent (_data, maxRow) * 100
    return round (p * GetSymTruePercent (myRow) / 100, 2)
def GetAvgProgressPercent (_data, progressbar = False):
    allp = 0
    if (progressbar):
        bar = IncrementalBar('Расчёт прогресса символов...', max = GetSymCount (_data))
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        allp += GetProgressPercent (_data, row)
        if (progressbar):
            bar.next()
    if (progressbar):
        bar.finish()
    print ("\n")
    p = allp / GetSymCount (_data)
    return round (p)
def GetBestRows (_data, progressbar = False):
    avg = int (GetAvgProgressPercent (_data, progressbar))
    rows = []
    if (progressbar):
        bar = IncrementalBar('Поиск лучших символов...', max = GetSymCount (_data))
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        if (GetProgressPercent (_data, row) >= avg):
            rows.append (row)
        if (progressbar):
            bar.next()
    if (progressbar):
        bar.finish()
    print ("\n")
    return rows
def GetBadRows (_data, progressbar = False, isList = False):
    avg = int (GetAvgProgressPercent (_data, progressbar))
    if (isList):
        rows = []
    else:
        d = {'symbol':[], 'true':[], 'false':[]}
        rows = pd.DataFrame (d)
    if (progressbar):
        bar = IncrementalBar('Поиск плохих символов...', max = GetSymCount (_data))
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        if (GetProgressPercent (_data, row) <= avg):
            if (isList):
                rows.append (row)
            else:
                rows = rows.append (row)
        if (progressbar):
            bar.next()
    if (progressbar):
        bar.finish()
    print ("\n")
    return rows
def GetRandomBadSymbolRow (_data):
    rows = GetBadRows (_data)
    row = rows.sample ()
    return row

def PrintSymStats (_data, sym, level=1):
    PrintBlock ("Загрузка статистики")
    row = GetSymRow (_data, sym)
    PrintBlock ('Статистика для символа "' + str (GetSymName (row)) + '"')
    if (GetProgressPercent (_data, row) >= GetAvgProgressPercent (_data)):
        PrintBlock ("Best symbol!")
    PrintBlock ("Прогресс: " + str (GetProgressPercent (_data, row)) + "%")
    PrintBlock ("Процент правильных ответов: " + str (GetSymTruePercent (row)) + "%")
    if (int (level) > 0):
        PrintBlock ("Ответов: " + str (GetSymAnswersCount (row)), True, 0)
        PrintBlock ("Правильных ответов: " + str (GetSymTrue (row)), True, 0)
        PrintBlock ("Неправильных ответов: " + str (GetSymFalse (row)) + "")
    if (int (level) > 1):
        PrintBlock ("Процент ответов от общего: " + str (GetAnswersPercent (_data, row)) + "%", True, 0)
        PrintBlock ("Процент правильных ответов от общего: " + str (GetTrueAnswersPercent (_data, row)) + "%", True, 0)
        PrintBlock ("Процент неправильных ответов общего: " + str (GetFalseAnswersPercent (_data, row)) + "%")
    if (int (level) > 2):
        PrintBlock ("Вклад в изучение:")
        PrintBlock ("Правильные ответы: " + str (GetCorrectedTrueAnswerPercent (_data, row)) + "%")
    PrintBlock ("")
def PrintAllStats (_data):
    PrintBlock ("Загрузка статистики")
    maxProg = GetSymCount (_data)
    percents = []
    names = []
    bar = IncrementalBar('Расчёт прогрессов...', max = maxProg)
    for row in _data.itertuples(index=False):
        d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
        row = pd.DataFrame (d)
        percents.append (GetProgressPercent (_data, row))
        names.append (GetSymName (row))

        bar.next ()
    bar.finish()
    print ("\n")
    for i in range (len (percents)):
        for j in range(len (percents)-i-1):
            if percents[j] > percents[j+1]:
                percents[j], percents[j+1] = percents[j+1], percents[j]
                names[j], names[j+1] = names[j+1], names[j]

    PrintBlock ("Статистика для всех символов:")
    txt = "\n"
    for i in range (len (percents)):
        txt += '"' + str (names[i]) + '": ' + str (percents[i]) + "%\n"
    PrintBlock (txt)


def PrintBestStats (_data):
    PrintBlock ("Загрузка статистики")
    bar = IncrementalBar('Анализ данных...', max=2)
    maxSyms = GetSymsMaxTruePercent (_data)
    bar.next ()
    minSyms = GetSymsMinTruePercent (_data)
    bar.next ()
    bar.finish()
    print ("\n")
    bestRows = GetBestRows (_data, True)
    badRows = GetBadRows (_data, True, True)

    maxTxt = ""
    minTxt = ""

    for sym in maxSyms:
        maxTxt += '"' + str (sym) + '" '
    for sym in minSyms:
        minTxt += '"' + str (sym) + '" '

    bar = IncrementalBar('Анализ лучших символов...', max = len (bestRows) * 3)
    bestTxt = ""

    names = []
    truePercents = []
    percents = []

    for row in bestRows:
        names.append (str (GetSymName (row)))
        truePercents.append (str (GetSymTruePercent (row)))
        percents.append (str (round (GetProgressPercent (_data, row))))
        bar.next ()

    for i in range (len (percents)):
        for j in range(len (percents)-i-1):
            if int (percents[j]) > int (percents[j+1]):
                percents[j], percents[j+1] = percents[j+1], percents[j]
                names[j], names[j+1] = names[j+1], names[j]
                truePercents[j], truePercents[j+1] = truePercents[j+1], truePercents[j]
        bar.next ()


    for i in range (len (bestRows)):
        bestTxt += '"' + names[i] + '" - ' + truePercents[i] + '% правильных ответов (' + 'Освоен на: ' + percents[i] + '%)\n'
        bar.next ()
        
    bar.finish()
    print ("\n")
    bar = IncrementalBar('Анализ плохих символов...', max = len (badRows) * 3)
    badTxt = ""

    names = []
    truePercents = []
    percents = []
    
    for row in badRows:
        names.append (str (GetSymName (row)))
        truePercents.append (str (GetSymTruePercent (row)))
        percents.append (str (round (GetProgressPercent (_data, row))))
        bar.next ()

    for i in range (len (percents)):
        for j in range(len (percents)-i-1):
            if int (percents[j]) > int (percents[j+1]):
                percents[j], percents[j+1] = percents[j+1], percents[j]
                names[j], names[j+1] = names[j+1], names[j]
                truePercents[j], truePercents[j+1] = truePercents[j+1], truePercents[j]
        bar.next ()

    for i in range (len (badRows)):
        badTxt += '"' + names[i] + '" - ' + truePercents[i] + '% правильных ответов (' + 'Освоен на: ' + percents[i] + '%)\n'
        bar.next ()
    bar.finish()
    print ("\n")
    
    getAvgProgressPercent = round (GetAvgProgressPercent (_data, True))
    PrintBlock ("Прогресс символов: " + str (getAvgProgressPercent) + "%")
    PrintBlock ("Наиболее запомнившиеся символы")
    PrintBlock ("Лучшие символы:\n" + str (bestTxt), False)
    PrintBlock ("Хорошие символы:\n" + str (maxTxt), False, 1)
    PrintBlock ("Плохо запомнившиеся символы")
    PrintBlock ("Худшие символы:\n" + str (badTxt), False)
    PrintBlock ("Обратить внимание:\n" + str (minTxt), False, 2)

def LoadFromTxt (_data, path):
    data = _data
    places = []
    try:
        with open(path, 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                places.append(currentPlace)
                PrintBlock ("Данные добавлены: " + str (currentPlace))
    except:
        return False

    for p in places:
        data = AddSymbol (data, p)
        Log ("Символ добавлен: " + str (p))
    data = SaveData (data)
    return data

Data = LoadData ()
slovar = {
    ' a ':'あ',  ' i ':'い',  ' u ':'う',   ' e ':'え',' o ':'お',
    'ka':'か', 'ki':'き', 'ku':'く', 'ke':'け','ko':'こ',
    'sa':'さ', 'shi':'し','su':'す', 'se':'せ','so':'そ',
    'ta':'た', 'chi':'ち','tsu':'つ','te':'て','to':'と',
    'na':'な', 'ni':'に', 'nu':'ぬ', 'ne':'ね','no':'の',
    'ha':'は', 'hi':'ひ', 'fu':'ふ', 'he':'へ','ho':'ほ',
    'ma':'ま', 'mi':'み', 'mu':'む', 'me':'め','mo':'も',
    'ya':'や', '':'','yu':'ゆ', '':'',  'yo':'よ',
    'ra':'ら', 'ri':'り', 'ru':'る', 're':'れ','ro':'ろ',
    'wa':'わ', '':'',  '':'',   '':'',  'wo':'を',
    'n':'ん',  '':'',   '':'',   '':'',   '':'',
}

translator = Translator ()
while (True):
    commands = input ('\nВведите команду: ').split (' ')
    if (commands[0] == "add"):
        if (len (commands) > 1):
            Data = AddSymbol (Data, commands[1])
    elif (commands[0] == "tmp"):
        for row in Data.itertuples(index=False):
            d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
            row = pd.DataFrame (d)
            Log (row)
            break
    elif (commands[0] == "del"):
        if (len (commands) > 1):
            Data = DeleteSymbol (Data, commands[1])
    elif (commands[0] == "stats"):
        if (len (commands) > 1):
            if (len (commands) > 2):
                PrintSymStats (Data, commands[1], commands[2])
            elif (commands[1] == "best"):
                PrintBestStats (Data)
            else:
                PrintAllStats (Data)
        else:
            PrintBestStats (Data)
    elif (commands[0] == "quit"):
        exit ()
    elif (commands[0] == "load"):
        if (len (commands) > 1):
            Data = LoadFromTxt (Data, commands[1])
    elif (commands[0] == "allowlogging"):
        _ALLOWLOGGING = not _ALLOWLOGGING
    elif (commands[0] == "train"):
        if (len (commands) > 1):
            count = 0
            try:
                count = int (commands[1])
            except:
                count = 10
            if (len (commands) > 2):
                wordCount = 1
                try:
                    wordCount = int (commands[2])
                except:
                    wordCount = 3

            PrintBlock ("Загрузка символов")
            badSymbols = GetBadRows (Data, True)
            lastData = Data
            lastProgress = []
            bar = IncrementalBar('Сохранение данных...', max = GetSymCount (lastData))
            for row in lastData.itertuples(index=False):
                d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
                row = pd.DataFrame (d)
                lastProgress.append (GetProgressPercent (lastData, row))
                bar.next ()
            bar.finish ()
            PrintBlock ("Тренеровка на " + str (count) + " слов. Длина слов: " + str (wordCount))
            gettedSyms = []
            maxI = 15
            for i in range (count):
                row = None
                syms = []
                word = ""
                japanWord = ""
                for w in range (wordCount):
                    nowI = 0
                    while nowI < maxI:
                        if (i % 2 == 0):
                            row = GetRandomSymbolRow (Data)
                        else:
                            row = badSymbols.sample ()
                        if (GetSymTruePercent (row) > 90) or (str (GetSymName (row) in syms)):
                            nowI += 1
                        else:
                            break
                    sym = str (GetSymName (row))
                    syms.append (sym)
                    if (not sym in gettedSyms):
                        gettedSyms.append (sym)
                    word += sym
                    japanWord += f" {sym} "
                for key in slovar:
                    japanWord = japanWord.replace(key, slovar[key])
                japanWord.replace (' ', '')
                ruWord = translator.translate (japanWord, src='ja', dest='ru').text
                cnt = input ('Напишите "' + str (word) + f'" (перевод - {ruWord}): ')
                cmd = input (f'"{japanWord}": ENTER - правильно, q - выйти, любой символ - неправильно')
                if (cmd == ""):
                    for s in syms:
                        Data = AddStats (Data, s, "true")
                elif (not cmd == "q"):
                    for s in syms:
                        Data = AddStats (Data, s, "false")
                else:
                    break
            PrintBlock ("Тренеровка завершена!")
            
            newData = LoadData ()
            symNames = []
            newProgress = []

            bar = IncrementalBar('Анализ изменений...', max = GetSymCount (newData) + 1)
            for row in newData.itertuples(index=False):
                d = {'symbol':[str (row[0])], 'true':[str (row[1])], 'false':[str (row[2])]}
                row = pd.DataFrame (d)

                symNames.append (GetSymName (row))
                newProgress.append (GetProgressPercent (newData, row))
                bar.next ()
            txt = ""
            for i in range (len (symNames)):
                progChange = round (newProgress[i] - lastProgress[i], 2)
                if not (int (progChange) == 0):
                    txt += f'Прогресс символа "{str (symNames[i])}": {str (lastProgress[i])}% -> {str (newProgress[i])}% ({str (progChange)}%)\n'
            bar.next ()
            bar.finish ()
            PrintBlock (txt)
    elif (commands[0] == "quit"):
        exit ()
    else:
        PrintBlock ("Управление символами")
        PrintBlock ('"add [symbol]" - добавить символ"\ndel [symbol]" - удалить символ"\nload [path]" - загрузить новые символы из .txt (по символу на строку файла)', False)
        PrintBlock ("Статистика")
        PrintBlock ('"stats [symbol] [level]" - показать статистику символа (уровень статистики level)"\nstats all" - показать всю статистику\n"stats best" - показать лучшие символы', False)
        
        PrintBlock ("Тренеровка")
        PrintBlock ('"train [count] [word_lenght]" - запустить тренеровку с количеством символов и длиной слова\nENTER - правильное написание символа\n[q] - завершить тренеровку"\n[ANOTHER]" - неправильное написание символа', False)

        PrintBlock ("[Система]")
        PrintBlock ('allowlogging - включить/выключить логи\n"quit" - выйти', False)
        continue