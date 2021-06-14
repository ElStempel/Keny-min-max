# Keny-min-max

## Keny to wariant tureckich warcab. Przyjąto założenia realizacyjne upraszczające zasady gry.

Zasady:
- ken porusza się o jedno pole do przodu lub na boki,
- ken może przeskoczyć nad sojusznikiem bez zbijania go,
- ken może zbić wroga w dowolnym kierunku poprzez przeskoczenie nad nim,
- ken może łączyć bicia w trakcie jednej tury,
- ken zostaje pepperem po dotarciu do przeciwnego krańca planszy,
- pepper może poruszać się o jedno pole w każdym kierunku.

Zaimplementowano:
- grę keny,
- sztuczną inteligencję z wykorzystaniem algorytmu min-max,
- możliwość podejrzenia procesu myślowego sztucznej intelgencji (wymaga zmiany w kodzie).

Nie zaimplementowano:
- oryginalnego schematu poruszania się peppera,
- remisu w przypadku 10 tur bez żadnego zbicia,
- cięć alfa-beta.
