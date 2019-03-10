# Protfólio na IV122 (jaro 2019)
## Celkové hodnotenie
Slabé stránky:
* [TODO]

Silné stránky:
* [TODO]

## Týždeň 1 - Rozcvička:
[Zadanie](https://www.fi.muni.cz/~xpelanek/IV122/zadani/zadani-rozcvicka.pdf)
#### A) Hrátky s čísly
`1.` Číslo s najväčším počtom deliteľov som hľadal prejdením všetkých čísel nasledovnou funkciou:
```pythonstub
def divisor_count(n: int) -> int:
    divs = 0
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divs += 1
    divs = 2 * divs - (1 if int(math.sqrt(n)) ** 2 == n else 0)
    return divs
```
Číslo s najvyšším deliteľom (menšie než 10000) je 7560 (64 deliteľov).

`2.` 200 čísel menších ako 1000 sa nedá vyjadriť ako súčet 3 štvorcov.

Kód na nájdenie najmenších častí
 ```pythonstub
squares: Dict[int, int] = {i * i: i for i in range(1, int(math.sqrt(top)) + 1) if i * i < top}
prev: Dict[int, AbstractSet[Tuple[int, ...]]] = {key: {(value,)} for key, value in squares.items()}
for count in range(1, k):
    new = defaultdict(set)
    for leftsum, tuples in prev.items():
        for square, base in squares.items():
            if leftsum + square < top:
                for tup in tuples:
                    new[leftsum + square].add(tuple(sorted((base,) + tup)))
    prev = new
prev
``` 
Počet spôsobov, koľkými je možné vytvoriť tieto čísla:
![Počet spôsobov, koľkými je možné vytvoriť tieto čísla](results/w1_A__sumsqdist_1.png)

`3.` 6171 sa ukončí po 262 krokoch, čo je najviac zo všetkých čísel do 10000.

Ukážka kódu z triedy, ktorá memoruje celé sekvenie. Tento spôsob je pamäťovo neefektívny, ale umožnuje rýchlo 
```pythonstub
def get(self, n: int) -> int:
    if n in self.mem:
        return self.mem[n]
    nxt = (n // 2) if n % 2 == 0 else (n * 3 + 1)
    self.mem[n] = 1 + self.get(nxt)
    return self.mem[n]
```

`4.` 49061 je hľadaná suma.

Funkcia na zistenie, či je dané číslo prvočíslo.
```pythonstub
def isprime(n: int) -> bool:
    for i in range(1, int(math.sqrt(n))):
        i += 1
        if n % i == 0:
            return False
    return True
```

`5.` 1594323 je prvé číslo väčšie než 1000000 v zadanej postupnosti.

Ukážka pamäťovo neefektívneho kódu ktorý hľadá dané číslo.
```pythonstub
seq = [1, 1]
while seq[-1] <= limit:                # limit = 1'000'000
    a, b = seq[-1], seq[-2]
    seq.append(a + b + math.gcd(a, b))
return seq[-1]
```


### B) Práce s grafikou

Rasterový obrázok zo zadania generuje nasleduvný skript:
```pythonstub
image_array = np.dstack((np.fromfunction(lambda x, y: 256 * y / imgdim, shape=imgsize, dtype=np.uint32),  # R
                         np.zeros(shape=imgsize, dtype=np.uint32),                                        # G
                         np.fromfunction(lambda x, y: 256 * x / imgdim, shape=imgsize, dtype=np.uint32))) # B
```

Výsledný obraz vyzerá takto:

![Raster](results/w1_B__raster_1.png)

Hviezdu som generoval z "rohov", ktoré ju tvoria.

```pythonstub
def corner(self, drawing: svgwrite.drawing.Drawing, size: int = 100, steps=10, pos=(0, 0), direction=(1, 1)):
    # transform moves a point according to the `pos` and `direction` parameters 
    transform = lambda x: add_tuple(pos, mult_tuple(direction, x))
    for i in range(steps + 1):
        p = size / steps * i
        drawing.add(svgwrite.shapes.Line(transform((p, 0)), transform((size, p)), stroke='black'))
```
Výsledok:

![Stars](results/w1_B__star_1.svg)

### C) Ulamova spirála


Algoritmus pre efektívne generovanie Ulamovej špirály pomocou iterovania kým napravo od aktuálneho smeru je nejaká hodnota.  
```pythonstub
array = np.zeros((2 * size + 1, 2 * size + 1), dtype=np.uint32)
array[size][size] = 1
pos = (size, size + 1)
direction = Direction.UP
value = 2
for i in range(4 * size):
    while array[add_tuple(direction.turn_right().value, pos)] != 0:
        array[pos] = value
        value += 1
        pos = add_tuple(pos, direction.value)
        if pos[0] == array.shape[0] or pos[1] == array.shape[1]:
            break
    direction = direction.turn_right()
return array
```

Na toto pole o veľkosti `1001x1001` boli následne volané funkcie `int -> bool`, ktoré vytvorili rôzne vzory.

Prvočísla:
![prvocisla](/results/w1_C__prime_1.png)

Deliteľné 5:
![delitele 5](/results/w1_C__div5_1.png)

Deliteľné 8:
![delitele 8](/results/w1_C__div8_1.png)

Fibonačiho postupnosť (táto postupnosť nie je taká zaujímavá, lebo rastie exponenciálne, čiže vyššie hodnoty su príliš "riedke"):
![fibonacci](/results/w1_C__fib_1.png)

### D) Vizualizace NSD

`1.` Vizualizácia `NSD(x,y) / MAX(x,y)` `x,y <= 1500`:

![NSD visualizacia](/results/w1_D__gcd_1.png)

`2.` Vizualizácia počtu krokov Euklidovho algoritmu:
* Odčítavacia verzia:
```pythonstub
def gcd_sub(a: int, b: int) -> int:
    count = 0
    while True:
        if a < b:
            a, b = b, a
        if a == b:
            return count
        a, b = a - b, b
        count += 1
```
![Odcitanie](/results/w1_D__gcdsub_1.png)

* Modulo verzia:
```pythonstub
def gcd_mod(a: int, b: int) -> int:
    count = 0
    while True:
        if a < b:
            a, b = b, a
        if b == 0:
            return count
        a, b = b, a % b
        count += 1
```
![Modulo](/results/w1_D__gcdmod_1.png)
* Obe verzie spolu (Červený kanál je odčítacia a modrý je modulo varianta):

![Odcitanie a modulo](/results/w1_D__gcdboth_1.png)

## Týždeň 2 - Kombinatorika, výpočty:

[zadanie](https://www.fi.muni.cz/~xpelanek/IV122/zadani/zadani-cisla.pdf)

### A) Generování kombinací, permutací, variací

### B) Pascalův trojúhelník

Pascalov trojuholník som vygeneroval pomocou objektu, ktorý memoruje hodnoty a 
garantuje alokovanie pamäte pre každé volanie.
```pythonstub
def _get(self, r: int, c: int):
    if self.data[r][c] is None:
        if c == 0 or r == c:
            self.data[r][c] = 1
        else:
            self.data[r][c] = self._get(r - 1, c - 1) + self._get(r - 1, c)
            if self.mod is not None:
                self.data[r][c] = self.data[r][c] % self.mod
    return self.data[r][c]
```

![pascal 50 5](/results/w2_B__pascal_50_5_1.png)
50 riadkov pascalovho trojuholníku so zafarbením `mod 5`.

![pascal 500 5](/results/w2_B__pascal_500_5_1.png)
500 riadkov pascalovho trojuholníku so zafarbením `mod 5`.

![pascal 500 10](/results/w2_B__pascal_500_10_1.png)
500 riadkov pascalovho trojuholníku so zafarbením `mod 10`.

### C) Výpočet π



### D) Umocňování

Implementoval som 2 algoritmy:

```pythonstub
def pow(base: float, power: int, modulo: int):
    ongoing = 1
    exp = base % modulo
    while power != 0:
        if power % 2 == 1:
            ongoing = (ongoing * exp) % modulo
        power = power // 2
        exp = (exp * exp) % modulo
    return ongoing
```
Efektívny algoritmus na výpočet celočíselných mocnín.

```pythonstub
def pow_naive(base: float, power: int, modulo: int):
    tmp = 1
    for _ in range(power):
        tmp = (tmp * base) % modulo
    return tmp
```
Naivný algoritmus na výpočet celočíselných mocnín.

Tieto algoritmy som následne porovnal na 3 rôznych výpočtoch:

| Vzorec                                           | Čas efektívneho | Čas neefektívneho |  
|--------------------------------------------------|-----------------|-------------------|
| `123^1234567 (mod 1000000007)`                   | 7700 ns         | 140718000 ns      |   
| `9^10 (mod 2)`                                   | 3100 ns         | 3700 ns           |   
| `123456^12345678901234567890 (mod 1000000007)`   | 19000 ns        | N/A               |   

Následne som zmeral rýchlosť efektívnej implementácie v závislosti od rastúceho exponentu (10 vzorkov pre každý bod):

![rychlost algo](results/w2_D__pow_efficiency_1.png)

Ako môžeme vidieť, zložitosť algoritmu naozaj rastie logaritmicky s rastúcim exponentom.








