from entitylib2 import *
fond = pygame.image.load("images/fondnfs.png")
playb = pygame.image.load("images/play.png")
quitb = pygame.image.load("images/quit.png")

print("""Key :
arrows : move
space : attack
E : put collected items on vessel
A : drom items collected""")

itemnames = ("valve", "nuclear_core", "piston", "chi", "fan", "gaz", "screw", "dvd")

class item1(Fired):
    size=(50, 50)
    ecoll=False
    speed=0
    dmg=0
    pnbr=0
    def action(self):
        global stack
        stack.append(self.pnbr)
class item2(item1):
    pnbr=1
class item3(item1):
    pnbr=2
class item4(item1):
    pnbr=3
class item5(item1):
    pnbr=4
class item6(item1):
    pnbr=5
class item7(item1):
    pnbr=6
class item8(item1):
    pnbr=7

itemlist = (item1, item2, item3, item4, item5, item6, item7, item8)

def run_menu():
    global core
    resize((600, 600))
    butt = 1
    ouvre = 1
    px = 0
    py = 0
    while ouvre:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                px = event.pos[0]
                py = event.pos[1]
            if px > 200 and px < 400 and py > 300 and py < 400:
                playb = pygame.image.load("images/playa.png")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        resize((512*3, 512*2))
                        return True
            else:
                playb = pygame.image.load("images/play.png")
            if px > 200 and px < 400 and py > 450 and py < 550:
                quitb = pygame.image.load("images/quita.png")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        ouvre = 0
            else:
                quitb = pygame.image.load("images/quit.png")
            if event.type == pygame.QUIT:
                ouvre = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ouvre = 0
                elif event.key == pygame.K_F11:fullscreen()
                elif event.key == pygame.K_F12:screenshoot()
            core.fen.blit(fond, (0, 0))
            core.fen.blit(playb, (200, 300))
            core.fen.blit(quitb, (200, 450))
        pygame.display.flip()
    resize((512*3, 512*2))
    return False
savename = input("Entry save name : ").replace(" ", "-")
superuser = False
if "#" in savename:
    savename, debug = savename.split("#")
    if debug == "sudo":
        print("Build mode enabled")
        superuser = True
        a = 0
        while a < len(core.mappy):
            core.mappy[a] = bytearray(core.mappy[a])
            a+=1
murs = dict()
fd = open("minimap.txt", "r", encoding="Utf-8")
content = fd.read().replace('\r\n', '\n').split('\n\n')
fd.close()

selmur = 0
murname = tuple(murs)
murvals = tuple(murs.values())
applied_items=0
stack=[]

class vaisseau(Obstacle):
    live=100
    size=(190, 190)

class desert_mob(IA):
    img_format = (6,"png")
    dmg=2
    range=500
    xp = 10
    delay = 40*40*3 # 40s
    size=(28, 19)
    live = 10
    sound="worm_damage_seffect.ogg"

class forest_mob(desert_mob):
    size=(31, 32)
    sound="scorpioncul.ogg"

class wrench(Fired):
    size=(50, 50)
    img_format = (4,"png")
    pcoll=False
    speed=10
    delay=20
    sound="un_bruit.ogg"
    dmg=4

class zone_checker(Fired):
    size = (32, 32)
    speed=0
    delay=20

def spawn():
    for s in spawnpoints:
        if randint(0, 14) == 0:
            pos = (s[1] + randint(-spawnrange, spawnrange), s[2] + randint(-spawnrange, spawnrange))
            a = 0
            while a < 5:
                check = zone_checker(pos, s[3:5], (0, 0))
                check.react()
                if check.delay > 0:
                    check.delay = 0
                    break;
                a+=1
            else:
                continue
            if s[0]:
                desert_mob(pos, s[3:5])
            else:
                forest_mob(pos, s[3:5])

class speed(effect):
    name = "speed boost"
    def init_effect(self, entity):
        "action when effect given"
        entity.speed = entity.__class__.speed*(1+self.level/2)
    active_effect=NoWeapon # NoWeapon represent passive function with 2 args
    def end_effect(self, entity):
        "action when effect disappear"
        entity.speed = entity.__class__.speed # règle la vitesse de l'entité sur la vitesse de base de cet entité

