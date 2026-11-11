from datetime import datetime
import os
import time


def get_cpu_temp():
  """Reads the CPU temperature from Intel coretemp hwmon or falls back to thermal zones."""
  # 1. Search hwmon for Intel coretemp driver (standard on x86 Intel CPUs)
  hwmon_base = "/sys/class/hwmon"
  if os.path.exists(hwmon_base):
    for hwmon_dir in os.listdir(hwmon_base):
      hwmon_path = os.path.join(hwmon_base, hwmon_dir)
      name_file = os.path.join(hwmon_path, "name")
      if os.path.exists(name_file):
        try:
          with open(name_file, "r") as nf:
            if "coretemp" in nf.read():
              # Usually temp1_input is the package temperature
              temp_file = os.path.join(hwmon_path, "temp1_input")
              if os.path.exists(temp_file):
                with open(temp_file, "r") as tf:
                  return float(tf.read().strip()) / 1000.0
        except Exception:
          continue

  # 2. Fallback to thermal_zone0 if coretemp isn't found
  try:
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
      return float(f.read().strip()) / 1000.0
  except FileNotFoundError:
    return None


print("Starting x86 Intel CPU Temperature Monitor. Press Ctrl+C to exit.\n")
f = open("cpu_log", "a", encoding="utf-8")

try:
  while True:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp = get_cpu_temp()

    if temp is not None:
      print(f"[{current_time}] | CPU Temperature: {temp:.2f} °C")
      f.write(f"[{current_time}] | CPU Temperature: {temp:.2f} °C\n")
    else:
      print(
          f"[{current_time}] | Error: Could not read CPU temperature from hwmon"
          " or thermal zone."
      )
      f.write(
          f"[{current_time}] | Error: Could not read CPU temperature from hwmon"
          " or thermal zone.\n"
      )

    time.sleep(10)

except KeyboardInterrupt:
  print("\nMonitoring stopped by user.")

finally:
  f.close()
