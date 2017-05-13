import random

suitlist = ["Diamonds", "Spades", "Hearts", "Clubs"]
special_cardlist = ["King", "Queen", "Jack", "Ace"]


class Card:
    def __init__(self, suit_type, value = 10, is_special_card = False, special_card = None):
        self.suit_type = suit_type
        self.value = value
        self.special_card = None
        
        if is_special_card:
            self.is_special_card = is_special_card
            self.special_card = special_card
            
            if special_card == "Ace":
                self.value = 1
              
    def __str__(self):
            return str(self.value) + " "+ str(self.suit_type) +" "+ str(self.special_card)
          

class Deck:
    def __init__(self):
        self.cardlist = [] 
        
        for suit in suitlist:
            self.create_suit(suit)
          
    def create_suit(self, suit_type):
        for value in range(2,11):
            card = Card(suit_type, value)
            self.cardlist.append(card)
      
        for special_card in special_cardlist:
            card = Card(suit_type, value, is_special_card = True, special_card = special_card)
            self.cardlist.append(card)
            
    def shuffle(self):
        random.shuffle(self.cardlist)
        
    def print_cards(self):
        for card in self.cardlist:
            print(card)
            
    def get_cards(self, num_cards):
        card_list = []
        for i in range(0,num_cards):
            card_list.append(self.cardlist.pop())
        return card_list
    
    def put_cards(self, card_list):
        for card in card_list:
            self.cardlist.append(card)
            
class Player:
    def __init__(self, name, bankroll = 100):    
        self.name = name
        self.total = 0
        self.bankroll = bankroll
        self.cardlist = []
        self.ace = False
        self.bet_amount = 5
        self.min_bet_amount = 5
        
    def get_name(self):
        return self.name

    def put_cards(self, card_list):
        for card in card_list:
            self.cardlist.append(card)
        print(self.accrue_total())
             
    def get_cards(self):
        cardlist = []
        for card in self.cardlist:
            cardlist.append(self.cardlist.pop())
        return cardlist
       
    def print_cards(self):
        for card in self.cardlist:
            print(card)
                
    def accrue_total(self):
        self.total = 0
        """ if the player is dealer ace value should be selected automatically as 1 or 11"""
        for card in self.cardlist:
            print(card)
            if card.special_card == "Ace" and self.total < 11:
                self.total += (card.value + 10)
                #self.ace = True
            else:
                self.total += card.value
                
        return self.total
    
    
    def get_total(self):
        return self.total
    
    def bet_money(self,player,min_bet_amount):
        self.bet_amount = int(input("Enter the bet amount"))
        while True:
            if self.bet_amount > min_bet_amount:
                if self.bet_amount < self.bankroll:
                    self.decrease_bankroll()
                    break
                else:
                    print("Enter bet amount less than %d" %self.bankroll)
                    self.bet_amount = int(input("Enter the bet amount"))
            else:
         
                print("Enter bet min bet amount as %d" %self.min_bet_amount)
                self.bet_amount = int(input("Enter the bet amount"))
            continue 
        
    def set_bankroll(self,bankroll):
        self.bankroll = bankroll  
        
    def get_bankroll(self):  
        return self.bankroll 
    
    def accure_bankroll(self, status): 
        print("Inside accure bank roll")
        if status == "BJplayer":
            print("BJ success Natural")
            self.bankroll += self.bet_amount*1.5*2
            print(self.bankroll)
        elif status == "BJdealer":
            print("BJ success dealer")
            self.bankroll += self.bet_amount*1.5*2
            print(self.bankroll)
        elif status == "tie":
            self.bankroll += self.bet_amount
            
        elif status == "PBsuccess":
            self.bankroll += self.bet_amount*2
            
        elif status == "DBsuccess":
            self.bankroll += self.bet_amount*2  
        
        else:
            print("bankroll before accrue %s" %self.bankroll)
            self.bankroll += self.bet_amount*2
            print("bankroll after accrue %s" %self.bankroll) 
            print(self.bankroll)
            print("Normal success")
        
    def decrease_bankroll(self): 
        print("Inside decrease bank roll")    
        self.bankroll = self.bankroll - self.bet_amount
        
    def print_bankroll(self):
        print("Inside print bank roll")
        print(self.name,self.bankroll)

