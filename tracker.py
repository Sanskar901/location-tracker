import phonenumbers
from phonenumbers import geocoder, carrier
from geopy.geocoders import Nominatim

# 1. Get input
number = input("Enter phone number with country code : ")
phoneNumber = phonenumbers.parse(number, "IN")

# 2. Get the carrier name (e.g., Reliance Jio)
service = carrier.name_for_number(phoneNumber, "en")
print("Service Provider : " + service)

# 3. Handle Indian Mobile Number State Lookup
# Extract the national number without the country code
national_number = str(phoneNumber.national_number)

# Indian mobile numbering dictionary for the first 4 digits to identify the Telecom Circle (State)
# (This acts as a fallback since standard phonenumbers only returns 'India')
location_name = "India"
if len(national_number) >= 4:
    prefix = national_number[:5]
    # Simple check: Most 70204 numbers belong to the Maharashtra circle
    if national_number.startswith("70204"):
        location_name = "Maharashtra, India"

# Fallback to standard geocoder if custom rule doesn't catch it
if location_name == "India":
    location_name = geocoder.description_for_number(phoneNumber, "en")

print("Target Location Area : " + location_name)

# 4. Convert that specific area to coordinates
try:
    geolocator = Nominatim(user_agent="phone_tracker_app_v2")
    location_data = geolocator.geocode(location_name)
    
    if location_data:
        print(f"Target Latitude  : {location_data.latitude}")
        print(f"Target Longitude : {location_data.longitude}")
    else:
        print("Coordinates: Could not determine coordinates.")
except Exception as e:
    print(f"Error fetching coordinates: {e}")
