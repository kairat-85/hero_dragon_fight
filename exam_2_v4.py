import random

dragon = {
    'hp': 2000,
    'defence': 120,
    'str': 150,
    'weapon': 0
}

hero = {
    'hp': 1000,
    'defence': 100,
    'str': 120,
    'weapon': 250,
    'shield': 150,
    'has_shield': False,
    'healing_potion': 1,
    'potion_heal_value': 500
}


def display_dragon_info(d):
    print(f'{"Информация о драконе:":->30}')
    for i in d:
        print('{}: {}'.format(i, d[i]))


def display_hero_info(h):
    print(f'{"Информация о герое:":->30}')
    for i in h:
        print('{}: {}'.format(i, h[i]))


def hero_turn(h, d):
    if random.randint(1, 100) <= 75:
        dmg = -abs(h['str'] + h['weapon'] - d['defence'])
    else:
        dmg = 0
    return dmg


def char_hp_check(char):
    if char['hp'] <= 0:
        char['hp'] = None
    return char['hp']


def input_hero_action():
    return input(
        '\nХод героя (attack(\033[4ma\033[0m), defence(\033[4md\033[0m), pass(\033[4mp\033[0m), heal(\033[4mh\033[0m)): '
    )


def hero_action_attack(h, d):
    dmg = hero_turn(h, d)
    if abs(dmg) > 0:
        modify_health(d, dmg)
        print('Герой нанёс {} ед. урона.'.format(abs(dmg)))
        display_dragon_info(d)
        if char_hp_check(d):
            pass
        else:
            print(
                f'{"=" * 20}\n'
                'У дракона осталось 0 ед. здоровья.\n'
                'Герой победил!'
            )
            exit()
    else:
        print(f'Герой не попал по дракону!')


def hero_action_pass():
    print('Герой пропускает ход!')
    pass


def equip_shield(h):
    if not h['has_shield']:
        h['defence'] = h['defence'] + h['shield']
        h['has_shield'] = True
        print(f'Герой поднимает щит. + {h["shield"]} к показателю брони героя')
        display_hero_info(h)
    else:
        pass


def remove_shield(h):
    if not h['has_shield']:
        pass
    else:
        hero['defence'] = hero['defence'] - hero['shield']
        h['has_shield'] = False
        print(f'\nГерой опускает щит. - {h["shield"]} к показателю брони героя')
        display_hero_info(h)


def dragon_turn(d, h):
    if random.randint(1, 100) <= 50:
        if random.randint(1, 100) <= 50:
            print('Дракон плюётся огненным шаром!')
            dmg = dragon_fire_ball(d, h)
            if abs(dmg) > 0:
                modify_health(hero, dmg)
                print('Дракон нанёс {} ед. урона.'.format(abs(dmg)))
                display_hero_info(h)
            else:
                print('Герой отражает атаку дракона щитом!')
        else:
            dmg = -abs(d['str'] + d['weapon'] - h['defence'])
            modify_health(hero, dmg)
            print('Дракон нанёс {} ед. урона.'.format(abs(dmg)))
            display_hero_info(h)
    else:
        print(f'Дракон проспал ход!')
        dmg = 0
    return dmg


def dragon_fire_ball(d, h):
    if not h['has_shield']:
        dmg = -abs(d['str'] * 2)
    else:
        dmg = 0
    return dmg


def modify_health(a, d):
    if d > 0:
        a['healing_potion'] -= 1
        a['hp'] = a['hp'] + d
        print(
            f'Герой использует зелье лечения. + {a["potion_heal_value"]} ед. к здоровью героя.\n'
            f'Осталось {a["healing_potion"]} ед. зелья.'
        )
        display_hero_info(a)
        if a['healing_potion'] <= 0:
            a['healing_potion'] = 0
    else:
        a['hp'] = a['hp'] + d

    if a['hp'] < 0:
        a['hp'] = 0
    return a


move = 0

while True:
    hero_action = input_hero_action()
    print('')
    if hero_action == 'attack' or hero_action == 'a':
        move += 1
        print(f'\033[4mХод {move}\033[0m. ', end='')
        hero_action_attack(hero, dragon)
    elif hero_action == 'defence' or hero_action == 'd':
        move += 1
        print(f'\033[4mХод {move}\033[0m. ', end='')
        equip_shield(hero)
    elif hero_action == 'pass' or hero_action == 'p':
        move += 1
        print(f'\033[4mХод {move}\033[0m. ', end='')
        hero_action_pass()
    elif hero_action == 'heal' or hero_action == 'h':
        if hero['healing_potion'] == 0:
            print(
                '{:->65}'.format(
                    f'У героя {hero["healing_potion"]} ед. зелий лечения! '
                    'Выберите другое действие.'
                )
            )
            continue
        else:
            move += 1
            print(f'\033[4mХод {move}\033[0m. ', end='')
            modify_health(hero, hero['potion_heal_value'])

    elif hero_action == 'exit':
        print('Выход из программы!')
        exit()
    else:
        print('Введите корректную команду')
        continue

    move += 1
    print('')
    print(f'\033[4mХод {move}\033[0m. ', end='')
    some_dmg = dragon_turn(dragon, hero)

    if char_hp_check(hero):
        pass
    else:
        print(
            f'{"=" * 20}\n'
            'У Героя осталось 0 ед. здоровья.\n'
            'Дракон победил!'
        )
        exit()

    remove_shield(hero)