class BlackJack:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.min_bet_amount = 0        
        self.playerlist = []
        self.create_player("Sam",1000)
        self.create_player("dealer", 1000)
          
    def create_player(self, name, bankroll):
        player = Player(name, bankroll)
        self.playerlist.append(player)
        
    def find_player(self, playername):
        for player in self.playerlist:
            if player.name == playername:
                return player
        return None
    
    def start_game(self,player):
        player.bet_money(self,self.min_bet_amount)
    
    
    def give_cards(self, player, num_cards):
        player_cardlist = []
        if player != None:
            player_cardlist = self.deck.get_cards(num_cards)
            if player_cardlist:
                player.put_cards(player_cardlist)
                player.print_cards()
        
    def dole(self, player):
        self.give_cards(player, 2)
            
    def hit(self, player): 
        self.give_cards(player, 1)

    def check_blackjack(self, player, dealer): 
        # to check if the total value is equal to 21 then black jack     
        status = "None"
        if player.get_total() == 21 and dealer.get_total() == 21:
            print("tie or PUSH")
            status = "tie"
            player.accure_bankroll(status)
            
        elif player.get_total() == 21:
            print(str(player.name) + " BLACK JACK Winner")
            status = "BJplayer"
            player.accure_bankroll(status)
            player.print_bankroll()    
            dealer.print_bankroll()
            
        elif dealer.get_total() == 21:
            print(str(player.name) + " BLACK JACK Winner")
            status = "BJdealer"
            dealer.accure_bankroll(status)
            dealer.print_bankroll()
            player.print_bankroll()
        else:
            status = "failure"  
            
        return status
           
    def check_bust(self, player, dealer):   
        #to check if the total is greater than 21 then busts player or dealer cannot play, break stop the game
        if player.get_total() > 21:
                status = "PBsuccess"
                print(str(player.name) +" BUSTS loses") 
                player.print_bankroll()
                dealer.accure_bankroll(status)
                dealer.print_bankroll()
                
        elif dealer.get_total() > 21:
                status = "DBsuccess"
                print(str(dealer.name) +" BUSTS loses") 
                dealer.decrease_bankroll()
                player.print_bankroll()
                dealer.print_bankroll()
                
        else:
            player.print_bankroll()
            status = "failure"
            
        return status
    
    
    def choose_hit_stand(self, player):
        #if total less than 21, the player or dealer can choose hit or stand. If dealer choose stand then break
        #check for the ace if ace then give 1 or 11
        if player.name == "dealer":
            if player.get_total() < 17:
                bj.hit(player)
                status = bj.check_blackjack(player,dealer)
                if status == "BJdealer":
                    print("Dealer has BLACK JACK")
                bust_status = bj.check_bust(player,dealer)
                if bust_status == "DBsuccess":
                    print("Dealer Busts")
                
        else:        
            while True:
                if player.get_total() < 21:
                    action = input("Choose either to HIT or STAND:")
                    if action == "HIT":
                        bj.hit(player)
                        status1 = bj.check_blackjack(player,dealer)
                        if status1 == "BJplayer":
                            print("Player has BLACK JACK")
                        bust_status = bj.check_bust(player,dealer)
                        if bust_status == "PBsuccess":
                            print("Player Busts")
                        continue
                    elif action == "STAND":
                        break
                    else:
                        pass

    def check_winner(self, player, dealer):
        #check the who is the winner of the game. Check the total points got from the player and the
        #dealer and return who is the winner
        status = "None"
        if player.get_total() < 21 and dealer.get_total() < 21:
            if player.get_total() == dealer.get_total():
                print("TIE")
                status = "tie"
                player.accure_bankroll(status)
                player.print_bankroll()
                dealer.print_bankroll()
                
            
            elif player.get_total() > dealer.get_total():
                status = "success"
                player.accure_bankroll(status)
                print("Player is the winner")
                player.print_bankroll()
            
            else:
                status = "success"
                dealer.accure_bankroll(status)
                print("Dealer is the winner")
                dealer.print_bankroll()
                
        return status       
        
      
    def play_game_again(self):
        #ask the player do you want to play the game again
        pass 
        
bj = BlackJack()

print("Finding the player")
player = bj.find_player("Sam")
bj.start_game(player)
print("Player is getting 2 cards")
bj.dole(player)


print("Finding the dealer")
dealer = bj.find_player("dealer")
print("dealer is getting two cards")
bj.dole(dealer)

status = bj.check_blackjack(player,dealer)
if status == "BJplayer":
    print("Player has BLACK JACK")
    # Dealer might want another card to see if he gets a black jack
elif status == "BJdealer":
    print("Dealer has BLACK JACK")   
    # Hit and try to see if the player gets a black jack 
elif status == "tie":
    print("TIE or PUSH, both dealer and player has BLACK JACK")
    
elif status == "failure":
    pass

status = bj.check_bust(player,dealer)
if status == "PBsuccess":
    print("Player Busts")

elif status == "DBsuccess":
    print("Dealer Busts")   
    
elif status == "failure":
    pass



    
print("player is choosing to hit or stand")
bj.choose_hit_stand(player)
print("dealer is choosing to hit or stand")
bj.choose_hit_stand(dealer)
status = bj.check_winner(player, dealer)
if status == "success":
    print("Winner")
elif status == "tie":
    print("Push or tie")


##Problems

# dealer should show only one card not two (In print use num)
# Reset the deck add get and put to the code
# How to play the next game
# Bet i.e money to be given and taken chips
#https://github.com/jmportilla/Complete-Python-Bootcamp