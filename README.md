# Oryzacola
Oryzacola is a virtual paddy field with of rice hybriding simulations.

## What Is Rice
Rice (scientific name *Oryza sativa*) is a primary grain which is widely cultivated in East Asia. Rice are usually consumed whole-grain, either boiled or steamed. Husked steamed white rice provides 45 grammes of carbohydrate per 100 g, and has a high glycemic index (GI) of *ca.* 84.

## How To Use

### Single Rice Crop
Firstly import this package:
```
from oryzacola import *
```
Create a rice crop using class `Oryza`:
```
a = Oryza()
```
You can assign specific traits to the crop. The genome of rice here includes `SeedShredding`, `FullCaryopsis`, `RhizoctoniaResistance`, `Glutinous`, `Yield`, `GrowthSpeed`, and `PlantHeight`. *Notice:* genes come in pairs.
```
a = Oryza(SeedShredding = (True, False), FullCaryopsis = True)
```
… will give a crop whose "seed shredding" trait is heterozygous & dominant, while "full caryopsis" trait is homozygous & dominant.

Any "new" rice crop has its *growth stage* (`Oryza.growth_stage`) of 0, which means the crop is still a sprout. Currently any `Oryza` instance will not grow as time elapses. You can use `Oryza.maturize()` to ripen it, allowing the crop to produce pollens and seeds.

After a rice crop having become mature, you can hybrid two crops using `*`:
```
a = Oryza(...)
b = Oryza(...)
a.maturize()
b.maturize()
c = a * b
```

The new crop's genes follow Mendel's rules. Another way (also a more natural way) is to have the crop receiving pollens from other crops (or from itself, as *Oryza sativa* is self-compatible), then randomly produce seeds by all the pollens it has received:
```
a = Oryza(...)
b = Oryza(...)
a.maturize()
b.maturize()
a.pollinated_by(b) # a pollen of B goes into A's "pollen depository"
a.self_pollinate() # a pollen of A itself goes into A's "pollen depository"
a.seed() # "seed" is also an instance of class Oryza
```

Simply print the crop to see its traits:
```
>>> a
>>>
物种:
    Oryza sativa
纯母系/父系世代数：
    1 / 1
自然落粒性:
    显性 (纯合)
颖果饱满性:
    隐性
纹枯病抗性:
    隐性
糯性:
    隐性
产量:
    1级 / 1级
生长速度:
    5级 / 5级
株高:
    3级 / 3级
```
You can also use `Oryza.inspect_plant()` to see the "true crop" — an ASCII art, which will adjust to certain genes. Just for fun.
```
>>> a.inspect_plant()
>>>
      ·      
    <-<-<-<-- 
   /        
  /
  |
\\|//
\\|//
```

### Paddy Field
***IN PROGRESS***

Class `PaddyRow` instances provide a *row* of rice crops to simulate natural pollination among multiple rice crops.
```
p1 = PaddyRow() # will have 4 crops by default
p2 = PaddyRow(size=6)
p3 = PaddyRow(wilderness=True) # randomize some traits of each crop
```

`PaddyRow.sightsee()` and `PaddyRow.maturize()` act similary as `Oryza.inspect_plant()` and `Oryza.maturize()`.

`PaddyRow.free_pollinate()` let all crops in the row which are mature spead their pollens by wind at once.
