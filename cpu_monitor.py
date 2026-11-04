#vcgencmd measure_temp

from datetime import datetime
import time


def get_cpu_temp():
  """Reads the CPU temperature from the Raspberry Pi thermal zone file."""
  try:
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
      temp_str = f.read().strip()
      # Convert millidegrees to degrees Celsius
      return float(temp_str) / 1000.0
  except FileNotFoundError:
    # Fallback for systems where thermal_zone0 isn't available
    return None


print("Starting CPU Temperature Monitor. Press Ctrl+C to exit.\n")

try:
  while True:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp = get_cpu_temp()

    if temp is not None:
      print(f"[{current_time}] | CPU Temperature: {temp:.2f} °C")
    else:
      print(
          f"[{current_time}] | Error: Could not read CPU temperature from thermal"
          " zone."
      )

    # Wait for 10 seconds before the next reading
    time.sleep(10)

except KeyboardInterrupt:
  print("\nMonitoring stopped by user.")