class slowness(effect):
    name = "slowness"
    def init_effect(self, entity):
        "action when effect given"
        entity.speed = entity.__class__.speed*(0.8**self.level)
    active_effect=NoWeapon # NoWeapon represent passive function with 2 args
    def end_effect(self, entity):
        "action when effect disappear"
        entity.speed = entity.__class__.speed # règle la vitesse de l'entité sur la vitesse de base de cet entité

class weakness(effect):
    name = "weakness"
    def init_effect(self, entity):
        "action when effect given"
        entity.speed = entity.__class__.speed*(0.8**self.level)
        entity.atk_freq = int(entity.__class__.atk_freq*(1.2**self.level))
    active_effect=NoWeapon # NoWeapon represent passive function with 2 args
    def end_effect(self, entity):
        "action when effect disappear"
        entity.speed = entity.__class__.speed # règle la vitesse de l'entité sur la vitesse de base de cet entité
        entity.atk_freq = entity.__class__.atk_freq # règle la vitesse de l'entité sur la vitesse de base de cet entité

Player.img_format = (3, "png")
init((wrench, vaisseau, desert_mob, forest_mob, zone_checker)+itemlist, (256*6, 256*4))

try:
    dres = pygame.image.load("textures/dialog.png")
except:
    print("Error : cannot load textures/dialog.png")
    dres = None

dbool = False
def dialog():
    global dbool
    pos = (512, 256*3)
    try:
        fd = open("intro.txt", "r", encoding="Utf-8")
        text = fd.read()
        fd.close()
    except:
        text = "The goal is to found and install the pieces of the vessel\nThe pieces were dispatched everywhere\nThere is 8 pieces to found"
    dbool = True
    if not (dres is None):
        core.images.append((dres, pos[0], pos[1]))
    core.images.append((write(text), pos[0] + 64, pos[1] + 64))

vaisseau((32, 32), (0, 0))
tmp = load(savename, (wrench, vaisseau, desert_mob, forest_mob)+itemlist)
if tmp is None:
    # beginner game
    dbool=True
    dialog()
    Player.chunk[0] = 32
    Player.pos[0] = 0
else:
    solved_state, applied_items, stack, core.score = tmp
Player.weapon = wrench # Le joueur lance des projectiles 'arrow'
Player.atk_freq=10 # 10/40 s de délai d'attaque pour le joueurs
player.atk_freq=10
if superuser:
    super_fd = open("minimap.txt", "a", encoding="Utf-8")

spawnpoints = []
spawnrange = 200
a = 1
for m in content[0].split('\n'):
    t = m.split(':')
    murs.__setitem__(t[0], Static(t[1], (int(t[2]), int(t[3])), t[4]))
