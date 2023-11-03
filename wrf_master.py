# -*- coding: utf-8 -*-
"""WRF_run.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ARnlUy1xKoITn38UsvEn6z-6MPX6V-Np
"""

import subprocess as sub
import os
import configparser
import wget
import shutil
import time

 # To be kept in the same folder as WPS and WRF
 # Set Environment Variables
os.environ["NETCDF"] = "/opt/apps/netcdf-fortran-4.6.0-openmpi-4.1.5"
os.environ["NETCDF_classic"] = "1"
current_directory = os.getcwd()
current_dir = current_directory
parent_directory = os.path.abspath(os.path.join(current_dir, os.pardir))
parent_dir = parent_directory



##### List of all the functions used
# 1. 
def edit_namelist_wps(file_path, param_name, new_value):
    # Read the contents of the file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Modify the desired parameter in the file
    for i, line in enumerate(lines):
        if param_name in line:
            # Assuming the parameter and value are separated by an equals sign '='
            # Modify the value of the parameter
            lines[i] = f"{param_name} = {new_value}\n"
            break  # Assuming there is only one occurrence of the parameter

    # Write the modified contents back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)

# 2. 
def run_bash_executable_on_terminal(executable_path):
    try:
        # Check if the executable has executable permissions
        if not os.access(executable_path, os.X_OK):
            os.chmod(executable_path, 0o755)  # Add executable permissions if needed

        sub.run([executable_path], check=True)
        print(f"Successfully executed {executable_path} on the terminal.")
    except sub.CalledProcessError as e:
        print(f"Error executing {executable_path} on the terminal: {e}")

# 3. 
def cut_files_with_similar_names(source_folder, destination_folder, filename_pattern):
    try:
        # Get a list of all files in the source_folder
        file_list = os.listdir(source_folder)

        # Filter files based on the filename_pattern
        matching_files = [file for file in file_list if filename_pattern in file]

        # Move matching files to the destination_folder
        for file in matching_files:
            source_file_path = os.path.join(source_folder, file)
            destination_file_path = os.path.join(destination_folder, file)
            shutil.move(source_file_path, destination_file_path)
            print(f"File '{source_file_path}' moved to '{destination_file_path}'.")

    except FileNotFoundError:
        print("Source folder not found.")
    except shutil.Error as e:
        print(f"Error moving files: {e}")

# 4. 
def extract_sections(input_string, delimiter):
    sections = input_string.split(delimiter)
    return sections

# 5.
def downloadable_time(time):
    hour_in = int(time)
    if hour_in % 3 == 1:
      hour_in = hour_in + 2
    if hour_in % 3 == 2:
      hour_in = hour_in + 1
    else:
      hour_in = hour_in
    return(hour_in)

# 6.
def copy_files_with_prefix(source_folder, destination_folder, prefix):
    try:
        # Get a list of all files in the source_folder
        file_list = os.listdir(source_folder)

        # Filter files based on the prefix
        matching_files = [file for file in file_list if file.startswith(prefix)]

        # Copy matching files to the destination_folder
        for file in matching_files:
            source_file_path = os.path.join(source_folder, file)
            destination_file_path = os.path.join(destination_folder, file)
            shutil.copy2(source_file_path, destination_file_path)
            print(f"File '{source_file_path}' copied to '{destination_file_path}'.")

    except FileNotFoundError:
        print("Source folder not found.")
    except shutil.Error as e:
        print(f"Error copying files: {e}")



##### Input the different values
dom_n = input("Enter number of domains")
lat_cen = input("Latitude of centre")
lon_cen = input("Longitude of centre")
start_date = input("Enter start date in format YYYY-MM-DD_HH:mm:SS, Y2Y2-M2-D2_H2:m2:s2, Y3Y3-M3-D3_H3:m3:s3")
end_date = input("Enter end date in format YYYY-MM-DD_HH:MM:SS, Y2Y2-M2-D2_H2:m2:s2, Y3Y3-M3-D3_H3:m3:s3")
parent_id = input("Enter the parent ID for domain 1, domain 2, domain 3")
parent_grid_ratio = input("Enter the parent_grid_ratio for domain 1, domain 2, domain 3")
x_end = input("Enter number of cells along x for domain 1, domain 2, domain 3")
y_end = input("Enter number of cells along y domain 1, domain 2, domain 3")
dx = input("grid resolution along x in metres domain 1, domain 2, domain 3")
dy = input("grid resolution along y in metres domain 1, domain 2, domain 3")
i_parent_start = input("i_parent_start in domain 1, domain 2, domain 3")
j_parent_start = input("j_parent_start in domain 1, domain 2, domain 3")




