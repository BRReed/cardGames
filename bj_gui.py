"""Black Jack GUI."""
from tkinter import *
from PIL import Image, ImageTk
from black_jack import BlackJack

bj = BlackJack()
root = Tk()
root.title("Black Jack")
root.geometry("500x500")

top_frame = Frame(root, bg='cyan', width=500, height=50, pady=3)
dealer_title_frame = Frame(root, bg='black', width=500, height=25, pady=3)
dealer_frame = Frame(root, bg='white', width=500, height=150)
player_title_frame = Frame(root, bg='black', width=500, height=25, pady=3)
player_frame = Frame(root, bg='white', width=500, height=150)
bot_frame = Frame(root, bg='green', width=500, height=50, pady=3)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0)
dealer_title_frame.grid(row=1)
dealer_frame.grid(row=2)
player_title_frame.grid(row=3)
player_frame.grid(row=4)
bot_frame.grid(row=5)


def getCard(hand, i):
    """Get card information from black jack."""
    if i == 0:
        if hand[i].suit == 1:
            suit = 'clubs'
        elif hand[i].suit == 2:
            suit = 'diamonds'
        elif hand[i].suit == 3:
            suit = 'hearts'
        elif hand[i].suit == 4:
            suit = 'spades'
        if hand[i].rank == 11:
            rank = 'jack'
        elif hand[i].rank == 12:
            rank = 'queen'
        elif hand[i].rank == 13:
            rank = 'king'
        elif hand[i].rank == 14:
            rank = 'ace'
        else:
            rank = hand[i].rank
        return f'images/{suit}_{rank}.gif'
    else:
        if hand[i].suit == 1:
            suit = 'clubs'
        elif hand[i].suit == 2:
            suit = 'diamonds'
        elif hand[i].suit == 3:
            suit = 'hearts'
        elif hand[i].suit == 4:
            suit = 'spades'
        if hand[i].rank == 11:
            rank = 'jack'
        elif hand[i].rank == 12:
            rank = 'queen'
        elif hand[i].rank == 13:
            rank = 'king'
        elif hand[i].rank == 14:
            rank = 'ace'
        else:
            rank = hand[i].rank
        return f'images/sm_{suit}_{rank}.gif'


def closeWindow():
    """Quit program."""
    root.destroy()


def totalMoney():
    """Change things in window for total money."""
    player_entry_instruction.configure(text='Enter your total cash below')
    player_entry.configure(state=NORMAL)
    start_button.configure(text='Enter',
                           command=playerTotalGet)


def playerTotalGet():
    """Get money total from user input."""
    try:
        total_get = int(player_entry.get())
    except ValueError:
        player_entry_instruction.configure(text='Enter a whole number')
        player_entry.delete(0, END)
    bj.player_money = total_get
    player_entry.delete(0, END)
    total_money.configure(text=f'Total money: ${bj.player_money}')
    player_entry_instruction.configure(text='Enter your bet')
    start_button.configure(command=playerBetGet)


def playerBetGet():
    """Get bet from user total."""
    current_bet.configure(text=f'Current bet: $0')
    player_entry.configure(text='')
    while True:
        try:
            bet_get = int(player_entry.get())
        except ValueError:
            player_entry_instruction.configure(text='Enter a whole number')
        if bet_get < bj.player_money and bet_get > 0:
                bj.player_bet = bet_get
                current_bet.configure(text=f'Current bet: ${bj.player_bet}')
                break
        else:
            player_entry_instruction.configure(text='Enter a # > 0 and' +
                                               f'# < {bj.player_money}')
            player_entry.delete(0, END)
            raise Exception('user input amount not within parameters')
                
    player_entry.delete(0, END)
    
    bj.rounds_played += 1
    player_entry_instruction.configure(text=f'Round of play:{bj.rounds_played}')
    player_entry.configure(state=DISABLED)
    startGame()


