from dataclasses import dataclass

from model.sighting import Sighting


@dataclass
class Arco:
    si1:Sighting
    si2:Sighting
    peso:int