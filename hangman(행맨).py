import random




#난이도 선택.
def collect_level():
    print('=====================================================\n=====================================================')
    user_want_level = input("원하는 난이도를 입력하세요.\nEasy : 1\nNormal : 2\nHard : 3\n여기에 입력하세요.     :")
    while not (user_want_level == '1' or user_want_level == '2' or user_want_level == '3'):
        print('=====================================================\n=====================================================')
        user_want_level = input("아라비아 숫자로 구성된 난이도 1, 2, 3 중에 입력하시오.\nEasy : 1\nNormal : 2\nHard : 3\n여기에 입력하세요.     :")   
    user_want_level = int(user_want_level)
    return user_want_level



    
#단어샘플 가져오기, 오류발생시 지적
def load_words(file):
    try:
        f = open(file, "r", encoding="UTF-8")
        words = []
        for word in f.readlines():
            words.append(word.strip('\n'))
        words.sort()
    except FileNotFoundError:
        print('다음 명령어를 입력하고, 출력된 위치에 words_sample.txt 가 있는 지 확인하시오.\nimport os\nos.getcwd()')
        import sys
        sys.exit()
    return words

#단어장 불러오기.
def load_words_and_show(file):
    try:
        f = open(file, "r", encoding="UTF-8")
        words = []
        for word in f.readlines():
            words.append(word.strip('\n'))
        words.sort()
        print('******************')
        print('단어장 : ',words)
        print('******************')
    except FileNotFoundError:
        print('다음 명령어를 입력하고, 출력된 위치에 words_sample.txt 가 있는 지 확인하시오.\nimport os\nos.getcwd()')
        import sys
        sys.exit()
    return words

#선택된 단어의 임의의 인덱스 지정
def pick_a_word(words):
    n = len(words)
    index = random.randint(0, n-1)
    return words[index]

#단어 구멍 뚫기
#난이도 1: 1/3만큼
#난이도 2: 1/2만큼
#난이도 3: 전부
def puncture_word(word, n, user_want_level):
    m = user_want_level
    length = len(word)
    if m == 1:
        n = length//3
    elif m == 2:
        n = length//2
    else:
        n = length
    target = random.sample(word, n)
    #target 은 구멍이 될 글자임.
    result = ""
    for s in word:
        if s in target:
            result = result + "_"
        else:
            result = result + s
    return result, target # 구멍뚫린 단어와, 구멍인 글자들 리턴.



def puncture_word4(word, n):
    m = 1
    length = len(word)
    if m == 1:
        n = length//3
    elif m == 2:
        n = length//2
    else:
        n = length
    target = set(random.sample(word, n))
    #target 은 구멍이 될 글자임.
    result = ""
    for s in word:
        if s in target:
            result = result + "_"
        else:
            result = result + s
    return result, target # 구멍뚫린 단어와, 구멍인 글자들 리턴.



def guess(picked_word, quiz_word, target, op):
    c = input("guess a hidden character : ")
    # ord('a') == 97, ord('z') == 122
    while not(len(c) == 1 and 97 <= ord(c) <= 122):
        c = input("guess a hidden character : ")
    if c in target:
        target.remove(c)
        quiz_word = ""
        for s in picked_word:
            if s in target:                
                quiz_word += "_"
            else:                  
                quiz_word += s
        print('------------------')
        print('맞았습니다.')
        print('남은 기회는', op, '번 남았습니다.')
        draw_hangman(op)
        
        return quiz_word, target, op
    else:
        op = op - 1
        print('------------------')
        print('틀렸습니다.')
        print('남은 기회는', op, '번 남았습니다.')
        draw_hangman(op)
        return quiz_word, target, op

hangman_pics = ['''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
      |
      |
      |
      |
      |
=========''']


def draw_hangman(op):
    print(hangman_pics[op])

