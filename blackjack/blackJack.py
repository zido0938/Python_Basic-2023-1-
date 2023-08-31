#블랙잭
#프로그래밍 기초 수업 과제

import random

def load_members():
    file = open("members.txt","r",encoding="UTF-8")
    members = {}

    for line in file:
        name, passwd, tries, wins, chips = line.strip('\n').split(',')
        members[name] = (passwd,int(tries),int(wins),int(chips))
    file.close()
    return members

def login(members):
    username = input("Enter your name: (4 letters max) ")
    while len(username) > 4:
        username = input("Enter your name: (4 letters max) ")
    trypasswd = input("Enter your password: ")
    if username in members:
        if members[username][0] == trypasswd:
            passwd,tries,wins,chips = members[username]
            return username, tries, wins, chips, members
        else:
            return login(members)
    else:
        members[username] = (trypasswd,0,0,0)
        return username, 0, 0, 0, members



def fresh_deck():
    suits = {"Spade", "Heart", "Diamond", "Club"}
    ranks = {"A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"}
    deck = []

    for shape in suits:
        for x in ranks:
            card = {"suit": shape, "rank": x}
            deck.append(card)

    random.shuffle(deck)
    return deck

def hit(deck):
    if deck == []:
        deck = fresh_deck()
    return  (deck[0] , deck[1:])


def count_score(cards):
    score = 0
    number_of_ace = 0
    for card in cards:
        if card['rank'] == 'A':
            number_of_ace += 1
            score += 1

        elif card['rank'] == 'J' or card['rank'] == 'Q' or card['rank'] == 'K':
            score += 10
        else:
            score += card['rank']

    for x in range(number_of_ace):
        if score+10 <= 21:
            score += 10
        else:
            return score
    return score


def show_cards(cards,message):
    print(message)
    for card in cards:
        print('   '+card['suit'],card['rank'])


def more(message):
    answer = input(message+' ')
    while not (answer == 'y' or answer == 'n'):
        answer = input(message)
    return answer == 'y'


def Game():
    card = fresh_deck()
    user_card = []
    com_card = []

    # 처음 2장씩 나눠 주기
    for x in range(2):
        add, card = hit(card)
        user_card += [add]
        add, card = hit(card)
        com_card += [add]

    # 딜러의 첫 카드 보여주기
    print("-----"+"\nMy cards are:")
    print("  **** **")
    print("  "+com_card[1]['suit']+' ',com_card[1]['rank'])

    # 유저 첫 카드 보여주기
    show_cards(user_card,"Your cards are:")

    user_score = count_score(user_card)
    com_score = count_score(com_card)

    #블랙잭으로 이긴 경우
    if user_score == 21:
        print("Blackjack! You won.")
        return 2   # 블랙잭으로 이기면 상금을 2배로받음

    #유저가 버스트가 아닌 동안
    while user_score < 21:

        #딜러는 점수가 16 이하면 무조건 카드 받음
        if com_score <= 16:
            add, card = hit(card)
            com_card += [add]
            com_score = count_score(com_card)

        if more("Hit? (y/n)"):
            add, card = hit(card)
            user_card += [add]
            user_score = count_score(user_card)
            print("  "+add['suit']+' ',add['rank'])

        else:
            break

    show_cards(com_card,"My cards are:")

    if user_score > 21:
        print("You burst! I won.")
        return -1

    if com_score > 21:
        print("I burst! You won.")
        return 1

    if user_score < com_score:
        print("I won.")
        return -1

    if user_score == com_score:
        print("We draw.")
        return 0

    else:
        print("You won.")
        return 1

def store_members(members):
    file = open("members.txt","w")
    names = members.keys()
    for name in names:
        passwd, tries, wins, chips = members[name]
        line = name + ',' + passwd + ',' + \
               str(tries) + ',' + str(wins) + "," + str(chips) + '\n'
        file.write(line)
    file.close()



def show_top5(members):
    print("-----")
    sorted_members = sorted(members.items(),key = lambda x:x[1][3],reverse=True)
    print("All-time Top 5 based on the number of chips earned")

    cnt = 1;
    for x in range(len(sorted_members)):

        if sorted_members[x][1][3] > 0:
            print("%d. "%cnt+sorted_members[x][0]+" : %d"%sorted_members[x][1][3])
            cnt += 1
        if cnt > 5:
            break


def main():
    print("Welcome to JH Casino!")
    play = True

    username, tries, wins, chips, members = login(load_members())

    while play:
        tries += 1
        result = Game()
        chips += result
        if result > 0:
            wins += 1
        print("Chips = ",chips)
        play = more("Play more? (y/n)")

    print("You played "+str(tries)+" games and won "+ str(wins) + " of them.")
    print("Your all-time winning percentage is %.1f %%"%(wins/tries*100))
    if chips >= 0:
        print("You have "+str(chips)+" chips.")
    else:
        print("You owe " + str(-chips) + " chips.")

    members[username]= (members[username][0],tries,wins,chips)
    store_members(members)
    show_top5(members)

    print("Bye!")


main()



