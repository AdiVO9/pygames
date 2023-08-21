import pygame
from random import choice
from sys import exit

pygame.init()

screen = pygame.display.set_mode((810, 810))
pygame.display.set_caption("Tic Tac Toe")
screen.fill("#1fe0c7")

cross = pygame.image.load("cross.png")
cross = pygame.transform.scale(cross, (170, 170))

plays_blocked = []

areas = []


# Class
class Area:
    def __init__(self, top_left: tuple, dims: tuple, refer: int):
        self.top_left = top_left
        self.dims = dims
        self.refer = refer

        self.filled = False
        self.oc = None
        self.colour = None
        self.centre = (self.top_left[0] + self.dims[0] / 2, self.top_left[1] + self.dims[1] / 2)
        self.rect = pygame.Rect(self.top_left, self.dims)

    def check_mouse_collide(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            return True

        else:
            return False


# Functions
def setup():
    screen.fill("#1fe0c7")

    areas.append(Area((0, 0), (270, 270), 0))
    areas.append(Area((278, 0), (270, 270), 1))
    areas.append(Area((548, 0), (270, 270), 2))

    areas.append(Area((0, 270), (270, 270), 3))
    areas.append(Area((270, 270), (270, 270), 4))
    areas.append(Area((540, 270), (270, 270), 5))

    areas.append(Area((0, 540), (270, 270), 6))
    areas.append(Area((270, 540), (270, 270), 7))
    areas.append(Area((540, 540), (270, 270), 8))

    pygame.draw.line(screen, "#10a18d", (0, 270), (810, 270), 8)
    pygame.draw.line(screen, "#10a18d", (0, 540), (810, 540), 8)
    pygame.draw.line(screen, "#10a18d", (270, 0), (270, 810), 8)
    pygame.draw.line(screen, "#10a18d", (540, 0), (540, 810), 8)


def check_collide_areas():
    for a in areas:
        if a.check_mouse_collide():
            return a.refer


def draw_move(loc: tuple, circle_turn: bool):
    if circle_turn:
        pygame.draw.circle(screen, "#ffffeb", loc, 90, 15)

    else:
        try:
            screen.blit(cross, cross.get_rect(center=loc))

        except TypeError:
            pass


def auto_pick():
    avail = []
    for i in areas:
        if not i.filled:
            avail.append((i, i.oc))

    player_circles = []
    for j in areas:
        if j.oc == "Circle":
            player_circles.append(j.refer)

    print("Player: " + str(player_circles))

    if len(avail) > 0:
        # Improve AI here:
        if len(player_circles) >= 2:
            check = defense_check(player_circles)

        else:
            check = [False]

        print("Check: " + str(check))
        if check[0]:
            if not areas[check[1]].filled:
                comp_choice = areas[check[1]]

            else:
                comp_choice = choice(avail)[0]

        else:
            comp_choice = choice(avail)[0]

        comp_choice.filled = True
        comp_choice.oc = "Cross"
        comp_choice.colour = "#424242"

        return comp_choice.centre


def check_win():
    win_combs = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (6, 4, 2))

    for w in win_combs:
        winner = match(w)
        if winner[0]:
            pygame.draw.line(screen, winner[4], winner[2].centre, winner[3].centre, 25)
            return winner

    return False, None, None, None, None


def check_tie():
    for j in areas:
        if j.oc is None:
            return False

    return True


def match(indexes: list | tuple):
    if areas[indexes[0]].oc == areas[indexes[1]].oc == areas[indexes[2]].oc \
            and areas[indexes[0]].oc is not None:
        return True, areas[indexes[0]].oc, areas[indexes[0]], areas[indexes[2]], areas[indexes[0]].colour

    else:
        return False, None, None, None, None


