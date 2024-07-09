import argparse
import cv2
import sys

def main():
    # Buat argumen, parsing, dan parsing argumen
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True, help="video.mp4")
    args = vars(ap.parse_args())

    # Memuat video
    camVideo = cv2.VideoCapture(args["video"])

    # Periksa apakah jalur video valid
    if not camVideo.isOpened():
        print(f"Error: Could not open video file {args['video']}")
        sys.exit(1)

    # Mendapatkan lebar, tinggi, dan FPS video asli
    frame_width = int(camVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(camVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = camVideo.get(cv2.CAP_PROP_FPS)

    # Menentukan codec dan membuat objek VideoWriter untuk menyimpan video
    output_path = 'output_video.avi'
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Terus ulang
    while True:
        # Ambil bingkai saat ini dan inisialisasi status teks
        (grabbed, frame) = camVideo.read()
        status = "No Target in sight"

        # Periksa untuk melihat apakah kita telah mencapai akhir video
        if not grabbed:
            break

        # Ubah bingkai menjadi skala abu-abu, buramkan, dan deteksi tepinya
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)  # Blur
        edged = cv2.Canny(blurred, 50, 150)  # Canny edge detection

        # Temukan kontur di peta tepi
        cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Lingkaran kontur
        for cnt in cnts:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) == 5:
                cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                status = "Target(s) in sight!"

        # Menggambar status teks pada bingkai
        cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Tampilkan pembingkaian dan rekam jika ada tombol yang ditekan
        cv2.imshow("Frame", frame)

        # Menyimpan frame ke file output video
        out.write(frame)

        key = cv2.waitKey(1) & 0xFF
        # Jika tombol 's' ditekan, hentikan perulangan
        if key == ord("s"):
            break

    # Bersihkan input rekaman video, tutup semua jendela yang terbuka, dan video writer
    camVideo.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