def startGame():
    """Set conditions for round start."""
    clearHands()
    start_button.configure(state=DISABLED)
    bj.player_hand.clear()
    bj.dealer_hand.clear()
    dealer_title.configure(text='Dealer\'s Hand Total:' +
                           f'{bj.cardSum(bj.dealer_hand)}')
    player_title.configure(text='Your Hand Total:' +
                           f'{bj.cardSum(bj.player_hand)}')
    bj.startRound()

    root.player_card_0 = ImageTk.PhotoImage(Image.open(getCard(bj.player_hand,
                                                               0)))
    root.player_card_1 = ImageTk.PhotoImage(Image.open(getCard(bj.player_hand,
                                                               1)))
    root.dealer_card_0 = ImageTk.PhotoImage(Image.open(getCard(bj.dealer_hand,
                                                               0)))
    root.dealer_card_1 = ImageTk.PhotoImage(Image.open(getCard(bj.dealer_hand,
                                                               1)))
    dealer_hand_label_0.configure(image=root.dealer_card_0)
    dealer_hand_label_1.configure(image=root.sm_card_back)
    player_hand_label_0.configure(image=root.player_card_0)
    player_hand_label_1.configure(image=root.player_card_1)
    hit_button.configure(state=NORMAL)
    stand_button.configure(state=NORMAL)
    player_title.configure(text='Your Hand Total:' +
                           f'{bj.cardSum(bj.player_hand)}')
    


    if bj.cardSum(bj.player_hand) == 21:
        special_case_button.configure(state=NORMAL, text='Cont',
                                      command=natural21)
        player_entry_instruction.configure(text='You got a Natural 21!')
        hit_button.configure(state=DISABLED)
        stand_button.configure(state=DISABLED)
        player_title.configure(text='Your Hand Total:' +
                               f'{bj.cardSum(bj.player_hand)}')
    else:
        if bj.dealer_hand[0].rank == 14:
            special_case_button.configure(state=NORMAL, text='Insure',
                                          command=insurance)
        if bj.player_hand[0].rank == bj.player_hand[1].rank:
            special_case_button2.configure(state=NORMAL, text='Split',
                                          command=splitPairs)
        if (bj.player_hand[0].rank + bj.player_hand[1].rank) in range(9, 12):
            special_case_button3.configure(state=NORMAL, text='D Down',
                                          command=doubleDown)


def insurance():
    player_entry_instruction.configure(text='Enter your insurance amount')
    player_entry.configure(state=NORMAL, text='')
    special_case_button.configure(text='Enter')
    while True:
        try:
            ins_bet_get = int(player_entry.get())
        except ValueError:
            player_entry_instruction.configure(text='Enter a whole number') 
        if (ins_bet_get * 2) <= bj.player_bet and ins_bet_get > 0:
            bj.insurance(ins_bet_get)
            break
        else:
            player_entry_instruction.configure(text='Enter a # > 0 and' +
                                               f'# < 1/2 of {bj.player_bet}')
            player_entry.delete(0, END)
            raise Exception('user input amount not within parameters')
    if bj.cardSum(bj.dealer_hand) == 21:
        player_entry.delete(0, END)
        dealer_hand_label_1.configure(image=root.dealer_card_1)
        hit_button.configure(state=DISABLED)
        stand_button.configure(state=DISABLED)
        special_case_button.configure(state=DISABLED, text='spesh')
        endGame()
    else:
        special_case_button.configure(state=DISABLED, text='spesh')
        player_entry.delete(0, END)
        bj.rounds_played += 1
        player_entry_instruction.configure(text=f'Round of play:{bj.rounds_played}')
        player_entry.configure(state=DISABLED)

    


def splitPairs():
    pass


def doubleDown():
    pass


def natural21():
    """Set conditions if player has a natural 21."""
    bj.endRound()
    special_case_button.configure(state=DISABLED, text='spesh')
    clearHands()
    endGame()


