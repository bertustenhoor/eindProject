from flask_meld import Component
from forms import BeToevoegenBoeking


class Boek(Component):
    form = BeToevoegenBoeking()
    