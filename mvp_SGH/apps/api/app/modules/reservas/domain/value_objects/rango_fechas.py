"""
Value Object: Rango de Fechas
"""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RangoFechas:
    inicio: date
    fin: date

    def __post_init__(self):
        if self.fin <= self.inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")

    def solapa_con(self, otro: "RangoFechas") -> bool:
        """True si los rangos se solapan (útil para verificar disponibilidad)."""
        return self.inicio < otro.fin and otro.inicio < self.fin

    def noches(self) -> int:
        return (self.fin - self.inicio).days