def hit():
    """Player hit and show card."""
    special_case_button.configure(state=DISABLED, text='spesh')
    special_case_button2.configure(state=DISABLED, text='spesh')
    hit_amount = 0
    for _ in bj.player_hand:
        hit_amount += 1
    bj.playerHit(bj.player_hand)
    if hit_amount == 2:
        root.player_card_2 = ImageTk.PhotoImage(Image.open(getCard(
                                                bj.player_hand, 2)))
        player_hand_label_2.configure(image=root.player_card_2)
    elif hit_amount == 3:
        root.player_card_3 = ImageTk.PhotoImage(Image.open(getCard(
                                                bj.player_hand, 3)))
        player_hand_label_3.configure(image=root.player_card_3)
    elif hit_amount == 4:
        root.player_card_4 = ImageTk.PhotoImage(Image.open(getCard(
                                                bj.player_hand, 4)))
        player_hand_label_4.configure(image=root.player_card_4)
    elif hit_amount == 5:
        root.player_card_5 = ImageTk.PhotoImage(Image.open(getCard(
                                                bj.player_hand, 5)))
        player_hand_label_5.configure(image=root.player_card_5)
    elif hit_amount == 6:
        root.player_card_6 = ImageTk.PhotoImage(Image.open(getCard(
                                                bj.player_hand, 6)))
        player_hand_label_6.configure(image=root.player_card_6)
    elif hit_amount == 7:
        root.player_card_7 = ImageTk.PhotoImage(Image.open(getCard(
                                                bj.player_hand, 7)))
        player_hand_label_7.configure(image=root.player_card_7)
    elif hit_amount == 8:
        root.player_card_8 = ImageTk.PhotoImage(Image.open(getCard(
                                                bj.player_hand, 8)))
        player_hand_label_8.configure(image=root.player_card_8)
    elif hit_amount == 9:
        root.player_card_9 = ImageTk.PhotoImage(Image.open(getCard(
                                                bj.player_hand, 9)))
        player_hand_label_9.configure(image=root.player_card_9)
    elif hit_amount == 10:
        root.player_card_10 = ImageTk.PhotoImage(Image.open(getCard(
                                                 bj.player_hand, 10)))
        player_hand_label_10.configure(image=root.player_card_10)
    else:
        print('hit_amount in hit function not within parameters')
    if bj.cardSum(bj.player_hand) > 21:
        hit_button.configure(state=DISABLED)
        stand_button.configure(state=DISABLED)
        root.dealer_card_1 = ImageTk.PhotoImage(Image.open(getCard(
                                                    bj.dealer_hand, 1)))
        dealer_hand_label_1.configure(image=root.dealer_card_1)
        bj.endRound()
        endGame()
    player_title.configure(text='Your Hand Total:' +
                           f'{bj.cardSum(bj.player_hand)}')


def showDealerCards():
    """Dealer hit and show in GUI."""
    dealer_hand_label_1.configure(image=root.dealer_card_1)
    while bj.cardSum(bj.dealer_hand) < 17:
        dealer_hit = 0
        for _ in bj.dealer_hand:
            dealer_hit += 1
        bj.dealer_hand.append(bj.deck.drawCard())
        if dealer_hit == 2:
            root.dealer_card_2 = ImageTk.PhotoImage(Image.open(getCard(
                                                    bj.dealer_hand, 2)))
            dealer_hand_label_2.configure(image=root.dealer_card_2)
        elif dealer_hit == 3:
            root.dealer_card_3 = ImageTk.PhotoImage(Image.open(getCard(
                                                    bj.dealer_hand, 3)))
            dealer_hand_label_3.configure(image=root.dealer_card_3)
        elif dealer_hit == 4:
            root.dealer_card_4 = ImageTk.PhotoImage(Image.open(getCard(
                                                    bj.dealer_hand, 4)))
            dealer_hand_label_4.configure(image=root.dealer_card_4)
        elif dealer_hit == 5:
            root.dealer_card_5 = ImageTk.PhotoImage(Image.open(getCard(
                                                    bj.dealer_hand, 5)))
            dealer_hand_label_5.configure(image=root.dealer_card_5)
        elif dealer_hit == 6:
            root.dealer_card_6 = ImageTk.PhotoImage(Image.open(getCard(
                                                    bj.dealer_hand, 6)))
            dealer_hand_label_6.configure(image=root.dealer_card_6)
        elif dealer_hit == 7:
            root.dealer_card_7 = ImageTk.PhotoImage(Image.open(getCard(
                                                    bj.dealer_hand, 7)))
            dealer_hand_label_7.configure(image=root.dealer_card_7)
        elif dealer_hit == 8:
            root.dealer_card_8 = ImageTk.PhotoImage(Image.open(getCard(
                                                    bj.dealer_hand, 8)))
            dealer_hand_label_8.configure(image=root.dealer_card_8)
        elif dealer_hit == 9:
            root.dealer_card_9 = ImageTk.PhotoImage(Image.open(getCard(
                                                    bj.dealer_hand, 9)))
            dealer_hand_label_9.configure(image=root.dealer_card_9)
        elif dealer_hit == 10:
            root.dealer_card_10 = ImageTk.PhotoImage(Image.open(getCard(
                                                     bj.dealer_hand, 10)))
            dealer_hand_label_10.configure(image=root.dealer_card_10)
        else:
            print('showDealerCards function not within parameters')


