import os
import sqlite3


class Players():
    def __init__(self):
        self.db_name = None #"dndtest.db"
        self.db = None
        self.cur = None

    ### base    
    def open_db(self, db_name=None):
        if db_name == None:
            print('sys: bad data')
            return
        self.db_name = db_name

        self.db = sqlite3.connect(self.db_name)
        self.cur = self.db.cursor()

    def exit_db(self):
        self.db.close()
        self.cur = None

    def create_tables(self):
        self.cur.execute("CREATE TABLE players(name, class, health, items)")
        self.db.commit()

    def delete_db(self):
        self.exit_db()
        os.remove(self.db_name) 

    def execute_command(self, cmd=''):
        if cmd == '':
            print('sys: bad data')
            return
            
        self.cur.execute(cmd)
        self.db.commit()

    # player
    def add_player(self, data=None):
        if data == None:
            print('sys: bad data')
            return
        self.cur.executemany("INSERT INTO players VALUES(?, ?, ?, ?)", data)
        self.db.commit()

    def del_player(self, player_name=None):
        if player_name == None:
            print('sys: bad data')
            return

        self.cur.execute(f'DELETE FROM players WHERE name="{player_name}"')
        self.db.commit()

        print(f'sys: player {player_name} successfully deleted')

    ### get
    def get_all(self):
        data = self.cur.execute("SELECT name, class, health, items FROM players")
        for i in data:
            print('#'*10, '-'*5, '#'*10)
            for j in i:
                print(j)

    def get_player(self, player_name=None):
        if player_name == None:
            print('sys: bad data')
            return
        
        player = self.cur.execute(f'SELECT class, health FROM players WHERE name="{player_name}"')
        print(f'###     {player_name.capitalize()}     ###')
        for i in player:
            print(f' -class: {i[0]} \n -health: {i[1]}')

    def get_items(self, player_name=None, return_items=False):
        if player_name == None:
            print('sys: bad data')
            return
        
        items = self.cur.execute(f'SELECT items FROM players WHERE name="{player_name}"')

        players_items = list()
        for i in items: # shitcode my beloved
            for j in i:
                for _ in j.split(','):
                    if _ == '' or _ == ' ' or _ == '_':
                        continue
                    players_items.append(_.strip())

        if return_items:
            return players_items

        for i in players_items:
            print(i)        

    ### set
    def add_item(self, player_name=None, item_name=None):
        if player_name == None or item_name == None:
            print('sys: bad data')
            return

        players_items = self.get_items(player_name, True)
        players_items.append(item_name.strip())

        text = str()
        for i in players_items:
            text += i
            text += ','
        
        self.cur.execute(f'UPDATE players SET items="{text}" WHERE name="{player_name}"')
        self.db.commit()

    def del_item(self, player_name=None, item_name=None):
        if player_name == None or item_name == None:
            print('sys: bad data')
            return
        
        players_items = self.get_items(player_name, True)
        ## ToDo - rewrite this shit
        to_pop = None
        for i in range(len(players_items)):
            if players_items[i] == item_name:
                to_pop = i
                break
        if to_pop != None:
            players_items.pop(to_pop)
        ##
        text = str()
        for i in players_items:
            text += i
            text += ','

        self.cur.execute(f'UPDATE players SET items="{text}" WHERE name="{player_name}"')
        self.db.commit()

    def change_health(self, player_name=None, change=0):
        if player_name == None or change == 0:
            print('sys: bad data')
            return

        change *= -1 # invert so i don't have to write minus every time someon took's damage

        health = self.cur.execute(f'SELECT health FROM players WHERE name="{player_name}"')
        for i in health:
            change += i[0]
        
        self.cur.execute(f'UPDATE players SET health="{change}" WHERE name="{player_name}"')
        self.db.commit()

        print(f"{player_name}'s health is now {change}")

