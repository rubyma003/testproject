def calculate_carbon_emissions(distance_km, travel_class="economy"):
    """
    Calculates estimated CO2 emissions in kilograms for a flight.
    """
    # Emission factors (kg of CO2 per passenger per kilometer)
    emission_rates = {
        "economy": 0.15,
        "business": 0.35,
        "first": 0.60
    }
    
    # Get the correct rate, default to economy if class isn't recognized
    rate = emission_rates.get(travel_class.lower(), 0.15)
    
    # Total emissions in kg
    total_emissions_kg = distance_km * rate
    
    # Convert to metric tons
    total_emissions_tons = total_emissions_kg / 1000
    
    return total_emissions_kg, total_emissions_tons

# Example usage: Let's say a flight from Toronto to Vancouver is about 3,350 km
distance = 3350
choice = "economy"

kg, tons = calculate_carbon_emissions(distance, choice)

print(f"Flight Distance: {distance} km")
print(f"Travel Class: {choice.capitalize()}")
print(f"Estimated CO2 Emissions: {kg:.2f} kg ({tons:.2f} metric tons)")