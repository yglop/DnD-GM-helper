from players import Players

pdb = Players() # players data base

help_msg = '''
    Connect  -   for connecting to or creating data base
    Exit    -   for exit (-:
    Create  -   for creating players table
    Execute -   if you ever need to execude sql command directly

    player commands:
        add [pN]     -   for adding player
        p [pN]       -   for deleting player
    
    get commands:
        a            -   to get all the data in the base 
        i [pN]       -   to get player's item's
        p [pN]       -   to get data about player (excluding item's)

    set commands:
        ia [pN] [iN] -   for adding item to player
        id [pN] [iN] -   for deleting an item
        h  [pN] [val]-   to damage or heal player

    ###
    [pN] - player's name
    [iN] - item's name
    ###
    '''

# it's unsafe only if you dont know what you are doing
# i wrote it for myself
# i know what am i doing
## call it shitcode if you wish
## it's working fine and i am okay with it
def loop(text):         
    text = text.strip()
    if len(text) == 0:
        return

    if text == 'Help':
        print(help_msg)

    if text == 'Connect':
        print('sys: enter db name')
        name = input() 
        if name == '':
            return
        pdb.open_db(name)
        print(f'sys: connected to {name}')
        return

    if text == 'Exit':
        pdb.exit_db()
        running = False
        print('yglop: hope you had a good game!')
        return

    if text == 'Create':
        pdb.create_tables()
        print('sys: tables for players created')
        return

    if text == 'Execute':
        print('sys: enter sql command')
        pdb.execute_command(input())
        return

    text = text.split(' ')
    if len(text) < 2:
        return

    if text[0] == 'player':
        if text[1] == 'add':
            pdb.add_player([tuple(text[2:]),])
            print(f'sys: player {text[2]} created')
        elif text[1] == 'del':
            pdb.del_player(text[2])

        print('sys: del command was executed') # debug
        return

    if text[0] == 'get':
        if text[1] == 'a' or text[1] == 'all':
            pdb.get_all()
        elif text[1] == 'i' or text[1] == 'item':
            pdb.get_items(text[2])
        elif text[1] == 'p' or text[1] == 'player':
            pdb.get_player(text[2])

        print('sys: get command was executed') # debug
        return

    if text[0] == 'set':
        if text[1] == 'ia':
            item_name = str()
            for i in text[3:]:
                item_name += i
                item_name += ' '
            pdb.add_item(text[2], item_name.strip())
            print(f'sys: item ({item_name.strip()}) added to player {text[2]}')
        elif text[1] == 'id':
            item_name = str()
            for i in text[3:]:
                item_name += i
                item_name += ' '
            pdb.del_item(text[2], item_name.strip())
            print(f'sys: item ({item_name.strip()}) belonging to {text[2]} was deleted')
        elif text[1] == 'h' or text[1] == 'health':
            pdb.change_health(text[2], text[3])
        print('sys: set command was executed') # debug
        return


running = True
print('\nsys: awaiting input \nsys: Write "Help" if you need any\n')
while running:
    loop(input())
