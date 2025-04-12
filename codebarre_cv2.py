import cv2
from pyzbar.pyzbar import decode as decode_1d
from pylibdmtx.pylibdmtx import decode as decode_2d
import csv
from datetime import datetime
import time
import threading


current_frame = None  
scan_result = ""      
db = {}               

# Load the medication database from CSV
def load_database(csv_path='medications.csv'):
    local_db = {}
    try:
        with open(csv_path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                barcode = row['barcode'].strip()
                local_db[barcode] = {
                    'name': row['name'].strip(),
                    'batch': row['batch'].strip(),
                    'expiry': row['expiry_date'].strip()
                }
    except Exception as e:
        print(f"Error loading CSV: {e}")
    return local_db

# Look up medication info using the scanned barcode
def check_medication(barcode, database):
    barcode = barcode.strip()
    if barcode in database:
        med = database[barcode]
        expiry_date = datetime.strptime(med['expiry'], "%Y-%m-%d")
        expired = expiry_date < datetime.today()
        result = f"Name: {med['name']}, Batch: {med['batch']}, Expiry: {med['expiry']}"
        if expired:
            result += " (EXPIRED)"
        else:
            result += " (Valid)"
        return result
    return None

# Thread function for scanning barcodes without blocking the display loop
def scanning_thread():
    global current_frame, scan_result, db
    cooldown = 3  # seconds between accepting new scans for the same barcode
    last_scan_time = 0
    while True:
        if current_frame is None:
            time.sleep(0.1)
            continue
        # Make a copy of the current frame to avoid conflicts
        frame_copy = current_frame.copy()
        # Resize to speed up processing
        small_frame = cv2.resize(frame_copy, (320, 240))
        # Decode both 1D and 2D barcodes
        codes = decode_1d(small_frame) + decode_2d(small_frame)
        if codes:
            # Take only the first detected barcode
            code = codes[0]
            barcode_data = code.data.decode('utf-8').strip()
            now = time.time()
            if now - last_scan_time > cooldown:
                result = check_medication(barcode_data, db)
                if result:
                    scan_result = f"Detected: {barcode_data}\n{result}"
                else:
                    scan_result = f"Detected: {barcode_data}\nUnknown barcode"
                last_scan_time = now
        time.sleep(0.1)  # Slight delay to reduce CPU load

# Main function: capture frames and display them with scan results overlaid
def main():
    global current_frame, scan_result, db

    # Load database from CSV
    db = load_database()

    # Start the camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Start the scanning thread
    thread = threading.Thread(target=scanning_thread, daemon=True)
    thread.start()

    print("Running fast medication scanner. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        # Update the global frame for the scanning thread
        current_frame = frame.copy()

        # Overlay the latest scan result on the frame
        if scan_result:
            y0, dy = 30, 30
            for i, line in enumerate(scan_result.split('\n')):
                y = y0 + i * dy
                cv2.putText(frame, line, (10, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Medication Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