def find_missing(child: list | tuple):
    c = list(child)
    print(f"Plays blocked: {plays_blocked}")
    c.sort()

    print("Player move: " + str(c))
    if c == [0, 1] and c not in plays_blocked:
        plays_blocked.append(c)
        return 2

    elif c == [1, 2] and c not in plays_blocked:
        plays_blocked.append(c)
        return 0

    elif c == [0, 2] and c not in plays_blocked:
        plays_blocked.append(c)
        return 1

    elif c == [3, 5] and c not in plays_blocked:
        plays_blocked.append(c)
        return 4

    elif c == [4, 5] and c not in plays_blocked:
        plays_blocked.append(c)
        return 3

    elif c == [3, 4] and c not in plays_blocked:
        plays_blocked.append(c)
        return 5

    elif c == [6, 7] and c not in plays_blocked:
        plays_blocked.append(c)
        return 8

    elif c == [7, 8] and c not in plays_blocked:
        plays_blocked.append(c)
        return 6

    elif c == [6, 8] and c not in plays_blocked:
        plays_blocked.append(c)
        return 7

    elif c == [0, 3] and c not in plays_blocked:
        plays_blocked.append(c)
        return 6

    elif c == [3, 6] and c not in plays_blocked:
        plays_blocked.append(c)
        return 0

    elif c == [0, 6] and c not in plays_blocked:
        plays_blocked.append(c)
        return 3

    elif c == [1, 7] and c not in plays_blocked:
        plays_blocked.append(c)
        return 4

    elif c == [1, 4] and c not in plays_blocked:
        plays_blocked.append(c)
        return 7

    elif c == [4, 7] and c not in plays_blocked:
        plays_blocked.append(c)
        return 1

    elif c == [2, 5] and c not in plays_blocked:
        plays_blocked.append(c)
        return 8

    elif c == [5, 8] and c not in plays_blocked:
        plays_blocked.append(c)
        return 2

    elif c == [2, 8] and c not in plays_blocked:
        plays_blocked.append(c)
        return 5

    elif c == [0, 8] and c not in plays_blocked:
        plays_blocked.append(c)
        return 4

    elif c == [4, 8] and c not in plays_blocked:
        plays_blocked.append(c)
        return 0

    elif c == [0, 4] and c not in plays_blocked:
        plays_blocked.append(c)
        return 8

    elif c == [2, 4] and c not in plays_blocked:
        plays_blocked.append(c)
        return 6

    elif c == [4, 6] and c not in plays_blocked:
        plays_blocked.append(c)
        return 2

    elif c == [2, 6] and c not in plays_blocked:
        plays_blocked.append(c)
        return 4

    return False


def find_all_pairs(lis: list):
    pairs = []
    for i in range(len(lis)):
        for j in lis[i:]:
            if lis[i] != j:
                pairs.append((lis[i], j))

    return pairs


def defense_check(inds: list | tuple):
    for ind in find_all_pairs(inds):
        missed = find_missing([areas[ind[0]].refer, areas[ind[1]].refer])
        print(f"Missed: {missed}\n")
        print(f"Checking conds: {[areas[ind[0]].refer, areas[ind[1]].refer] not in plays_blocked and missed is not False}")

        if areas[ind[0]].oc == areas[ind[1]].oc == "Circle" and \
                [areas[ind[0]].refer, areas[ind[1]].refer] in plays_blocked and missed is not False:
            return True, missed

    return False, None


setup()
circle = None
win = False
tie = False
print_ = False

print("\nPlayer start: Press 1\nComputer start: Press 2\n")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and check_collide_areas() is not None and circle \
                and not areas[check_collide_areas()].filled and not win and not tie:
            draw_move(areas[check_collide_areas()].centre, circle)

            circle = False
            areas[check_collide_areas()].filled = True
            areas[check_collide_areas()].oc = "Circle"
            areas[check_collide_areas()].colour = "#ffffeb"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                exit()

            if event.key == pygame.K_1:
                circle = True

            elif event.key == pygame.K_2:
                circle = False

    if check_win()[0] and not win and not tie:
        win, print_ = True, True

    elif check_tie() and not tie:
        tie, print_ = True, True

    if circle is False and not win and not tie:
        draw_move(auto_pick(), circle)
        circle = True

    if check_win()[0] and not win and not tie:
        win, print_ = True, True

    elif check_tie() and not tie:
        tie, print_ = True, True

    pygame.display.update()

    if print_:
        if check_win()[1] == "Circle":
            print("\nPlayer has won!")

        elif check_win()[1] == "Cross":
            print("\nComputer has won!")

        elif check_tie():
            print("\nIt's a tie!")
        print_ = False
