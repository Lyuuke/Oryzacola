import random

oryzaInfoFormat = '''
物种:
    Oryza sativa
纯母系/父系世代数：
    {1[0]} / {1[1]}
自然落粒性:
    {0[0]}
颖果饱满性:
    {0[1]}
纹枯病抗性:
    {0[2]}
糯性:
    {0[3]}
产量:
    {0[4]}
生长速度:
    {0[5]}
株高:
    {0[6]}
'''

plantInspection = '''
      {0[0]} {0[5]} {0[2]} {0[7]}
    <-<-<-<--{0[4]}
   / {0[6]} {0[1]} {0[8]} {0[3]}
  /
  |
\\\\|//
'''

plantInspectionStem = '\\\\|//\n'

class SelfingError(Exception):
    pass

class SeedOnlyError(Exception):
    pass

class Pollen:
    def __init__(se, di = {}, ge = 1, **tr):
        se.generations = ge
        se.pollen_id = random.random()
        se.traits = {
            'SeedShredding': True,
            'FullCaryopsis': False,
            'RhizoctoniaResistance': False,
            'Glutinous': False,
            'Yield': 1,
            'GrowthSpeed': 5,
            'PlantHeight': 3
        }
        for i in tr:
            if i in se.traits:
                se.traits[i] = tr[i]
        if di:
            for j in di:
                if j in se.traits:
                    se.traits[j] = di[j]
    def __mul__(se, al):
        newPlant = {}
        for i in se.traits:
            newPlant[i] = (se.traits[i], al.traits[i])
        return(Oryza(newPlant, ge = (se.generations + 1, al.generations + 1)))

