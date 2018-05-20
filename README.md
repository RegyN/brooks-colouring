# Kolorowanie Brooksa

### Changelog:

#### 0.3
* Nowa klasa PartGraph implementująca funkcjonalność klasy Graph, ale dla grafów o wierzchołkach o dowolnej numeracji (niekoniecznie kolejno od 0 do n-1)
* Poprawki w sprawdzaniu cykli i ich kolorowaniu w klasie Graph.

#### 0.2
* Dodana możliwość zapisu kolorowania do pliku .csv
* Dodane argumenty do wywoływania programu z konsoli

#### 0.1
Pierwsza wersja
* Na razie tylko klasa Graph, udostępniająca funkcje potrzebne do algorytmu
* Trzeba jeszcze wymyślić jak łączyć kolorowania składowych dla grafów niedwuspójnych

### Znane problemy:
* Działa tylko dla grafów dwuspójnych
* Brak weryfikacji danych wejściowych
* Raczej kiepska optymalizacja