import math
from asyncio.log import logger
from cmath import log
from PIL import Image, ImageFont, ImageDraw
import datetime
import calendar
import json
import os
import glob
import re

STATIC_IMG_FOLDER = './static/images/'

poppin = "./capture_writer/Poppins/Poppins-MediumItalic.ttf"
with open('./capture_writer/config.json') as f:
    classes_configs = json.load(f)

# print(classes_configs)


def return_classes_names():
    names = []
    for i in classes_configs:
        names.append(i["class"])
    return names

# print(return_classes_names())


def return_class(class_name: str):
    answer = {}
    for i in classes_configs:
        if class_name == i["class"]:
            answer = i
            return True, answer
    return False, answer

# print(return_class('First_World_Problems'))


def drawTextWithOutline(draw, text, x, y, font):
    draw.text((x-2, y-2), text, (0, 0, 0), font=font)
    draw.text((x+2, y-2), text, (0, 0, 0), font=font)
    draw.text((x+2, y+2), text, (0, 0, 0), font=font)
    draw.text((x-2, y+2), text, (0, 0, 0), font=font)
    draw.text((x, y), text, (255, 255, 255), font=font)
    return


def drawTextInBox(img, text, template_config):
    #img : PIL.JpegImagePlugin.JpegImageFile
    draw = ImageDraw.Draw(img)
    # print(template_config)
    # print(type(template_config['areas']))
    for string, area in zip(text, template_config['areas']):
        fontsize = template_config["fontsize"]
        exit = False
        make_less_fontsize = True
        while exit == False:
            string = string.upper()
            if make_less_fontsize == False:
                fontsize += 2
            font = ImageFont.truetype(poppin, fontsize, encoding="unic")
            w, h = draw.textsize(string, font)
            lineCount = 1
            if w > (area[2] - area[0]):
                lineCount = int(round((w / (area[2] - area[0])) + 1))
            lines = []
            if lineCount > 1:
                lastCut = 0
                isLast = False
                for i in range(0, lineCount):
                    if lastCut == 0:
                        cut = int((len(string) / lineCount) * i)
                    else:
                        cut = lastCut
                    if i < lineCount - 1:
                        nextCut = int((len(string) / lineCount) * (i + 1))
                    else:
                        nextCut = len(string)
                        isLast = True
                    # make sure we don't cut words in half
                    if nextCut == len(string) or string[nextCut] == " ":
                        pass
                        #print("may cut")
                    else:
                        while string[nextCut] != " ":
                            nextCut += 1
                    line = string[cut:nextCut].strip()
                    # is line still fitting ?
                    w, h = draw.textsize(line, font)
                    if not isLast and w > (area[2] - area[0]):
                        nextCut -= 1
                        while string[nextCut] != " ":
                            nextCut -= 1
                    lastCut = nextCut
                    lines.append(string[cut:nextCut].strip())
            else:
                lines.append(string)
            #            if i == 1:
            lastY = area[3] - h * (lineCount + 1) - 10
            #print(lineCount*h + (lineCount-1)*h*0.15)
            #print(area[3] - area[1])
            if (lineCount*h + (lineCount-1)*h*0.15 < area[3] - area[1]):
                # на случай если надо увеличить размер шрифта как например в последнем окне Doge
                exit = True
                # print(fontsize)
            else:
                fontsize -= 1
            # print(fontsize)
        for i in range(0, lineCount):
            w, h = draw.textsize(lines[i], font)
            x = area[0] + ((area[2] - area[0]) / 2) - (w/2)
            y = lastY + h
            drawTextWithOutline(draw, lines[i], x, y, font)
            lastY = y
    return img


def clean_old_memes(dir: str, class_: str):
    '''
    Удаляет старые мемы по паттерну второго параметра функции
    @dir - путь до папки с изображениями
    @class_ - путь до папки с изображениями
    '''
    path_pattern = dir+f"/{class_}*.jpg"
    print(path_pattern)
    for f in glob.glob(path_pattern):
        print(f)
        try:
            print(f'Удаление файла {f}')
            os.remove(f)
        except Exception as e:
            print('[clean_old_memes]:', e)