class Oryza:
    def __init__(se, di = {}, ge = (1, 1), **tr):
        se.growth_stage = 0
        # 生长阶段
        #   |-    YOUNG    -|   |- MATURE  -| SEEDING
        #   1   2   3   4   5   6   7   8   9   10
        se.self_pollination_weight = 5
        # 自授粉权重 - 数值化的自交亲和性
        se.pollen_adhesion = 1
        # 影响风媒传粉距离
        se.generations = ge
        se.traits = {
            'SeedShredding': (True, True),
            'FullCaryopsis': (False, False),
            'RhizoctoniaResistance': (False, False),
            'Glutinous': (False, False),
            'Yield': (1, 1),
            'GrowthSpeed': (5, 5),
            'PlantHeight': (3, 3)
        }
        for i in tr:
            if i in se.traits:
                if isinstance(tr[i], tuple):
                    se.traits[i] = tr[i]
                else:
                    se.traits[i] = (tr[i], tr[i])
        if di:
            for j in di:
                if j in se.traits:
                    se.traits[j] = di[j]
        se.pollens = []
        se.pollen_weights = []
    def __mul__(se, al):
        return se.gamete(ovum = True) * al.gamete()
    def __repr__(se):
        infos = []
        for i in se.traits:
            if isinstance(se.traits[i][0], bool):
                if se.traits[i][0] or se.traits[i][1]:
                    if se.traits[i][0] and se.traits[i][1]:
                        infos.append('显性 (纯合)')
                    else:
                        infos.append('显性 (杂合)')
                else:
                    infos.append('隐性')
            elif isinstance(se.traits[i][0], int):
                infos.append('{0}级 / {1}级'.format(max(se.traits[i]), min(se.traits[i])))
        return oryzaInfoFormat.format(infos, se.generations)
    def grow(se):
        se.growth_stage += 1
    def maturize(se):
        se.growth_stage = 6
    def inspect_pollens(se):
        if se.pollens == []:
            print('目前没有花粉')
        else:
            tempNum = 1
            for i in se.pollens:
                print('花粉 #{}'.format(tempNum))
                print('世代数 {}'.format(i.generations))
                for j in i.traits:
                    print('{0}: {1}'.format(j, i.traits[j]))
                tempNum += 1
    def inspect_plant(se):
        earFill = [] # len(earFill) := 9
        stemSecs = max(se.traits['PlantHeight']) // 2
        yieldSecs = min(max(se.traits['Yield']) // 2 + 1, 9)
        if se.traits['FullCaryopsis'][0] or se.traits['FullCaryopsis'][1]:
            fillIcon = 'o'
        else:
            fillIcon = '·'
        for i in range(yieldSecs):
            earFill.append(fillIcon)
        for j in range(9 - yieldSecs):
            earFill.append(' ')
        plantImage = plantInspection.format(earFill)
        plantImage += (plantInspectionStem * stemSecs)
        print(plantImage)
    def gamete(se, ovum = False):
        newGemete = {}
        for i in se.traits:
            if isinstance(se.traits[i][0], bool):
                newGemete[i] = random.choice(se.traits[i])
            else:
                newGemete[i] = random.randint(min(se.traits[i]), max(se.traits[i]))
        if ovum:
            return Pollen(newGemete, ge = se.generations[0])
        else:
            return Pollen(newGemete, ge = se.generations[1])
    def self_pollinate(se, wg = None):
        if wg == None:
            wgt = se.self_pollination_weight
        if wgt != 0:
            se.pollens.append(se.gamete())
            se.pollen_weights.append(wgt)
        else:
            tempErr = SelfingError('该植株自交不亲和')
            raise tempErr
    def pollinated_by(se, al, wg = 2):
        if isinstance(al, Pollen):
            se.pollens.append(al)
            se.pollen_weights.append(wg)
        elif isinstance(al, Oryza):
            se.pollens.append(al.gamete())
            se.pollen_weights.append(wg)
    def seed(se):
        if se.pollens == []:
            return None
        else:
            return se.gamete() * random.choice(se.pollens)

class PaddyField:
    def __init__(se, size = 6):
        se.field = []
        for i in range(size):
            templist = []
            for j in range(size):
                templist.append(Oryza())
            se.field.append(templist)

class PollenBarrier:
    def __init__(se):
        se.pollens = []
    def pollinated_by(se, al, wg = 2):
        if isinstance(al, Pollen):
            se.pollens.append(al)
            se.pollen_weights.append(wg)
        elif isinstance(al, Oryza):
            se.pollens.append(al.gamete())
            se.pollen_weights.append(wg)

class SeedBag:
    def __init__(se):
        se.bag = []
    def __getitem__(se, lo):
        return se.bag[lo]
    def __repr__(se):
        glance = ''
        for i in se.bag:
            if True in i.traits['FullCaryopsis']:
                if True in i.traits['Glutinous']:
                    glance += 'O '
                else:
                    glance += '0 '
            else:
                if True in i.traits['Glutinous']:
                    glance += 'o '
                else:
                    glance += '. '
        return glance
    def collect(se, sd):
        if isinstance(sd, Oryza):
            se.bag.append(sd)
        else:
            tempErr = SeedOnlyError('种子袋只能装种子')
            raise tempErr

class PaddyRow:
    def __init__(se, size = 4, wilderness = False):
        se.field = {}
        se.wind = 3 # 决定风媒传粉的最大距离
        if not wilderness:
            for i in range(size):
                se.field[i] = Oryza()
        else:
            for i in range(size):
                se.field[i] = Oryza(
                    SeedShredding = random.choice([True, False]),
                    FullCaryopsis = random.choice([True, False]),
                    RhizoctoniaResistance = random.choice([True, False]),
                    Glutinous = random.choice([True, False]),
                    Yield = random.randint(3, 15),
                    GrowthSpeed = random.randint(2, 10),
                    PlantHeight = random.randint(2, 8)
                    )
    def __getitem__(se, lo):
        return se.field[lo]
    def sightsee(se):
        for i in se.field:
            se.field[i].inspect_plant()
    def set_barrier(se, lo):
        se.field[i] = PollenBarrier()
    def maturize(se):
        for i in se.field:
            se.field[i].growth_stage = 6
    def free_pollinate(se):
        for i in se.field:
            if se.field[i].growth_stage >= 6:
                neighbors = {}
                validWind = se.wind - se.field[i].pollen_adhesion
                for totDist in range(1, validWind + 1):
                    if i + totDist in se.field.keys():
                        neighbors[i + totDist] = int(10 / totDist)
                    if i - totDist in se.field.keys():
                        neighbors[i - totDist] = int(10 / totDist)
                for j in neighbors:
                    if se.field[j].growth_stage >= 6:
                        se.field[j].pollinated_by(se.field[i], wg = neighbors[j])
    def range_polinate(se, sl):
        ...
    def tick(se):
        ...
    def ellapse(se, tp):
        ...



if __name__ == '__main__':
    p = PaddyRow(wilderness = True, size = 8)
    b = SeedBag()
    p.maturize()
    p.free_pollinate()
    for i in p.field:
        b.collect(p.field[i].seed())
    print(b)