def stand():
    """End round for player."""
    special_case_button.configure(state=DISABLED, text='spesh')
    special_case_button2.configure(state=DISABLED, text='spesh')
    hit_button.configure(state=DISABLED)
    stand_button.configure(state=DISABLED)
    showDealerCards()
    bj.endRound()
    endGame()


def clearHands():
    """Return all card labels to blanks."""
    dealer_hand_label_10.configure(image=root.sm_card_blank)
    dealer_hand_label_9.configure(image=root.sm_card_blank)
    dealer_hand_label_8.configure(image=root.sm_card_blank)
    dealer_hand_label_7.configure(image=root.sm_card_blank)
    dealer_hand_label_6.configure(image=root.sm_card_blank)
    dealer_hand_label_5.configure(image=root.sm_card_blank)
    dealer_hand_label_4.configure(image=root.sm_card_blank)
    dealer_hand_label_3.configure(image=root.sm_card_blank)
    dealer_hand_label_2.configure(image=root.sm_card_blank)
    dealer_hand_label_1.configure(image=root.sm_card_blank)
    dealer_hand_label_0.configure(image=root.card_blank)

    player_hand_label_10.configure(image=root.sm_card_blank)
    player_hand_label_9.configure(image=root.sm_card_blank)
    player_hand_label_8.configure(image=root.sm_card_blank)
    player_hand_label_7.configure(image=root.sm_card_blank)
    player_hand_label_6.configure(image=root.sm_card_blank)
    player_hand_label_5.configure(image=root.sm_card_blank)
    player_hand_label_4.configure(image=root.sm_card_blank)
    player_hand_label_3.configure(image=root.sm_card_blank)
    player_hand_label_2.configure(image=root.sm_card_blank)
    player_hand_label_1.configure(image=root.sm_card_blank)
    player_hand_label_0.configure(image=root.card_blank)


def endGame():
    """Change items in GUI to end round."""
    dealer_title.configure(text='Dealer\'s Hand Total:' +
                           f'{bj.cardSum(bj.dealer_hand)}')
    player_title.configure(text='Your Hand Total:' +
                           f'{bj.cardSum(bj.player_hand)}')
    start_button.configure(state=NORMAL, text='Continue', command=playerBetGet)
    total_money.configure(text=f'Total money: ${bj.player_money}')
    player_entry_instruction.configure(text='Enter a bet amount')
    player_entry.configure(state=NORMAL, text='')


total_money = Label(top_frame, text=f'Total money: ${bj.player_money}')
current_bet = Label(top_frame, text=f'Current bet: ${bj.player_bet}')
start_button = Button(top_frame, text='Start', state=NORMAL,
                      command=totalMoney)
quit_button = Button(top_frame, text='Quit', state=NORMAL, command=closeWindow)
player_entry_instruction = Label(top_frame, text='Press start to begin')
player_entry = Entry(top_frame, state=DISABLED)
hit_button = Button(top_frame, text='Hit', state=DISABLED,
                    command=hit)
special_case_button = Button(top_frame, text='Spesh1', state=DISABLED)
special_case_button2 = Button(top_frame, text='Spesh2', state=DISABLED)
special_case_button3 = Button(top_frame, text ='Spesh3', state=DISABLED)
stand_button = Button(top_frame, text='Stand', state=DISABLED, command=stand)

total_money.grid(row=0, column=1, columnspan=3)
current_bet.grid(row=1, column=1, columnspan=3)
start_button.grid(row=3, column=0)
quit_button.grid(row=3, column=4)
player_entry_instruction.grid(row=4, column=1, columnspan=3)
player_entry.grid(row=5, column=1, columnspan=3)
hit_button.grid(row=6, column=0)
special_case_button.grid(row=7, column=1)
special_case_button2.grid(row=7, column=2)
special_case_button3.grid(row=7, column=3)
stand_button.grid(row=6, column=4)

