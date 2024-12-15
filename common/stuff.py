from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


class Projectile:
    def __init__(self, pos: Point, vel: Point):
        self.pos = pos
        self.vel = vel

    def __eq__(self, rhs) -> bool:
        return self.pos == rhs.pos and self.vel == rhs.vel

    def collides_with(self, other: "Projectile") -> Point | None:
        # Returns None if collision isn't found, coordinates otherwise
        if self == other:
            return self.pos

        if self.vel == other.vel:
            # parallel and not starting in same location
            return None

        # solve for t in self.pos + t(self.vel) = other.pos + t(other.vel)
        # spos-opos = tovel - tsvel
        # spos - opos = t(ovel - svel)
        # t = (spo-opos)/(ovel-svel)
        # t = (self.)
