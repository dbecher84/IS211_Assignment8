#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Plays a game of Pig with people of the computer"""

import random
import time

random.seed(0)


class Player(object):
    """defines a human player for the game"""
    def __init__(self, player_num):
        """human player constructor"""
        self.player_id = player_num
        self.roll = True
        self.total_score = 0
        self.type = 'human'

    def hold_roll(self):
        """is player rolling or holding"""
        try:
            choice = raw_input('Are you going to hold (h) or roll (r)? ')
            if choice not in ('h', 'r'):
                raise ValueError
            if choice.lower() == 'h':
                self.roll = False
                print 'Turn ended.'
            if choice.lower() == 'r':
                self.roll = True
                print 'Rolling again.'
        except ValueError:
            print 'Not a valid option. Must be h or r.'
            self.hold_roll()

class PCPlayer(Player):
    """defines a computer player for th game"""
    def __init__(self, player_num):
        """computer player constructor"""
        Player.__init__(self, player_num)
        self.type = 'computer'

    def hold_roll(self, response):
        """is computer player holding or rolling"""
        choice = response
        if choice.lower() == 'h':
            self.roll = False
            print 'Turn ended.'
        if choice.lower() == 'r':
            self.roll = True
            print 'Rolling again.'


class Dice(object):
    """defines the dice for the game"""
    def __init__(self):
        """dice constructor"""
        self.rolled_value = None

    def roll(self):
        """random number from 1-6 for dice value"""
        self.rolled_value = random.randint(1, 6)
        return self.rolled_value


class Game(object):
    """sets up the game"""
    def __init__(self, list_players):
        """constructor for Game"""
        self.player_list = list_players
        self.win_score = 100
        #determines starting player. proceeds in order after that.
        self.starting_player = random.randint(1, (len(self.player_list) - 1))
        self.next_player = None
        self.dice = Dice()

        self.current_player = self.player_list[self.starting_player]
        print 'Player {} will go first'.format(self.current_player.player_id)

        self.start_turn(self.current_player)



    def turn_change(self, player):
        """changes the current player"""
        if player.total_score >= self.win_score:
            print 'Player {} has won!'.format(player.player_id)

        else:
            if player.player_id == len(self.player_list):
                self.starting_player = 0
                self.current_player = self.player_list[0]
                self.start_turn(self.current_player)
            else:
                self.starting_player += 1
                self.current_player = self.player_list[self.starting_player]
                self.start_turn(self.current_player)



    def start_turn(self, player):
        """turn for player"""
        turn_score = 0
        count = len(self.player_list) - 1
        print "The current score are."
        while count >= 0:
            print "Player {}'s total score is {}.".format(self.player_list[count].player_id,
                                                          self.player_list[count].total_score)
            count -= 1#prints all current total scores
        print "It is player {}'s turn.".format(player.player_id)

        if player.type == 'human':
            player.roll = True
            while player.roll:

                die_num = self.dice.roll()

                if die_num == 1:
                    print 'You rolled 1 no points gained this time.'
                    player.roll = False
                    turn_score = 0

                else:
                    turn_score = turn_score + die_num
                    print 'You rolled {}'.format(self.dice.rolled_value)
                    print 'Your score this round is {}'.format(turn_score)
                    print 'Your score for the game is {}'.format(player.total_score)
                    player.hold_roll()

        if player.type == 'computer':
            player.roll = True
            hold25 = 25
            hold100 = 100 - player.total_score
            while player.roll:

                die_num = self.dice.roll()

                if die_num == 1:
                    print 'You rolled 1 no points gained this time.'
                    player.roll = False
                    turn_score = 0

                else:
                    turn_score = turn_score + die_num
                    added_total = turn_score + player.total_score
                    print 'You rolled {}'.format(self.dice.rolled_value)
                    print 'Your score this round is {}'.format(turn_score)
                    print 'Your score for the game is {}'.format(player.total_score)
                    if added_total >= 100:
                        player.hold_roll('h')
                    if hold25 < hold100:
                        hold_at = hold25
                    else:
                        hold_at = hold100
                    if hold_at >= turn_score:
                        player.hold_roll('r')
                    else:
                        player.hold_roll('h')

        player.total_score += turn_score
        print 'Your total score is now {}.'.format(player.total_score)

        self.turn_change(player)#switch to next player

def timed():
    """turns timer on and off"""
    time_on = False
    try:
        time_input = raw_input('Will the game be timed? y/n ')
    except ValueError:
        print 'Input must be y or n.'
        timed()
    if time_input.lower() == 'y':
        time_on = True
    return time_on