def change_text_count(text: list, box_count: int):
    # соединили боксы установив точки между боксами.
    # соединили боксы установив точки между боксами.
    string = ".".join(text)
    string = re.sub('([!?.])', r'\1|', string)
    count = len(re.findall(r'[!?.]', string))
    new_text = re.split('\|', string)
    if count == box_count:
        return new_text
    elif count > box_count:
        while len(new_text) > box_count:
            u_index=0
            u_len = math.inf
            # находим 2 соседних элемента которые суммарно имеют наименьшую длину
            for i in range(0,len(new_text)-1):
                if len(new_text[i]+new_text[i+1]) < u_len:
                    u_len = len(new_text[i]+new_text[i+1])
                    u_index = i
            #  объединяем
            union = new_text[u_index]+new_text[u_index+1]
            u_new_text = new_text[0:u_index]+[union]+new_text[u_index+2:]
            new_text = u_new_text
        return new_text
    elif count < box_count:
        while len(new_text) < box_count:
            u_index = 0
            u_len = 0
            for i in range(len(new_text)):
                if len(new_text[i])>u_len:
                    u_len = len(new_text[i])
                    u_index = i
            share = new_text[u_index].split(' ')
            k=0
            for i in range(len(share)):
                k=i
                sum1=sum([len(x) for x in share[:i]])
                sum2=sum([len(x) for x in share[i:]])
                if sum1>sum2:
                    break
            part1 = " ".join(share[:k])
            part2 = " ".join(share[k:])
            u_new_text = new_text[0:u_index] + [part1] + [part2] + new_text[u_index+1:]
            new_text = u_new_text
        return new_text



def draw_text(class_: str, text: str):
    print(f"text  {text}")
    # чистые картинки лежат в папке templates
    # проверка на наличие такого класса в рисовалке

    if class_ not in return_classes_names():
        print(
            f"Config.json doesn't contains {class_}. Check config and class name.")
    else:
        # получение конфига класса
        check, template_config = return_class(class_)
        if check:
            # получение шаблона мема (картинки без подписей)
            image = Image.open(f"./capture_writer/templates/{class_}.jpg")

            # текст уже приходит разбитый в list
            # сплитуем текст мема
            #text = text.split('|')

            # случай когда у нас текста меньше чем коробок для написания текста
            # ПЕРЕДЕЛАЙ ТЕКСТ)
            if len(template_config['areas']) != len(text):
                text = change_text_count(text,len(template_config['areas']))
            #while len(template_config['areas']) > len(text):
            #    text.append(" ")
            #text = text if len(template_config['areas']) == len(text) else text.append("")
            # проверяем что количество боксов совпадает с количеством окошек для написания
            #if len(template_config['areas']) == len(text):
            # начинаем рисовать
            image = drawTextInBox(image, text, template_config)
            # создадим текущую метку utc для создания уникальной картинки
            crnt_dt = str(calendar.timegm(
                datetime.datetime.utcnow().utctimetuple()))
            # создаем путь до нового мема
            path_img = f"{STATIC_IMG_FOLDER}{class_}_{crnt_dt}.jpg"
            # прежде чем сохранять, имеет смысл почистить другие мемы
            clean_old_memes(STATIC_IMG_FOLDER, class_)

            # это потом можно удалить или закомментировать
            image.save(path_img)
            # вот тут тебе вернется картинка и флаг получилось или нет
            # type(img) = PIL.JpegImagePlugin.JpegImageFile
            return True, path_img
            '''else:
                # количество окошек не совпадает с количеством текстовых единиц мема
                print("textbox's count and texts count are not equal")
                return False, image'''
        else:
            print(f"something goes wrong in getting {class_} config")
