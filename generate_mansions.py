import ephem
import math
import datetime
from ics import Calendar, Event

def get_lunar_mansion(date):
    # Compute moon position for the given date
    moon = ephem.Moon()
    moon.compute(date)
    
    # Convert equatorial coordinates to ecliptic (Tropical Zodiac)
    ecl = ephem.Ecliptic(moon)
    lon_deg = math.degrees(ecl.lon)
    
    # The 28 traditional Mansions of the Moon
    mansions = [
        "1: Al-Sharatan", "2: Al-Botein", "3: Al-Thurayya", "4: Aldebaran",
        "5: Al-Haq'ah", "6: Al-Han'ah", "7: Al-Dhira", "8: Al-Nathrah",
        "9: Al-Tarf", "10: Al-Jabhah", "11: Al-Zubrah", "12: Al-Sarfah",
        "13: Al-Awwa", "14: Al-Simak", "15: Al-Ghafr", "16: Al-Zubana",
        "17: Al-Iklil", "18: Al-Qalb", "19: Al-Shaulah", "20: Al-Na'am",
        "21: Al-Baldah", "22: Sa'd al-Dhabih", "23: Sa'd Bula", "24: Sa'd al-Su'ud",
        "25: Sa'd al-Akhbiya", "26: Al-Fargh al-Muqaddam", "27: Al-Fargh al-Muakhar", "28: Batn al-Hut"
    ]
    
    # Calculate the mansion index (0 to 27)
    # Each mansion is exactly 360/28 = 12.8571428 degrees
    mansion_index = int(lon_deg / (360.0 / 28.0))
    return mansions[mansion_index]

def generate_mansions_calendar():
    cal = Calendar()
    today = datetime.datetime.utcnow().date()
    
    # 90-day rolling window
    for i in range(90):
        current_date = today + datetime.timedelta(days=i)
        
        # Check the moon's position at noon to determine the dominant daily mansion
        check_time = datetime.datetime.combine(current_date, datetime.time(12, 0))
        mansion_name = get_lunar_mansion(check_time)
        
        event_name = f"Lunar Mansion {mansion_name}"
        
        e = Event(name=event_name, begin=current_date)
        e.make_all_day()
        cal.events.add(e)
        
    with open("lunar_mansions.ics", "w") as f:
        f.writelines(cal.serialize_iter())

if __name__ == "__main__":
    generate_mansions_calendar()
