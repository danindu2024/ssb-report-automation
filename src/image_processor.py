"""
Image processing pipeline for SSB Monthly Report Automation.
Handles event photos, director headshots, and signatures.

Based on: img processing strategy.md
"""
import os
from pathlib import Path
from PIL import Image, ExifTags

from config import IMAGE_SPECS, ASSETS_DIR


def auto_rotate(img):
    """
    Fix image orientation based on EXIF data (from phone cameras).
    Without this, portrait photos taken on phones appear sideways.
    """
    try:
        exif_data = img._getexif()
        if exif_data is None:
            return img

        # Find the orientation tag key
        orientation_key = next(
            (k for k, v in ExifTags.TAGS.items() if v == 'Orientation'), None
        )
        if orientation_key is None:
            return img

        orientation_value = exif_data.get(orientation_key)

        rotation_map = {3: 180, 6: 270, 8: 90}
        if orientation_value in rotation_map:
            img = img.rotate(rotation_map[orientation_value], expand=True)

    except (AttributeError, Exception):
        pass  # No EXIF data or non-JPEG — use image as-is

    return img


def smart_crop(img, target_aspect_ratio):
    """
    Crop image to target aspect ratio, preserving center content.
    Implements the near-match tolerance check missing from the original.

    Args:
        img: PIL Image object
        target_aspect_ratio: e.g., 4/3 for landscape, 1/1 for square

    Returns:
        Cropped PIL Image
    """
    current_width, current_height = img.size
    current_aspect = current_width / current_height

    # Near-match tolerance — avoid unnecessary crop
    if abs(current_aspect - target_aspect_ratio) < 0.01:
        return img

    if current_aspect > target_aspect_ratio:
        # Image is wider than target → crop sides
        new_width = int(current_height * target_aspect_ratio)
        left = (current_width - new_width) // 2
        return img.crop((left, 0, left + new_width, current_height))
    else:
        # Image is taller than target → crop top/bottom
        new_height = int(current_width / target_aspect_ratio)
        top = (current_height - new_height) // 2
        return img.crop((0, top, current_width, top + new_height))


def _process_folder(raw_folder, processed_folder, spec_key):
    """
    Generic processor for a single image folder.
    Reads from raw_folder, writes sequentially named files to processed_folder.

    Args:
        raw_folder:       Path - where original uploads live
        processed_folder: Path - where processed files are saved
        spec_key:         str  - key into IMAGE_SPECS ("event", "director", "signature")

    Returns:
        int - count of processed images
    """
    spec = IMAGE_SPECS[spec_key]
    target_w = spec["width"]
    target_h = spec["height"]
    quality = spec["quality"]
    target_aspect = target_w / target_h

    processed_folder.mkdir(parents=True, exist_ok=True)

    # Supported source formats
    supported_exts = {'.jpg', '.jpeg', '.png'}

    photo_count = 1
    processed_files = []

    for img_file in sorted(raw_folder.glob("*")):
        if img_file.suffix.lower() not in supported_exts:
            continue

        try:
            img = Image.open(img_file).convert("RGB")

            # Step 1: Auto-rotate based on EXIF
            img = auto_rotate(img)

            # Step 2: Minimum resolution check (1024px width per spec)
            if img.width < 1024 and spec_key == "event":
                print(f"  ⚠️  Skipping {img_file.name}: width {img.width}px below minimum (1024px)")
                continue

            # Step 3: Smart center crop to target aspect ratio
            img_cropped = smart_crop(img, target_aspect)

            # Step 4: Resize to standard dimensions
            img_resized = img_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

            # Step 5: Save with sequential name (01.jpg, 02.jpg, ...)
            output_filename = f"{photo_count:02d}.jpg"
            output_file = processed_folder / output_filename

            save_kwargs = {"quality": quality, "optimize": True}
            if spec_key != "signature":
                save_kwargs["progressive"] = True  # Progressive JPEG for events/directors

            img_resized.save(output_file, "JPEG", **save_kwargs)
            processed_files.append(str(output_file))
            photo_count += 1

        except Exception as e:
            print(f"  ❌ Error processing {img_file.name}: {e}")

    return len(processed_files)


def process_all_event_images(events_data):
    """
    Process all event photo folders referenced in the events data.
    Reads from: assets/images/events/raw/{PHOTO_FOLDER}/
    Writes to:  assets/images/events/processed/{PHOTO_FOLDER}/

    Args:
        events_data: list of event row dicts extracted by data_loader
    """
    if not events_data:
        print("  No events data. Skipping image processing.")
        return

    raw_root = ASSETS_DIR / "images" / "events" / "raw"
    processed_root = ASSETS_DIR / "images" / "events" / "processed"

    total_processed = 0

    for event in events_data:
        photo_folder = event.get("PHOTO_FOLDER")
        if not photo_folder:
            continue

        raw_folder = raw_root / str(photo_folder)
        if not raw_folder.exists():
            print(f"  ⚠️  Raw folder not found: {raw_folder}")
            continue

        processed_folder = processed_root / str(photo_folder)
        print(f"  Processing event folder: {photo_folder}")

        count = _process_folder(raw_folder, processed_folder, "event")
        total_processed += count
        print(f"    ✓ {count} images processed → {processed_folder}")

    print(f"✓ Event image processing complete. Total: {total_processed} images.")


def process_director_photos():
    """
    Process all board member headshots to square format (400×400).
    Reads from: assets/images/directors/raw/DIRECTOR_*.jpg
    Writes to:  assets/images/directors/processed/
    """
    raw_dir = ASSETS_DIR / "images" / "directors" / "raw"
    processed_dir = ASSETS_DIR / "images" / "directors" / "processed"

    if not raw_dir.exists():
        print(f"  ⚠️  Director raw folder not found: {raw_dir}")
        return

    processed_dir.mkdir(parents=True, exist_ok=True)
    spec = IMAGE_SPECS["director"]
    count = 0

    for img_file in raw_dir.glob("DIRECTOR_*.jpg"):
        try:
            img = Image.open(img_file).convert("RGB")
            img = auto_rotate(img)
            img_cropped = smart_crop(img, spec["width"] / spec["height"])
            img_resized = img_cropped.resize((spec["width"], spec["height"]), Image.Resampling.LANCZOS)
            output_file = processed_dir / img_file.name
            img_resized.save(output_file, "JPEG", quality=spec["quality"], optimize=True)
            count += 1
        except Exception as e:
            print(f"  ❌ Error processing {img_file.name}: {e}")

    print(f"✓ Director photo processing complete. {count} photos processed.")
