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

Hybriding two crops using `*`:
```
a = Oryza(...)
b = Oryza(...)
c = a * b
```
The new crop's genes follow Mendel's rules.

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