l = len(content)
while a < l:
    tmp = content[a].split('\n')
    x, y = tmp[0].split(', ')
    xy = (int(x), int(y))
    b = 1
    l2 = len(tmp)
    while b < l2:
        t = tmp[b].split(':')
        if t[0] in ("spawn_desert", "spawn_forest") and not superuser:
            spawnpoints.append((t[0] == "spawn_forest", int(t[1]) + murs[t[0]].size[0]//2, int(t[2]) + murs[t[0]].size[1]//2) + xy)
        elif t[0] in itemnames:
            if dbool:
                print("Put piece")
                itemlist[itemnames.index(t[0])]((int(t[1]), int(t[2])), (xy[0] + 31, xy[1] + 31), (1, 0))
        else:
            murs[t[0]].append((int(t[1]), int(t[2])), xy)
        b+=1
    a+=1

class pipe:
    h = pygame.image.load("image/pipe_right.png").convert_alpha()#1 pour en vertical, 2 pour horizontal
    v = pygame.transform.rotate(h, 90)
    db = pygame.image.load("image/pipe_courbe.png").convert_alpha()#3 pour droite-bas
    gb = pygame.transform.rotate(db, 270)#4 gauche-bas
    du = pygame.transform.rotate(db, 180)#6 droite-haut
    gu = pygame.transform.rotate(db, 90)#5 gauche-haut
    dgu = pygame.image.load("image/pipe_three.png").convert_alpha() #z droite-gauche-haut
    gbu = pygame.transform.rotate(dgu, 270)#y gauche-haut-bas
    dgb = pygame.transform.rotate(dgu, 180)#x droite-gauche-bas
    dub = pygame.transform.rotate(dgu, 90)#u droite-haut-bas

def board(shema):
    global core
    sprite_x = 50
    sprite_y = 50
    for line in shema:
        for car in line:
            if car == '1':
                core.fen.blit(pipe.h, (sprite_x, sprite_y))
            elif car == '2':
                core.fen.blit(pipe.v, (sprite_x, sprite_y))
            elif car == '3':
                core.fen.blit(pipe.db, (sprite_x, sprite_y))
            elif car == '4':
                core.fen.blit(pipe.gb, (sprite_x, sprite_y))
            elif car == '5':
                core.fen.blit(pipe.du, (sprite_x, sprite_y))
            elif car == '6':
                core.fen.blit(pipe.gu, (sprite_x, sprite_y))
            elif car == 'z':
                core.fen.blit(pipe.dgu, (sprite_x, sprite_y))
            elif car == 'y':
                core.fen.blit(pipe.gbu, (sprite_x, sprite_y))
            elif car == 'x':
                core.fen.blit(pipe.dgb, (sprite_x, sprite_y))
            elif car == 'u':
                core.fen.blit(pipe.dub, (sprite_x, sprite_y))
            pygame.display.flip()
            sprite_x = sprite_x + 50
        sprite_x = 50
        sprite_y = sprite_y + 50

class enigme_pipe:
    def run():
        global core
        resize((1000, 600))
        wall = pygame.image.load("image/mur.png").convert_alpha()
        fond = pygame.image.load("image/fond.png").convert_alpha()
        batterie = pygame.image.load("image/batterie.png").convert_alpha()
        select = pygame.image.load("image/selecteur.png").convert_alpha()
        gear = pygame.image.load("image/gear.png").convert_alpha()
        voyant_rouge = pygame.image.load("image/red.png").convert_alpha()
        voyant_vert = pygame.image.load("image/green.png").convert_alpha()
        voyant = voyant_rouge
        select_x = 0
        select_y = 0
        select_pos_x = 50
        select_pos_y = 50
        file = open("map/pipe_one.txt","r+")
        shema = []
        for line in file:
            line_shema = []
            for car in line:
                if car != '\n':
                    line_shema.append(car)
            shema.append(line_shema)

        core.fen.blit(fond, (0, 0))
        board(shema)
        core.fen.blit(voyant, (0, 0))
        core.fen.blit(select, (select_pos_x, select_pos_y))

        file.close()
        loop_enigme_one = True
        frame = time()
        while loop_enigme_one:
            frame += 0.04#frame
            T = frame - time()#frame
            if T > 0:sleep(T)#frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop_enigme_one = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN and select_y < 9:
                        select_y = select_y + 1
                        select_pos_y = select_pos_y + 50
                    elif event.key == pygame.K_UP and select_y > 0:
                        select_y = select_y - 1
                        select_pos_y = select_pos_y - 50
                    elif event.key == pygame.K_RIGHT and select_x < 9:
                        select_x = select_x + 1
                        select_pos_x = select_pos_x + 50
                    elif event.key == pygame.K_LEFT and select_x > 0:
                        select_x = select_x - 1
                        select_pos_x = select_pos_x - 50
                    elif event.key == pygame.K_SPACE:
                        voyant = voyant_rouge
                        if  shema[1][0] == '6' and shema[1][1] == '4' and shema[2][1] == '1' and shema[3][0] == '3' and shema[3][1] == '5' and shema[4][0] == '1' and shema[5][0] == '6' and shema[5][1] == '2' and shema[5][2] == '4' and shema[5][5] == '3' and shema[5][6] == '2' and shema[5][7] == '4':
                            if  shema[6][2] == '6' and shema[6][3] == '2' and shema[6][4] == '2' and shema[6][5] == '5' and shema[6][7] == '1' and shema[7][7] == '1' and shema[8][3] == '3' and shema[8][4] == '2' and shema[8][5] == '2' and shema[8][6] == '2' and shema[8][7] == '5':
                                if  shema[9][3] == '6' and shema[9][4] == '2' and shema[9][5] == '2' and shema[9][6] == '2' and shema[9][7] == '2' and shema[9][8] == '2':
                                    voyant = voyant_vert
                                    loop_enigme_one = False
                                    resize((512*3, 512*2))
                                    return True
                    elif event.key == pygame.K_F11:fullscreen()
                    elif event.key == pygame.K_F12:screenshoot()
                    elif event.key == pygame.K_RETURN:
                        if shema[select_y][select_x] == '1':
                            shema[select_y][select_x] = '2'
                        elif shema[select_y][select_x] == '2':
                            shema[select_y][select_x] = '1'
                        elif shema[select_y][select_x] == '3':
                            shema[select_y][select_x] = '4'
                        elif shema[select_y][select_x] == '4':
                            shema[select_y][select_x] = '5'
                        elif shema[select_y][select_x] == '5':
                            shema[select_y][select_x] = '6'
                        elif shema[select_y][select_x] == '6':
                            shema[select_y][select_x] = '3'
                        elif shema[select_y][select_x] == 'z':
                            shema[select_y][select_x] = 'y'
                        elif shema[select_y][select_x] == 'y':
                            shema[select_y][select_x] = 'x'
                        elif shema[select_y][select_x] == 'x':
                            shema[select_y][select_x] = 'u'
                        elif shema[select_y][select_x] == 'u':
                            shema[select_y][select_x] = 'z'
                    core.fen.blit(fond, (0, 0))
                    core.fen.blit(voyant, (0, 0))
                    board(shema)
                    core.fen.blit(select, (select_pos_x, select_pos_y))
                pygame.display.flip()
        resize((512*3, 512*2))
        return False

def run_minigame():
    width, height = 700, 700
    resize((width, height))
    #--------resources_call--------#
    background = pygame.image.load("ressources/wood_back.png")
    tape = pygame.image.load("ressources/tape.png")
    screw = pygame.image.load("ressources/screw.png")
    rusty = pygame.image.load("ressources/rusty_metal.png")
    wire = pygame.image.load("ressources/copper_wire.png")
    plastic =  pygame.image.load("ressources/plastic.png")
    box = pygame.image.load("ressources/box.png")
    hole = pygame.image.load("ressources/hole.png")
    #------position_defining-------#
    tape_pos = (100,100)
    screw_pos = (160,100)
    rusty_pos = (240,100)
    wire_pos = (310,100)
    plastic_pos = (380,100)
    metalb_pos = (550, 400)
    plasticb_pos = (150, 400)
    #-----initializing_follow------#
    follow1 = False
    follow2 = False
    follow3 = False
    follow4 = False
    follow5 = False
    #-----initializing_victory-----#
    victory1 = False
    victory2 = False
    victory3 = False
    victory4 = False
    victory5 = False
    #-------frame_rate_limit-------#
    timer = time()
    loop = True
    mouse_pos = (100,100)
    while loop:
    #--------victory_test--------#
        if tape_pos[0] + 30 > plasticb_pos[0] - 10 and tape_pos[0] + 30 > plasticb_pos[0] - 10 and tape_pos[1] + 30 > plasticb_pos[1] - 10 and tape_pos[1] + 30 > plasticb_pos[1] - 10:
            print("tape")
            victory1 = True
        if screw_pos[0] + 30 > metalb_pos[0] - 10 and screw_pos[0] + 30 > metalb_pos[0] - 10 and screw_pos[1] + 30 > metalb_pos[1] - 10 and screw_pos[1] + 30 > metalb_pos[1] - 10:
            print("screw")
            victory2 = True
        if screw_pos[0] + 30 > metalb_pos[0] - 10 and rusty_pos[0] + 30 > metalb_pos[0] - 10 and rusty_pos[1] + 30 > metalb_pos[1] - 10 and rusty_pos[1] + 30 > metalb_pos[1] - 10:
            print("rusty")
            victory3 = True
        if wire_pos[0] + 30 > metalb_pos[0] - 10 and wire_pos[0] + 30 > metalb_pos[0] - 10 and wire_pos[1] + 30 > metalb_pos[1] - 10 and wire_pos[1] + 30 > metalb_pos[1] - 10:
            print("wire")
            victory4 = True
        if tape_pos[0] + 30 > plasticb_pos[0] - 10 and plastic_pos[0] + 30 > plasticb_pos[0] - 10 and plastic_pos[1] + 30 > plasticb_pos[1] - 10 and plastic_pos[1] + 30 > plasticb_pos[1] - 10:
            print("plastic")
            victory5 = True
        mouse_pos = pygame.mouse.get_pos()
    #-------order_to_follow--------#
        if follow1:
            tape_pos = mouse_pos
        else:
            tape_pos == (100,100)
        if follow2:
            screw_pos = mouse_pos
        else:
            screw_pos == (100,100)
        if follow3:
            rusty_pos = mouse_pos
        else:
            rusty_pos == (100,100)
        if follow4:
            wire_pos = mouse_pos
        else:
            wire_pos == (100,100)
        if follow5:
            plastic_pos = mouse_pos
        else:
            plastic_pos == (100,100)
    #----------apply_pos---------#
        core.fen.fill(0)
        core.fen.blit(background, (0,0))
        core.fen.blit(box, metalb_pos)
        core.fen.blit(box, plasticb_pos)
        core.fen.blit(tape, tape_pos)
        core.fen.blit(screw, screw_pos)
        core.fen.blit(rusty, rusty_pos)
        core.fen.blit(wire, wire_pos)
        core.fen.blit(plastic, plastic_pos)
    #-------kingdom_hearts-------#
        pygame.display.flip()
        timer += .02
        if (timer > time()):
            sleep(timer - time())
        if victory1 == True and victory2 == True and victory3 == True and victory4 == True and victory5 == True:
            loop = False
            return True
            break
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                loop = False
                return False
                break
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > tape_pos[0] - 10 and event.pos[0] < tape_pos[0] + 70 and event.pos[1] > tape_pos[1] - 10 and event.pos[1] < tape_pos[1] + 70:
                    follow1 = not follow1
                elif event.pos[0] > screw_pos[0] - 10 and event.pos[0] < screw_pos[0] + 70 and event.pos[1] > screw_pos[1] - 10 and event.pos[1] < screw_pos[1] + 70:
                    follow2 = not follow2
                elif event.pos[0] > rusty_pos[0] - 10 and event.pos[0] < rusty_pos[0] + 70 and event.pos[1] > rusty_pos[1] - 10 and event.pos[1] < rusty_pos[1] + 70:
                    follow3 = not follow3
                elif event.pos[0] > wire_pos[0] - 10 and event.pos[0] < wire_pos[0] + 70 and event.pos[1] > wire_pos[1] - 10 and event.pos[1] < wire_pos[1] + 70:
                    follow4 = not follow4
                elif event.pos[0] > plastic_pos[0] - 10 and event.pos[0] < plastic_pos[0] + 70 and event.pos[1] > plastic_pos[1] - 10 and event.pos[1] < plastic_pos[1] + 70:
                    follow5 = not follow5
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:fullscreen()
                elif event.key == pygame.K_F12:screenshoot()
    return True

solved_state = 0
selecting=False
continuer=run_menu()
while continuer:
    if dbool and core.timer >= 1:
        dbool=False
        del core.images[0]
        if len(core.images) > 0:
            del core.images[0]
    if core.tic % 120 == 0:
        spawn()
    if len(stack) and core.tic % 20 == 0:
        Player.apply(weakness, 21, len(stack))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                Player.move[0] = 1
                Player.dir = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                Player.move[0] = -1
                Player.dir = 2
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                Player.move[1] = 1
                Player.dir = 1
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                Player.move[1] = -1
                Player.dir = 3
            elif event.key == pygame.K_SPACE:tir()
            elif event.key == pygame.K_F12:screenshoot()
            elif event.key == pygame.K_TAB:
                save(savename, (solved_state, applied_items, stack, core.score));print("Game saved.")
                if superuser:
                    super_fd.close()
                    super_fd = open("minimap.txt", "a", encoding="Utf-8")
            elif event.key == pygame.K_ESCAPE:
                continuer=run_menu()
            elif event.key == pygame.K_e and Player.chunk[0] >= 30 and Player.chunk[0] <= 32 and Player.chunk[1] >= 30 and Player.chunk[1] <= 32:
                # place action
                print("Pièce(s) placée(s) dans le vaisseau.")
                applied_items+=len(stack)
                stack.clear()
                if solved_state == 0 and (applied_items >= 4 or superuser):solved_state += enigme_pipe.run()
                elif solved_state == 1 and (applied_items >= 8 or superuser):
                    if run_minigame():
                        continuer = False
                        print("YOU WIN !")
                    resize((512*3, 512*2))
            elif event.key == pygame.K_q and len(stack) > 0:
                # drop action
                print("Drop d'un item")
                print(stack)
                itemlist[stack.pop()]((Player.pos[0] - Player.move[0] * 72, Player.pos[1] - Player.move[1] * 72), tuple(Player.chunk), tuple(Player.move))
            elif event.key == pygame.K_F11:fullscreen()
            elif event.key == pygame.K_c:
                tmp = input("Command : ")
                if "(" in tmp or "=" in tmp:
                    try:exec(tmp)
                    except:print("Commande inconnue")
                else:
                    try:print(eval(tmp))
                    except:print("Donnée inconnue")
            elif event.key == pygame.K_b and superuser:
                core.mappy[Player.chunk[1]][Player.chunk[0]] += 1
                if core.mappy[Player.chunk[1]][Player.chunk[0]] - 48 == len(core.img_base):
                    core.mappy[Player.chunk[1]][Player.chunk[0]] = 48
                core.img[Player.chunk[1]][Player.chunk[0]] = core.img_base[core.mappy[Player.chunk[1]][Player.chunk[0]] - 48]
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if Player.move[0] == 1:
                    Player.move[0] = 0
                    if Player.move[1]:
                        Player.dir = Player.move[1]%4
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if Player.move[0] == -1:
                    Player.move[0] = 0
                    if Player.move[1]:
                        Player.dir = Player.move[1]%4
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if Player.move[1] == 1:
                    Player.move[1] = 0
                    if Player.move[0]:
                        Player.dir = (Player.move[0]-1)%4
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if Player.move[1] == -1:
                    Player.move[1] = 0
                    if Player.move[0]:
                        Player.dir = (Player.move[0]-1)%4
        elif event.type == pygame.QUIT: # On clique sur la croix pour quitter
            continuer=False
        elif superuser:
            if event.type == pygame.MOUSEMOTION and selecting:
                core.images[-1][1] = pygame.mouse.get_pos()[0]
                core.images[-1][2] = pygame.mouse.get_pos()[1]
                Player.pos[0] = int(Player.pos[0])
                Player.pos[1] = int(Player.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Place bloc
                    if selecting:del core.images[-1]
                    core.images.append([murvals[selmur].img] + list(event.pos))
                    selecting = True
                    Player.pos[0] = int(Player.pos[0])
                    Player.pos[1] = int(Player.pos[1])
                elif event.button == 2:
                    # Select another bloc
                    if selecting:
                        del core.images[-1]
                    selmur += 1
                    if selmur == len(murname):
                        selmur = 0
                    print("selected :", murname[selmur])
                    if selecting:
                        core.images.append([murvals[selmur].img] + list(event.pos))
                elif event.button == 3 and selecting:
                    # Abort placement
                    del core.images[-1]
                    selecting = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and selecting:
                    # Save placement
                    pos = (int(-core.size[0] + Player.size[0]//2 + Player.pos[0] + core.dec[0] * 256 + event.pos[0]),
                           int(-core.size[1] + Player.size[1]//2 + Player.pos[1] + core.dec[1] * 256 + event.pos[1]))
                    chunk = (Player.chunk[0] + pos[0]//256-31, Player.chunk[1] + pos[1]//256-31)
                    murvals[selmur].append((pos[0]%256, pos[1]%256), chunk)
                    super_fd.write("\n\n"+str(chunk[0])+", "+str(chunk[1])+"\n"+murname[selmur]+":"+str(pos[0]%256)+":"+str(pos[1]%256))
                    del core.images[-1]
                    selecting = False
    Refresh()
    if Player.live <= 0:
        pygame.display.quit() # Ferme la fenêtre pygame
        break
    elif Player.live < 20:
        Player.live += 0.001 # 25s par point de vies

if superuser:
    super_fd.close()
    fd = open("map.txt", 'wb')
    i = iter(core.mappy)
    fd.write(next(i))
    for a in i:
        fd.write(b'\n' + a)
    fd.close()

if continuer: # On est mort ou c'est juste que l'on a quitté le jeu ?
    # Actions à effectuer après la mort du joueur :
    print("Game Over")
else:
    # Actions à effectuer après avoir quitté le jeu
    pygame.display.quit()
    print("À bientôt :)")
    save(savename, (solved_state, applied_items, stack, core.score))