##### Edit namelist wps parameters
namelist_path = os.path.join(current_directory, "namelist.wps")
edit_namelist_wps(namelist_path, "max_dom", dom_n)
edit_namelist_wps(namelist_path, "start_date", start_date)
edit_namelist_wps(namelist_path, "end_date", end_date)
edit_namelist_wps(namelist_path, "ref_lat", lat_cen)
edit_namelist_wps(namelist_path, "ref_lon", lon_cen)
edit_namelist_wps(namelist_path, "e_we", x_end)
edit_namelist_wps(namelist_path, "e_sn", y_end)
edit_namelist_wps(namelist_path, "dx", dx)
edit_namelist_wps(namelist_path, "dy", dy) 
edit_namelist_wps(namelist_path, "i_parent_start", i_parent_start)
edit_namelist_wps(namelist_path, "j_parent_start", j_parent_start)
edit_namelist_wps(namelist_path, "parent_id", parent_id)
edit_namelist_wps(namelist_path, "parent_grid_ratio", parent_grid_ratio)



##### Run geogrid.exe
bash_executable_path = os.path.join(current_directory, "geogrid.exe") 
run_bash_executable_on_terminal(bash_executable_path)




##### Extract dates and times from input
start_date_multi_domain = extract_sections(start_date, ",")

START = extract_sections(start_date_multi_domain[0], "_")
start_day = START[0]
start_time = START[1]
day_details = extract_sections(start_day, "-")
time_details = extract_sections(start_time, ":")
yyyy = day_details[0]
mm = day_details[1]
dd = day_details[2]
yyyymmdd = yyyy + mm + dd
hh = time_details[0]
minute = time_details[1]
sec = time_details[2]

START2 = extract_sections(start_date_multi_domain[1], "_")
start_day2 = START2[0]
start_time2 = START2[1]
day_details2 = extract_sections(start_day2, "-")
time_details2 = extract_sections(start_time2, ":")
yyyy2 = day_details2[0]
mm2 = day_details2[1]
dd2 = day_details2[2]
yyyymmdd2 = yyyy2 + mm2 + dd2
hh2 = time_details[0]
minute2 = time_details[1]
sec2 = time_details[2]

START3 = extract_sections(start_date_multi_domain[2], "_")
start_day3 = START3[0]
start_time3 = START3[1]
day_details3 = extract_sections(start_day3, "-")
time_details3 = extract_sections(start_time3, ":")
yyyy3 = day_details3[0]
mm3 = day_details3[1]
dd3 = day_details3[2]
yyyymmdd3 = yyyy3 + mm3 + dd3
hh3 = time_details[0]
minute3 = time_details[1]
sec3 = time_details[2]

end_date_multi_domain = extract_sections(end_date, ",")
END = extract_sections(end_date_multi_domain[0], "_")
end_day = END[0]
end_time = END[1]
end_day_details = extract_sections(end_day, "-")
end_time_details = extract_sections(end_time, ":")
end_yyyy = end_day_details[0]
end_mm = end_day_details[1]
end_dd = end_day_details[2]
end_yyyymmdd = end_yyyy + end_mm + end_dd
end_hh = end_time_details[0]
end_minute = end_time_details[1]
end_sec = end_time_details[2]

END2 = extract_sections(end_date_multi_domain[1], "_")
end_day2 = END2[0]
end_time2 = END2[1]
end_day_details2 = extract_sections(end_day, "-")
end_time_details2 = extract_sections(end_time, ":")
end_yyyy2 = end_day_details2[0]
end_mm2 = end_day_details2[1]
end_dd2 = end_day_details2[2]
end_yyyymmdd2 = end_yyyy2 + end_mm2 + end_dd2
end_hh_2 = end_time_details2[0]
end_minute_2 = end_time_details2[1]
end_sec_2 = end_time_details2[2]

END3 = extract_sections(end_date_multi_domain[2], "_")
end_day3 = END3[0]
end_time3 = END3[1]
end_day_details3 = extract_sections(end_day, "-")
end_time_details3 = extract_sections(end_time, ":")
end_yyyy3 = end_day_details3[0]
end_mm3 = end_day_details3[1]
end_dd3 = end_day_details3[2]
end_yyyymmdd3 = end_yyyy3 + end_mm3 + end_dd3
end_hh_3 = end_time_details3[0]
end_minute_3 = end_time_details3[1]
end_sec_3 = end_time_details3[2]





##### Download meterological files
down_time_start = downloadable_time(int(start_time[0]))
down_time_end = downloadable_time(int(end_time_details[0]))
T = 0
print(down_time_end)

while T<=down_time_end:
  TT = "%02d" % T
  url1 = "https://data.rda.ucar.edu/ds083.2/grib2/"+yyyy+"/"+yyyy+"."+mm+"/fnl_"+yyyymmdd+"_"+TT+"_00.grib2"
  print(url1)
  wget.download(url1, parent_dir + '/data/')
  T = T + 6

