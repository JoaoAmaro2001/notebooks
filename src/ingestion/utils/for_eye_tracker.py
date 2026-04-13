# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                              IMPORT LIBRARIES                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pandas as pd
import os

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                          PROCESSING FUNCTIONS                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def _convert_pupil_time_to_timestamp(df):
    if df is None or df.empty:
        return df
    if "PupilTime" not in df.columns:
        return df

    df["time"] = pd.to_datetime(df["PupilTime"], unit="ns", errors="coerce")
    return df


def _ensure_datetime_index(df):
    if df is None or df.empty:
        return df

    df = _convert_pupil_time_to_timestamp(df)

    if not pd.api.types.is_datetime64_any_dtype(df.index):
        if "time" in df.columns:
            df = df.set_index(df["time"])
        else:
            df.index = pd.to_datetime(df.index, errors="coerce")
    return df.sort_index()


def build_eye_tracker_table(dataset, include_raw_frames=False, tolerance_ms=100):
    """Return a merged table for PupilLabs decoded frames and gaze data."""
    decoded_frames = dataset.streams.PupilLabs.DecodedFrames.data.copy()
    gaze = dataset.streams.PupilLabs.PupilGaze.data.copy()

    if decoded_frames.empty or gaze.empty:
        raise ValueError("DecodedFrames or PupilGaze stream is empty.")

    decoded_frames = decoded_frames[decoded_frames["Value"] != 0].copy()
    decoded_frames = _ensure_datetime_index(decoded_frames)
    gaze = _ensure_datetime_index(gaze)

    merged = pd.merge_asof(
        decoded_frames,
        gaze,
        left_index=True,
        right_index=True,
        direction="nearest",
        tolerance=pd.Timedelta(milliseconds=tolerance_ms),
        suffixes=("_frame", "_gaze"),
    )

    if include_raw_frames and hasattr(dataset.streams.PupilLabs, "RawFrames"):
        raw_frames = dataset.streams.PupilLabs.RawFrames.data.copy()
        raw_frames = _ensure_datetime_index(raw_frames)
        merged = pd.merge_asof(
            merged,
            raw_frames,
            left_index=True,
            right_index=True,
            direction="nearest",
            tolerance=pd.Timedelta(milliseconds=tolerance_ms),
            suffixes=("", "_raw"),
        )

    return merged


def export_eye_tracker_table(dataset, outdir, filename="eye_tracker_table.csv", **kwargs):
    table = build_eye_tracker_table(dataset, **kwargs)
    table = table.reset_index()
    if table.columns[0] == "index":
        table.rename(columns={"index": "Timestamp"}, inplace=True)

    os.makedirs(outdir, exist_ok=True)
    table.to_csv(os.path.join(outdir, filename), index=False)
    return table

    