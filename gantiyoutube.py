import pychromecast
from pychromecast.discovery import discover_chromecasts, stop_discovery
from pychromecast.controllers.youtube import YouTubeController
import time



ip_target = input("\nMasukan ip Target Diharapkan Memastikan Port 8009 dan 8008 Terbuka(Lihat di Nmap): ")
with open('ip.txt','w') as file:
    file.write(ip_target + "\n" )

print("ip Sudah di simpan di ip.txt file")
print(f"Sedang mencari perangkat di {ip_target}...")
services, browser = discover_chromecasts()
time.sleep(2)

cast_info = next((s for s in services if s.host == ip_target), None)

if cast_info:
    print(f"Perangkat ditemukan: {cast_info.friendly_name}")
    
    cast = pychromecast.Chromecast(cast_info, zconf=browser.zc)
    cast.wait()
    print(f"MODEL : {cast.cast_info.model_name}")
    print(f"PABRIKAN : {cast.cast_info.manufacturer}")
    print(f"UUID : {cast.cast_info.uuid}")
    print(f"Volume INFO : {int(cast.status.volume_level * 100)}%")
    time.sleep(1)

    print("\n++++OPSI++++")
    print("1.VOLUME")
    print("2.GANTI YOUTUBE")
    print("3.MATIKAN APP")
    print("4.QUIT")
    opsi = input("\nMasukan Opsi: ")

    if opsi == "1":
        print("\n++++OPSI VOLUME++++")
        print("1.STEL VOLUME")
        print("2.NAIK/TURUN OTOMATIS")
        opsi_volume = input("\nPilih opsi: ")
        
        if opsi_volume == "1":
            volume = float(input("Berapa volume (0.0 - 1.0): "))
            cast.set_volume(volume)
            print("Volume disetel.")
        elif opsi_volume == "2":
            waktu_tunggu = float(input("Berapa detik jeda sebelum mulai: "))
            durasi_lama = float(input("Berapa detik durasi looping: "))
            
            print(f"Menunggu {waktu_tunggu} detik...")
            time.sleep(waktu_tunggu)
            
            waktu_mulai = time.time()
            print("Looping volume dimulai...")
            while time.time() - waktu_mulai < durasi_lama:
                cast.set_volume(0.1)
                time.sleep(0.5)
                if time.time() - waktu_mulai >= durasi_lama: break
                cast.set_volume(0.8)
                time.sleep(0.5)
            print("Looping selesai.")

    elif opsi == "2":
        YOUTUBE_APP_ID = '233637DE'
        
        # 1. Pastikan Input Bersih
        video_id_raw = input("\nMasukan ID Youtube (Contoh: dQw4w9WgXcQ): ")
        if "v=" in video_id_raw:
            video_id = video_id_raw.split("v=")[-1].split("&")[0]
        elif "youtu.be" in video_id_raw:
            video_id = video_id_raw.split("/")[-1]
        else:
            video_id = video_id_raw
            
        print(f"[*] Target ID: {video_id}")

        # 2. Inisialisasi Controller
        yt = YouTubeController()
        cast.register_handler(yt)
        
        # 3. CLEAN START (Matikan app dulu biar sesi baru)
        print("[*] Mematikan sesi YouTube lama...")
        cast.quit_app() 
        time.sleep(3) # Tunggu benar-benar mati

        # 4. Buka App Baru
        print("[*] Membuka YouTube...")
        cast.start_app(YOUTUBE_APP_ID)
        
        # 5. Tunggu Sesi Aktif (Logic Penting!)
        print("[*] Menunggu aplikasi siap...")
        timeout = 0
        while True:
            time.sleep(1)
            timeout += 1
            # Cek apakah App ID di TV sudah YouTube
            if cast.app_id == YOUTUBE_APP_ID:
                print("[+] Aplikasi terdeteksi aktif!")
                break
            if timeout > 20:
                print("(!) Timeout menunggu aplikasi.")
                break
        
        # Jeda Wajib untuk Android TV (Loading Animation)
        print("[*] Buffer 5 detik untuk loading screen...")
        time.sleep(5)

        # 6. DOUBLE TAP STRATEGY
        # Tembak perintah pertama
        print("[*] Percobaan putar ke-1...")
        yt.play_video(video_id)
        
        # Seringkali yang pertama diabaikan karena inisialisasi player
        time.sleep(2)
        
        # Tembak perintah kedua (Biasanya ini yang berhasil)
        print("[*] Percobaan putar ke-2 (Memaksa)...")
        yt.play_video(video_id)
        
        print("[+] Selesai.")

    elif opsi == "3":
        cast.quit_app()
        print("\nBerhasil Dimatikan...")

    elif opsi == "4":
        print("\nKeluar dari program...")

    else:
        print("Opsi Tidak Tersedia")

else:
    print(f"Gagal menemukan info cast untuk IP {ip_target}")

stop_discovery(browser)
