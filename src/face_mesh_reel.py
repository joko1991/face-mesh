"""
Face Mesh - "jak działa deepfake"
=========================================================
Nakłada siatkę geometrii twarzy (468 punktów, MediaPipe) na Twoje nagranie.

Instalacja (w venv):
    pip install mediapipe opencv-python

Użycie:
    python face_mesh_reel.py input.mp4 output.mp4 --style mesh
    python face_mesh_reel.py input.mp4 output.mp4 --style dots
    python face_mesh_reel.py input.mp4 output.mp4 --style contours

Style:
    mesh     - pełna siatka trójkątów (najbardziej "techniczny" look)
    dots     - same punkty (minimalistycznie, ładne na jasnym tle)
    contours - kontury twarzy, oczu, ust (czytelne, mniej "gęste")

"""

import argparse
import sys

import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

# Kolor siatki — dobrany pod chłodną paletę (możesz zmienić na swój brand)
# Format BGR (nie RGB!)
MESH_COLOR = (200, 160, 80)      # chłodny niebieski
DOT_COLOR = (230, 200, 120)      # jaśniejszy akcent


def process_video(input_path: str, output_path: str, style: str) -> None:
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        sys.exit(f"Nie mogę otworzyć pliku: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    mesh_spec = mp_drawing.DrawingSpec(color=MESH_COLOR, thickness=1, circle_radius=0)
    dot_spec = mp_drawing.DrawingSpec(color=DOT_COLOR, thickness=1, circle_radius=1)

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as face_mesh:
        frame_idx = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame_idx += 1

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                for landmarks in results.multi_face_landmarks:
                    if style == "mesh":
                        mp_drawing.draw_landmarks(
                            image=frame,
                            landmark_list=landmarks,
                            connections=mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mesh_spec,
                        )
                    elif style == "dots":
                        mp_drawing.draw_landmarks(
                            image=frame,
                            landmark_list=landmarks,
                            connections=None,
                            landmark_drawing_spec=dot_spec,
                            connection_drawing_spec=None,
                        )
                    elif style == "contours":
                        mp_drawing.draw_landmarks(
                            image=frame,
                            landmark_list=landmarks,
                            connections=mp_face_mesh.FACEMESH_CONTOURS,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_styles
                            .get_default_face_mesh_contours_style(),
                        )

            out.write(frame)
            if frame_idx % 30 == 0:
                print(f"\rKlatka {frame_idx}/{total}", end="", flush=True)

    cap.release()
    out.release()
    print(f"\nGotowe: {output_path}")
    print("Uwaga: plik wyjściowy jest bez dźwięku — podłóż audio w CapCut/DaVinci.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face mesh overlay na wideo")
    parser.add_argument("input", help="Ścieżka do nagrania wejściowego (mp4)")
    parser.add_argument("output", help="Ścieżka pliku wyjściowego (mp4)")
    parser.add_argument(
        "--style",
        choices=["mesh", "dots", "contours"],
        default="mesh",
        help="Styl wizualizacji (domyślnie: mesh)",
    )
    args = parser.parse_args()
    process_video(args.input, args.output, args.style)
