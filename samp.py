import os
import httpx
import zipfile
import time

# Define the exact 7-character code map for the full book ZIP configurations
books_to_download = {
    "Class_11_Maths_Part1": "kemh1dd",
    "Class_11_Physics_Part1": "keph1dd",
    "Class_11_Physics_Part2": "keph2dd",
    "Class_12_Maths_Part1": "lemh1dd",
    "Class_12_Maths_Part2": "lemh2dd",
    "Class_12_Physics_Part1": "leph1dd",
    "Class_12_Physics_Part2": "leph2dd"
}

def download_and_extract_ncert():
    # Setup working folders
    base_dir = "NCERT_Complete_Library"
    os.makedirs(base_dir, exist_ok=True)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Initialize connection pipeline
    with httpx.Client(headers=headers, timeout=120.0) as client:
        for book_name, code in books_to_download.items():
            url = f"https://ncert.nic.in/textbook/pdf/{code}.zip"
            zip_file_path = os.path.join(base_dir, f"{book_name}.zip")
            extraction_folder = os.path.join(base_dir, book_name)
            
            print(f"[INFO] Fetching full archive for {book_name}...")
            
            try:
                response = client.get(url)
                
                if response.status_code == 200:
                    # 1. Save the downloaded binary data as a .zip file
                    with open(zip_file_path, "wb") as f:
                        f.write(response.content)
                    print(f"[SUCCESS] Downloaded archive: {zip_file_path}")
                    
                    # 2. Extract the content automatically on-the-fly
                    print(f"[PROCESS] Unzipping chapters into '{book_name}/'...")
                    os.makedirs(extraction_folder, exist_ok=True)
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                        zip_ref.extractall(extraction_folder)
                    
                    # 3. Clean up the residual .zip file to save storage space
                    os.remove(zip_file_path)
                    print(f"[CLEANUP] Deleted raw zip file. Book files are organized.\n")
                    
                else:
                    print(f"[ERROR] NCERT returned an error code {response.status_code} for {book_name}\n")
                    
            except Exception as e:
                print(f"[CRITICAL] Connection failure on {book_name}: {e}\n")
                
            # Polite cooldown buffer for government infrastructure servers
            time.sleep(3)

if __name__ == "__main__":
    print("=====================================================")
    print("  NCERT Automatic Single-Stream Portfolio Ingestor   ")
    print("=====================================================")
    download_and_extract_ncert()
    print("[FINISHED] All requested Mathematics and Physics volumes are compiled!")