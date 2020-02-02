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
    return True
