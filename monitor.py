from datetime import datetime;
import time;
from sense_hat import SenseHat;

# Initialize the Sense HAT
sense = SenseHat();

# Define your calibration offset determined from testing
HUMIDITY_OFFSET = -45.7  # Example: subtract 25.0% if it reads too high

# Optional: Clear any existing messages or LEDs
sense.clear()

print("Starting Sense HAT Monitor. Press Ctrl+C to exit.\n")

try:
  while True:
    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Read temperature and humidity
    # Temperature from the humidity sensor is generally more accurate for
    # ambient room temp
    temperature = sense.get_temperature_from_humidity();
    humidity = sense.get_humidity()+HUMIDITY_OFFSET;

    # Print formatted output to the command line
    print(
        f"[{current_time}] | Temperature: {temperature:.2f} °C | Humidity:"
        f" {humidity:.2f} %|"
    );

    # Wait for 10 seconds before the next reading
    time.sleep(10);

except KeyboardInterrupt:
  print("\nMonitoring stopped by user.");
  sense.clear();
