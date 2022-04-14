import pygame as pygame
import sys
import time
import random
pygame.init()

display_width = 900
display_height = 700
background_color = (34,139,34)
grey = (220,220,220)
black = (0,0,0)
green = (0, 200, 0)
red = (255,0,0)
light_slat = (119,136,153)
dark_slat = (47, 79, 79)
dark_red = (255, 0, 0)
pygame.init()
font = pygame.font.SysFont("Arial", 20)
textfont = pygame.font.SysFont('Comic Sans MS', 35)
game_end = pygame.font.SysFont('dejavusans', 100)
blackjack = pygame.font.SysFont('roboto', 70)

SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('BlackJack')
gameDisplay.fill(background_color)
pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 550, 900, 500))


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for value in RANKS:
            for suit in SUITS:
                self.cards.append((value, suit))
  
    def shuffle(self):
        random.shuffle(self.cards)
        

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop()
            
class Hand(Deck):
    def __init__(self):
        self.cards = []
        self.card_img = []
        self.value = 0 

    def add_card(self, card):
        self.cards.append(card)

    def calc_hand(self):
        first_card_index = [a_card[0] for a_card in self.cards]
        non_aces = [c for c in first_card_index if c != 'A']
        aces = [c for c in first_card_index if c == 'A']

        for card in non_aces:
            if card in 'JQK':
                self.value += 10
            else:
                self.value += int(card)

        for card in aces:
            if self.value <= 10:
                self.value += 11
            else:
                self.value += 1


    def display_cards(self):
        for card in self.cards:
            cards = "".join((card[0], card[1]))
            if cards not in self.card_img:
                self.card_img.append(cards)
                
###text object render
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def end_text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
class Play:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        self.gameplaying = False
        
    def blackjack(self):
        self.gameplaying = True
        self.dealer.calc_hand()
        self.player.calc_hand()

        show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
        
        if self.player.value == 21 and self.dealer.value == 21:
            gameDisplay.blit(show_dealer_card, (550, 200))
            black_jack("Both with BlackJack!", 500, 250, grey)
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value == 21:
            gameDisplay.blit(show_dealer_card, (550, 200))
            black_jack("You got BlackJack!", 500, 250, green)
            time.sleep(4)
            self.play_or_exit()
        elif self.dealer.value == 21:
            gameDisplay.blit(show_dealer_card, (550, 200))
            black_jack("Dealer has BlackJack!", 500, 250, red)
            time.sleep(4)
            self.play_or_exit()
            
        self.player.value = 0
        self.dealer.value = 0
        
    def deal(self):
        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())
        self.dealer.display_cards()
        self.player.display_cards()
        self.player_card = 1
        dealer_card = pygame.image.load('img/' + self.dealer.card_img[0] + '.png').convert()
        dealer_card_2 = pygame.image.load('img/back.png').convert()
            
        player_card = pygame.image.load('img/' + self.player.card_img[0] + '.png').convert()
        player_card_2 = pygame.image.load('img/' + self.player.card_img[1] + '.png').convert()

        
        game_texts("Dealer's hand is:", 500, 50)

        gameDisplay.blit(dealer_card, (400, 100))
        gameDisplay.blit(dealer_card_2, (550, 100))

        game_texts("Your's hand is:", 500, 300)
        
        gameDisplay.blit(player_card, (300, 350))
        gameDisplay.blit(player_card_2, (410, 350))
        game_texts("Wallet : ", 250, 580)
        self.blackjack()
        
    def hit(self):
        if not self.gameplaying:
            return
        self.player.add_card(self.deck.deal())
        self.blackjack()
        self.player_card += 1
        
        if self.player_card == 2:
            self.player.calc_hand()
            self.player.display_cards()
            player_card_3 = pygame.image.load('img/' + self.player.card_img[2] + '.png').convert()
            gameDisplay.blit(player_card_3, (520, 450))
                    
        if self.player_card == 3:
            self.player.calc_hand()
            self.player.display_cards()
            player_card_4 = pygame.image.load('img/' + self.player.card_img[3] + '.png').convert()
            gameDisplay.blit(player_card_4, (630, 450))
                    
        if self.player.value > 21:
            game_finish("You Busted!", 500, 250, red)
            time.sleep(4)
            self.play_or_exit()
                
        self.player.value = 0

        if self.player_card > 4:
            sys.exit()
            
    def stand(self):
        if not self.gameplaying:
            return
        show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
        gameDisplay.blit(show_dealer_card, (550, 200))
        self.blackjack()
        self.dealer.calc_hand()
        self.player.calc_hand()
        if self.player.value > self.dealer.value:
            game_finish("You Won!", 500, 250, green)
            time.sleep(3)
            self.play_or_exit()
        elif self.player.value < self.dealer.value:
            game_finish("Dealer Wins!", 500, 250, red)
            time.sleep(3)
            self.play_or_exit()
        else:
            game_finish("It's a Tie!", 500, 250, grey)
            time.sleep(3)
            self.play_or_exit()


    def play_or_exit(self):
            time.sleep(1)
            self.gameplaying = False
            self.player.value = 0
            self.dealer.value = 0
            self.deck = Deck()
            self.deck.shuffle()
            self.dealer = Hand()
            self.player = Hand()
            gameDisplay.fill(background_color)
            pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 550, 900, 500))
            pygame.display.update()

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    TextSurf, TextRect = text_objects(msg, font)
    TextRect.center = ((x + (w/2)), (y + (h/2)))
    gameDisplay.blit(TextSurf, TextRect)
    
def game_texts(text, x, y):
    TextSurf, TextRect = text_objects(text, textfont)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


def game_finish(text, x, y, color):
    TextSurf, TextRect = end_text_objects(text, game_end, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def black_jack(text, x, y, color):
    TextSurf, TextRect = end_text_objects(text, blackjack, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
   
play_blackjack = Play()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        button("Hit / +", 25, 625, 250, 50, light_slat, dark_slat, play_blackjack.hit)
        button("Select / Double", 300, 625, 250, 50, light_slat, dark_slat, play_blackjack.deal)
        button("Stand / -", 600, 625, 250, 50, light_slat, dark_slat, play_blackjack.stand)
    
    pygame.display.flip()

  

 