import pychromecast
from pychromecast.discovery import discover_chromecasts, stop_discovery
from pychromecast.controllers.youtube import YouTubeController
import time

# --- INPUT & DISCOVERY ---
ip_target = input("\nEnter Target IP (Ensure Ports 8009 & 8008 are Open via Nmap): ")

with open('ip.txt', 'w') as file:
    file.write(ip_target + "\n")

print("IP saved to ip.txt")
print(f"Searching for device at {ip_target}...")

services, browser = discover_chromecasts()
time.sleep(2)

cast_info = next((s for s in services if s.host == ip_target), None)

if cast_info:
    print(f"Device Found: {cast_info.friendly_name}")
    
    cast = pychromecast.Chromecast(cast_info, zconf=browser.zc)
    cast.wait()
    
    # --- DEVICE INFO ---
    print(f"MODEL        : {cast.cast_info.model_name}")
    print(f"MANUFACTURER : {cast.cast_info.manufacturer}")
    print(f"UUID         : {cast.cast_info.uuid}")
    print(f"CURRENT VOL  : {int(cast.status.volume_level * 100)}%")
    time.sleep(1)

    print("\n++++ OPTIONS ++++")
    print("1. VOLUME CONTROL")
    print("2. FORCE YOUTUBE")
    print("3. KILL APP")
    print("4. QUIT")
    
    option = input("\nSelect Option: ")

    # --- OPTION 1: VOLUME ---
    if option == "1":
        print("\n++++ VOLUME OPTIONS ++++")
        print("1. SET SPECIFIC VOLUME")
        print("2. AUTOMATIC LOOP (STROBE)")
        vol_option = input("\nSelect option: ")
        
        if vol_option == "1":
            volume = float(input("Enter volume level (0.0 - 1.0): "))
            cast.set_volume(volume)
            print("Volume set.")
            
        elif vol_option == "2":
            wait_time = float(input("Delay before start (seconds): "))
            duration = float(input("Loop duration (seconds): "))
            
            print(f"Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            
            start_time = time.time()
            print("Volume loop started...")
            while time.time() - start_time < duration:
                cast.set_volume(0.1)
                time.sleep(0.5)
                if time.time() - start_time >= duration: break
                cast.set_volume(0.8)
                time.sleep(0.5)
            print("Loop finished.")

    # --- OPTION 2: YOUTUBE ---
    elif option == "2":
        YOUTUBE_APP_ID = '233637DE'
        
        # 1. Clean Input
        video_id_raw = input("\nEnter YouTube ID or URL (e.g., dQw4w9WgXcQ): ")
        if "v=" in video_id_raw:
            video_id = video_id_raw.split("v=")[-1].split("&")[0]
        elif "youtu.be" in video_id_raw:
            video_id = video_id_raw.split("/")[-1]
        else:
            video_id = video_id_raw
            
        print(f"[*] Target ID: {video_id}")

        # 2. Init Controller
        yt = YouTubeController()
        cast.register_handler(yt)
        
        # 3. Clean Start
        print("[*] Terminating old YouTube session...")
        cast.quit_app() 
        time.sleep(3) 

        # 4. Open New App
        print("[*] Launching YouTube...")
        cast.start_app(YOUTUBE_APP_ID)
        
        # 5. Wait for Active Session
        print("[*] Waiting for application to load...")
        timeout = 0
        while True:
            time.sleep(1)
            timeout += 1
            if cast.app_id == YOUTUBE_APP_ID:
                print("[+] Application detected active!")
                break
            if timeout > 20:
                print("(!) Timeout waiting for application.")
                break
        
        # Mandatory Buffer for Android TV Loading Screen
        print("[*] Buffering 5s for loading animation...")
        time.sleep(5)

        # 6. Double Tap Strategy
        print("[*] Playback attempt 1...")
        yt.play_video(video_id)
        
        time.sleep(2)
        
        print("[*] Playback attempt 2 (Forcing)...")
        yt.play_video(video_id)
        
        print("[+] Done.")

    # --- OPTION 3: KILL APP ---
    elif option == "3":
        cast.quit_app()
        print("\nApp terminated successfully...")

    # --- OPTION 4: QUIT ---
    elif option == "4":
        print("\nExiting program...")

    else:
        print("Option not available.")

else:
    print(f"Failed to find cast info for IP {ip_target}")

stop_discovery(browser)