def main(LEVEL):
    op = 5
    user_want_level = collect_level()
    sorted_words = load_words("words_sample.txt")
    picked_word = pick_a_word(sorted_words)
    quiz_word, target = puncture_word(picked_word, 2, user_want_level)
    while '_' in quiz_word and op != 0:
        print(quiz_word)
        quiz_word, target, op = guess(picked_word, quiz_word, target, op)
    if op != 0:
        print(picked_word)
        print("축하합니다!")
        if user_want_level <= 2:
            RE = input('난이도를 한 단계 증가해 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                LEVEL += user_want_level
                main2(LEVEL)
            else:
                print('수고하셨습니다.')
        elif user_want_level == 3:
            print('가장 어려운 단계를 성공하셨습니다! 축하합니다.')
    else:
        print('기회를 모두 소진하여 패배하였습니다.')
        print('정답은', picked_word, '입니다.')
        if user_want_level >= 2:
            RE = input('난이도를 한 단계 감소해 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                LEVEL += user_want_level
                main3(LEVEL)
            else:
                print('수고하셨습니다.')
        elif user_want_level == 1:
            RE = input('단어장을 제공받은 뒤, 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                main4()
            else:
                print('수고하셨습니다.')
    

########
def main2(LEVEL):
    op = 5
    LEVEL += 1
    user_want_level = LEVEL
    sorted_words = load_words("words_sample.txt")
    picked_word = pick_a_word(sorted_words)
    quiz_word, target = puncture_word(picked_word, 2, user_want_level)
    while '_' in quiz_word and op != 0:
        print(quiz_word)
        quiz_word, target, op = guess(picked_word, quiz_word, target, op)
    if op != 0:
        print(picked_word)
        print("축하합니다!")
        if user_want_level <= 2:
            RE = input('난이도를 한 단계 증가해 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                main2(LEVEL)
            else:
                print('수고하셨습니다.')
        elif user_want_level == 3:
            print('가장 어려운 단계를 성공하셨습니다! 축하합니다.')
    else:
        print('기회를 모두 소진하여 패배하였습니다.')
        print('정답은', picked_word, '입니다.')
        if user_want_level >= 2:
            RE = input('난이도를 한 단계 감소해 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                main3(LEVEL)
            else:
                print('수고하셨습니다.')
        elif user_want_level == 1:
            RE = input('단어장을 제공받은 뒤, 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                main4()
            else:
                print('수고하셨습니다.')
######################
def main3(LEVEL):
    op = 5
    LEVEL -= 1
    user_want_level = LEVEL
    sorted_words = load_words("words_sample.txt")
    picked_word = pick_a_word(sorted_words)
    quiz_word, target = puncture_word(picked_word, 2, user_want_level)
    while '_' in quiz_word and op != 0:
        print(quiz_word)
        quiz_word, target, op = guess(picked_word, quiz_word, target, op)
    if op != 0:
        print(picked_word)
        print("축하합니다!")
        if user_want_level <= 2:
            RE = input('난이도를 한 단계 증가해 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                main2(LEVEL)
            else:
                print('수고하셨습니다.')
        elif user_want_level == 3:
            print('가장 어려운 단계를 성공하셨습니다! 축하합니다.')
    else:
        print('기회를 모두 소진하여 패배하였습니다.')
        print('정답은', picked_word, '입니다.')
        if user_want_level >= 2:
            RE = input('난이도를 한 단계 감소해 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                main3(LEVEL)
            else:
                print('수고하셨습니다.')
        elif user_want_level == 1:
            RE = input('단어장을 제공받은 뒤, 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                main4()
            else:
                print('수고하셨습니다.')
#############

def main4():
    op = 5
    user_want_level = 1
    LEVEL = 1
    sorted_words = load_words_and_show("words_sample.txt")
    
    picked_word = pick_a_word(sorted_words)
    quiz_word, target = puncture_word(picked_word, 2, 1)
    while '_' in quiz_word and op != 0:
        print(quiz_word)
        quiz_word, target, op = guess(picked_word, quiz_word, target, op)
    if op != 0:
        print(picked_word)
        print("축하합니다!")
        if user_want_level <= 2:
            RE = input('난이도를 한 단계 증가해 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                main2(LEVEL)
            else:
                print('수고하셨습니다.')
        elif user_want_level == 3:
            print('가장 어려운 단계를 성공하셨습니다! 축하합니다.')
    else:
        print('기회를 모두 소진하여 패배하였습니다.')
        print('정답은', picked_word, '입니다.')
        if user_want_level >= 2:
            RE = input('난이도를 한 단계 감소해 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                main3(LEVEL)
            else:
                print('수고하셨습니다.')
        elif user_want_level == 1:
            RE = input('단어장을 제공받은 뒤, 다시 도전해보시겠습니까? (y/n)')
            while not (RE == 'y' or RE == 'n'):
                RE = input(" 'y' 또는 'n'을 입력하시오. ")
            if RE == 'y':
                main4()
            else:
                print('수고하셨습니다.')





main(0)