dealer_title = Label(dealer_title_frame,
                     text=f'Dealer\'s Hand Total: {bj.cardSum(bj.dealer_hand)}'
                     )
player_title = Label(player_title_frame,
                     text=f'Your Hand Total: {bj.cardSum(bj.player_hand)}')

dealer_title.grid(row=0, column=0)
player_title.grid(row=0, column=0)

card_blank = 'images/card_blank.gif'
sm_card_blank = 'images/sm_card_blank.gif'
card_back = 'images/card_back.gif'
sm_card_back = 'images/sm_card_back.gif'
root.card_blank = ImageTk.PhotoImage(Image.open('images/card_blank.gif'))
root.sm_card_blank = ImageTk.PhotoImage(Image.open('images/sm_card_blank.gif'))
root.card_back = ImageTk.PhotoImage(Image.open('images/card_back.gif'))
root.sm_card_back = ImageTk.PhotoImage(Image.open('images/sm_card_back.gif'))

dealer_hand_label_10 = Label(dealer_frame, image=root.sm_card_blank)
dealer_hand_label_10.grid(row=0, column=0)
dealer_hand_label_9 = Label(dealer_frame, image=root.sm_card_blank)
dealer_hand_label_9.grid(row=0, column=1)
dealer_hand_label_8 = Label(dealer_frame, image=root.sm_card_blank)
dealer_hand_label_8.grid(row=0, column=2)
dealer_hand_label_7 = Label(dealer_frame, image=root.sm_card_blank)
dealer_hand_label_7.grid(row=0, column=3)
dealer_hand_label_6 = Label(dealer_frame, image=root.sm_card_blank)
dealer_hand_label_6.grid(row=0, column=4)
dealer_hand_label_5 = Label(dealer_frame, image=root.sm_card_blank)
dealer_hand_label_5.grid(row=0, column=5)
dealer_hand_label_4 = Label(dealer_frame, image=root.sm_card_blank)
dealer_hand_label_4.grid(row=0, column=6)
dealer_hand_label_3 = Label(dealer_frame, image=root.sm_card_blank)
dealer_hand_label_3.grid(row=0, column=7)
dealer_hand_label_2 = Label(dealer_frame, image=root.sm_card_blank)
dealer_hand_label_2.grid(row=0, column=8)
dealer_hand_label_1 = Label(dealer_frame, image=root.sm_card_blank)
dealer_hand_label_1.grid(row=0, column=9)
dealer_hand_label_0 = Label(dealer_frame, image=root.card_blank)
dealer_hand_label_0.grid(row=0, column=10)

player_hand_label_10 = Label(player_frame, image=root.sm_card_blank)
player_hand_label_10.grid(row=0, column=0)
player_hand_label_9 = Label(player_frame, image=root.sm_card_blank)
player_hand_label_9.grid(row=0, column=1)
player_hand_label_8 = Label(player_frame, image=root.sm_card_blank)
player_hand_label_8.grid(row=0, column=2)
player_hand_label_7 = Label(player_frame, image=root.sm_card_blank)
player_hand_label_7.grid(row=0, column=3)
player_hand_label_6 = Label(player_frame, image=root.sm_card_blank)
player_hand_label_6.grid(row=0, column=4)
player_hand_label_5 = Label(player_frame, image=root.sm_card_blank)
player_hand_label_5.grid(row=0, column=5)
player_hand_label_4 = Label(player_frame, image=root.sm_card_blank)
player_hand_label_4.grid(row=0, column=6)
player_hand_label_3 = Label(player_frame, image=root.sm_card_blank)
player_hand_label_3.grid(row=0, column=7)
player_hand_label_2 = Label(player_frame, image=root.sm_card_blank)
player_hand_label_2.grid(row=0, column=8)
player_hand_label_1 = Label(player_frame, image=root.sm_card_blank)
player_hand_label_1.grid(row=0, column=9)
player_hand_label_0 = Label(player_frame, image=root.card_blank)
player_hand_label_0.grid(row=0, column=10)



root.mainloop()
