class Planet:
    def __init__(self, name, exalted_house, debilitated_house, ruling_house, friendly_planets, enemy_planets):
        self.name = name
        self.exalted_house = exalted_house
        self.debilitated_house = debilitated_house
        self.ruling_house = ruling_house
        self.friendly_planets = friendly_planets
        self.enemy_planets = enemy_planets

class House:
    def __init__(self, house_number, ruling_planet, significator_planet):
        self.house_number = house_number
        self.ruling_planet = ruling_planet
        self.significator_planet = significator_planet
        self.planet = None

class BirthChart:
    def __init__(self):
        self.houses = self._initialize_houses()
        self.planets = self._initialize_planets()

    def _initialize_houses(self):
        houses = [
            House(1, "Mars", "Sun"),
            House(2, "Venus", "Jupiter"),
            House(3, "Mercury", "Mars"),
            House(4, "Moon", "Moon"),
            House(5, "Sun", "Jupiter"),
            House(6, "Mercury", "Ketu"),
            House(7, "Venus", "Venus"),
            House(8, "Mars", "Saturn, Mars, Moon"),
            House(9, "Jupiter", "Jupiter"),
            House(10, "Saturn", "Saturn"),
            House(11, "Saturn", "Jupiter"),
            House(12, "Jupiter", "Rahu")
        ]
        return houses

    def _initialize_planets(self):
        planets = [
            Planet("Sun", exalted_house=1, debilitated_house=7, ruling_house=5, friendly_planets=["Moon", "Mars", "Jupiter"], enemy_planets=["Venus", "Saturn", "Rahu"]),
            Planet("Moon", exalted_house=2, debilitated_house=8, ruling_house=4, friendly_planets=["Sun", "Mercury"], enemy_planets=["Rahu", "Ketu"]),
            Planet("Mars", exalted_house=10, debilitated_house=4, ruling_house=1, friendly_planets=["Sun", "Moon", "Jupiter"], enemy_planets=["Mercury", "Ketu"]),
            Planet("Mercury", exalted_house=6, debilitated_house=12, ruling_house=3, friendly_planets=["Sun", "Venus", "Rahu"], enemy_planets=["Moon"]),
            Planet("Jupiter", exalted_house=4, debilitated_house=10, ruling_house=9, friendly_planets=["Sun", "Moon", "Mars"], enemy_planets=["Mercury", "Venus"]),
            Planet("Venus", exalted_house=12, debilitated_house=6, ruling_house=7, friendly_planets=["Mercury", "Saturn", "Ketu"], enemy_planets=["Sun", "Moon", "Rahu"]),
            Planet("Saturn", exalted_house=7, debilitated_house=1, ruling_house=10, friendly_planets=["Mercury", "Venus", "Rahu"], enemy_planets=["Sun", "Moon", "Mars"]),
            Planet("Rahu", exalted_house=3, debilitated_house=9, ruling_house=None, friendly_planets=["Mercury", "Saturn", "Ketu"], enemy_planets=["Sun", "Mars"]),
            Planet("Ketu", exalted_house=9, debilitated_house=3, ruling_house=None, friendly_planets=["Venus", "Rahu"], enemy_planets=["Moon", "Mars"])
        ]
        return planets

    def assign_planets_to_houses(self, planet_positions):
        for planet_name, house_number in planet_positions.items():
            planet = self.get_planet_by_name(planet_name)
            house = self.get_house_by_number(house_number)
            if house and planet:
                house.planet = planet

    def get_planet_by_name(self, planet_name):
        for planet in self.planets:
            if planet.name == planet_name:
                return planet
        return None

    def get_house_by_number(self, house_number):
        for house in self.houses:
            if house.house_number == house_number:
                return house
        return None

    def calculate_planetary_effects(self):
        effects = {}
        for house in self.houses:
            if house.planet:
                effect = self._determine_effect(house.planet, house)
                effects[house.house_number] = effect
        return effects

    def _determine_effect(self, planet, house):
        if house.house_number == planet.exalted_house:
            return f"{planet.name} is exalted in house {house.house_number}, giving strong positive effects."
        elif house.house_number == planet.debilitated_house:
            return f"{planet.name} is debilitated in house {house.house_number}, giving weak or negative effects."
        else:
            return f"{planet.name} is neutral in house {house.house_number}."

    def display_chart(self):
        chart = ""
        for house in self.houses:
            chart += f"House {house.house_number}: Ruling Planet - {house.ruling_planet}, "
            if house.planet:
                chart += f"Planet - {house.planet.name}\n"
            else:
                chart += "Planet - None\n"
        return chart

def generate_birth_chart(user_data):
    birth_chart = BirthChart()

    planetary_positions = {
        "Sun": 1,
        "Moon": 4,
        "Mars": 7,
        "Mercury": 3,
        "Jupiter": 9,
        "Venus": 6,
        "Saturn": 10,
        "Rahu": 11,
        "Ketu": 12
    }

    birth_chart.assign_planets_to_houses(planetary_positions)
    effects = birth_chart.calculate_planetary_effects()
    chart_representation = birth_chart.display_chart()

    return chart_representation, effects