class Factory(object):
    """Generates human and computer players"""
    def __init__(self):
        self.list_players = []
        self.export_list = []

    def gen_players(self):
        """generates a list of players"""
        count = 1
        for item in self.list_players:
            if item == 'human':
                self.export_list.append(Player(count))
                count += 1
            if item == 'computer':
                self.export_list.append(PCPlayer(count))
                count += 1


def start_game():
    """starts a game"""
    try:
        number_of_players = int(raw_input('Enter the number of human players for the game. '))
    except ValueError:
        print 'Input must be a number.'
        start_game()
    try:
        number_of_pc_players = int(raw_input('Enter the number of computer players for the game. '))
    except ValueError:
        print 'Input must be a number.'
        start_game()

    whos_playing = Factory()
    for num in range(number_of_players):
        whos_playing.list_players.append('human')
    for num in range(number_of_pc_players):
        whos_playing.list_players.append('computer')

    whos_playing.gen_players()
    player_list = whos_playing.export_list

    timer = timed()

    if timer:
        Gameproxy(player_list)
    else:
        Game(player_list)


class Gameproxy(Game):
    """time game class"""
    def __init__(self, list_players):
        self.timed_play_cont = True
        self.start_time = time.time()
        self.game_len = 60
        Game.__init__(self, list_players)

    def time_count(self):
        """turns on timer in game"""
        if time.time() - self.start_time >= self.game_len:
            self.timed_play_cont = False
        else:
            print 'You have {:0.2f} seconds remaining in the game.'.format(self.game_len-
                                                                           (time.time() -
                                                                            self.start_time))

    def turn_change(self, player):
        """changes the current player"""
        if self.timed_play_cont:
            if player.total_score >= self.win_score:
                print 'Player {} has won!'.format(player.player_id)

            else:
                if player.player_id == len(self.player_list):
                    self.starting_player = 0
                    self.current_player = self.player_list[0]
                    self.start_turn(self.current_player)
                else:
                    self.starting_player += 1
                    self.current_player = self.player_list[self.starting_player]
                    self.start_turn(self.current_player)

    def start_turn(self, player):
        """turn for player"""
        turn_score = 0
        count = len(self.player_list) - 1
        print "The current score are."
        while count >= 0:
            print "Player {}'s total score is {}.".format(self.player_list[count].player_id,
                                                          self.player_list[count].total_score)
            count -= 1#prints all current total scores
        print "It is player {}'s turn.".format(player.player_id)

        if player.type == 'human':
            player.roll = True
            while player.roll:

                self.time_count()
                if self.timed_play_cont:
                    die_num = self.dice.roll()

                    if die_num == 1:
                        print 'You rolled 1 no points gained this time.'
                        player.roll = False
                        turn_score = 0

                    else:
                        turn_score = turn_score + die_num
                        print 'You rolled {}'.format(self.dice.rolled_value)
                        print 'Your score this round is {}'.format(turn_score)
                        print 'Your score for the game is {}'.format(player.total_score)
                        player.hold_roll()

                else:
                    player.roll = False
                    print 'Time has Expired.'
                    print 'The final scores are.'
                    count2 = len(self.player_list) - 1
                    while count2 >= 0:
                        print "Player {}'s total score is {}.".format(self.player_list[count2]
                                                                      .player_id,
                                                                      self.player_list[count2]
                                                                      .total_score)
                        count2 -= 1#prints all current total scores
                    return

        if player.type == 'computer':
            player.roll = True
            hold25 = 25
            hold100 = 100 - player.total_score
            while player.roll:

                self.time_count()
                if self.timed_play_cont:
                    die_num = self.dice.roll()

                    if die_num == 1:
                        print 'You rolled 1 no points gained this time.'
                        player.roll = False
                        turn_score = 0

                    else:
                        turn_score = turn_score + die_num
                        added_total = turn_score + player.total_score
                        print 'You rolled {}'.format(self.dice.rolled_value)
                        print 'Your score this round is {}'.format(turn_score)
                        print 'Your score for the game is {}'.format(player.total_score)
                        if added_total >= 100:
                            player.hold_roll('h')
                        if hold25 < hold100:
                            hold_at = hold25
                        else:
                            hold_at = hold100
                        if hold_at >= turn_score:
                            player.hold_roll('r')
                        else:
                            player.hold_roll('h')

                else:
                    player.roll = False
                    print 'Time has Expired.'
                    print 'The final scores are.'
                    count3 = len(self.player_list) - 1
                    while count3 >= 0:
                        print "Player {}'s total score is {}.".format(self.player_list[count3]
                                                                      .player_id,
                                                                      self.player_list[count3]
                                                                      .total_score)
                        count3 -= 1#prints all current total scores
                    return

        player.total_score += turn_score
        print 'Your total score is now {}.'.format(player.total_score)

        self.turn_change(player)#switch to next player


if __name__ == '__main__':
    start_game()