T = T - 6





##### Run ungrib.exe
command = ['csh', os.path.join(current_directory, "link_grib.csh")] + [os.path.join(parent_directory, "data/fnl*.")] 
sub.run(command, check=True)

#Move the GRIB files to WPS
# Example usage:
if __name__ == "__main__":
    source_folder = parent_directory
    destination_folder = current_directory
    filename_pattern = "GRIBFILE"

    cut_files_with_similar_names(source_folder, destination_folder, filename_pattern)


exe_path_2 = os.path.join(current_directory, "ungrib.exe")
sub.run([exe_path_2], check=True)



# Run metgrid.exe and copy metgrid files to run folder
exe_path_3 = os.path.join(current_directory, "metgrid.exe")
sub.run([exe_path_3], check=True)

if __name__ == "__main__":
    source_folder = current_dir
    destination_folder = parent_dir + "/WRF-4.1.1/run/"
    prefix = "met_em"

    copy_files_with_prefix(source_folder, destination_folder, prefix)



 # Edit namelist.input
namelist_wrf=os.path.join(parent_directory, "WRF-4.1.1/run/namelist.input")

yyyy = day_details[0] + "," """ + day_details2[0] + "," + day_details3[0]"""
mm = day_details[1] + ","  """+ day_details2[1] + "," + day_details3[1]"""
dd = day_details[2] + ","  """+ day_details2[2] + "," + day_details3[2]"""
time_details_hour = time_details[0] + ","  """+ time_details2[0] + "," + time_details3[0]"""
time_details_minute = time_details[1] + ","  """+ time_details2[1] + "," + time_details3[1]"""
time_details_second = time_details[2] + ","  """+ time_details2[2] + "," + time_details3[2]"""
end_yyyy = end_day_details[0] + ","  """+ end_day_details2[0] + "," + end_day_details3[0]"""
end_mm = end_day_details[1] + ","  """+ end_day_details2[1] + "," + end_day_details3[1]"""
end_dd = end_day_details[2] + ","  """+ end_day_details2[2] + "," + end_day_details3[2]"""
end_time_details_hour = end_time_details[0] + "," + end_time_details2[0] + "," + end_time_details3[0]
end_time_details_minute = end_time_details[1] + "," + end_time_details2[1] + "," + end_time_details3[1]
end_time_details_second = end_time_details[2] + "," + end_time_details2[2] + "," + end_time_details3[2]

edit_namelist_wps(namelist_wrf, "run_hours", T)

edit_namelist_wps(namelist_wrf, "start_year", yyyy)
edit_namelist_wps(namelist_wrf, "start_month", mm)
edit_namelist_wps(namelist_wrf, "start_day", dd)
edit_namelist_wps(namelist_wrf, "start_hour", time_details_hour)
edit_namelist_wps(namelist_wrf, "start_minute", time_details_minute)
edit_namelist_wps(namelist_wrf, "start_second", time_details_second)

edit_namelist_wps(namelist_wrf, "end_year", end_yyyy)
edit_namelist_wps(namelist_wrf, "end_month", end_mm)
edit_namelist_wps(namelist_wrf, "end_day", end_dd)
edit_namelist_wps(namelist_wrf, "end_hour", T)
edit_namelist_wps(namelist_wrf, "end_minute", end_time_details[1])
edit_namelist_wps(namelist_wrf, "end_second", end_time_details[2])

edit_namelist_wps(namelist_wrf, "interval_seconds", 21600)
edit_namelist_wps(namelist_wrf, "time_step", int(0.005*float(min([dx, dy]))))

edit_namelist_wps(namelist_wrf, "e_we", x_end)
edit_namelist_wps(namelist_wrf, "e_sn", y_end)
edit_namelist_wps(namelist_wrf, "e_vert", 33)
edit_namelist_wps(namelist_wrf, "dx", dx)
edit_namelist_wps(namelist_wrf, "dy", dy)

edit_namelist_wps(namelist_wrf, "p_top_requested", 60000)
edit_namelist_wps(namelist_wrf, "mp_physics", 2)
edit_namelist_wps(namelist_wrf, "ra_lw_physics", 0)
edit_namelist_wps(namelist_wrf, "ra_sw_physics", 0)
edit_namelist_wps(namelist_wrf, "bl_pbl_physics", 0)
edit_namelist_wps(namelist_wrf, "cu_physics", 0)
edit_namelist_wps(namelist_wrf, "cudt", 0)


 # Run real.exe
exe_path_6 = os.path.join(parent_directory, "WRF-4.1.1/run/real.exe")
sub.run([exe_path_6])


time.sleep(20)
 # Run wrf.exe
command = ['sbatch', os.path.join(parent_directory, "WRF-4.1.1/run/parallel.sh")]
sub.run(command, check=True)



