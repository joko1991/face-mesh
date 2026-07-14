"""
Face Mesh - "jak działa deepfake"
=========================================================
Nakłada siatkę geometrii twarzy (468 punktów, MediaPipe) na Twoje nagranie.

Instalacja (w venv):
    pip install mediapipe opencv-python

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
        trail = None
        scan_position = 0
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
                    elif style == "neon":

                        print("NEON ACTIVE")

                        overlay = frame.copy()

                        neon_mesh_spec = mp_drawing.DrawingSpec(
                            color=(255, 0, 255),
                            thickness=2,
                            circle_radius=0
                        )

                        neon_dot_spec = mp_drawing.DrawingSpec(
                            color=(0, 255, 255),
                            thickness=2,
                            circle_radius=3
                        )

                        mp_drawing.draw_landmarks(
                            image=overlay,
                            landmark_list=landmarks,
                            connections=mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=neon_dot_spec,
                            connection_drawing_spec=neon_mesh_spec,
                        )

                        glow = cv2.GaussianBlur(overlay, (0, 0), 10)

                        frame = cv2.addWeighted(
                            overlay,
                            1.5,
                            glow,
                            0.5,
                            0
                        )
                    elif style == "hologram":

                        if trail is None:
                            trail = frame.copy()

                        overlay = frame.copy()

                        hologram_mesh = mp_drawing.DrawingSpec(
                            color=(255, 80, 200),  # różowo-fioletowa siatka
                            thickness=1,
                            circle_radius=0
                        )

                        hologram_points = mp_drawing.DrawingSpec(
                            color=(255, 255, 255),
                            thickness=2,
                            circle_radius=3
                        )

                        mp_drawing.draw_landmarks(
                            image=overlay,
                            landmark_list=landmarks,
                            connections=mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=hologram_points,
                            connection_drawing_spec=hologram_mesh,
                        )

                        # delikatna poświata
                        glow = cv2.GaussianBlur(
                            overlay,
                            (0, 0),
                            5
                        )

                        overlay = cv2.addWeighted(
                            overlay,
                            1.5,
                            glow,
                            0.5,
                            0
                        )

                        # motion trail
                        trail = cv2.addWeighted(
                            trail,
                            0.8,
                            overlay,
                            0.2,
                            0
                        )

                        frame = cv2.addWeighted(
                            frame,
                            0.5,
                            trail,
                            0.5,
                            0
                        )
                    elif style == "scan":

                        overlay = frame.copy()

                        # przesuwanie linii skanującej
                        scan_position = (scan_position + 15) % frame.shape[1]

                        # rysowanie linii
                        cv2.line(
                            overlay,
                            (scan_position, 0),
                            (scan_position, frame.shape[0]),
                            (255, 255, 0),
                            2
                        )

                        scan_zone = frame.copy()

                        mesh_spec = mp_drawing.DrawingSpec(
                            color=(255, 255, 0),
                            thickness=1,
                            circle_radius=0
                        )

                        dot_spec = mp_drawing.DrawingSpec(
                            color=(255, 255, 255),
                            thickness=2,
                            circle_radius=2
                        )

                        mp_drawing.draw_landmarks(
                            image=scan_zone,
                            landmark_list=landmarks,
                            connections=mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=dot_spec,
                            connection_drawing_spec=mesh_spec,
                        )

                        # maska - mesh tylko za linią skanu
                        mask = cv2.cvtColor(scan_zone, cv2.COLOR_BGR2GRAY)

                        _, mask = cv2.threshold(
                            mask,
                            10,
                            255,
                            cv2.THRESH_BINARY
                        )

                        frame = cv2.addWeighted(
                            frame,
                            0.7,
                            scan_zone,
                            0.3,
                            0
                        )

                        frame = cv2.addWeighted(
                            frame,
                            1,
                            overlay,
                            0.3,
                            0
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
        choices=["mesh", "dots", "contours", "neon", "hologram", "scan"],
        default="mesh",
        help="Styl wizualizacji (domyślnie: mesh)",
    )
    args = parser.parse_args()
    process_video(args.input, args.output, args.style)
