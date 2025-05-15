# level_up_drills/06_large_binary_data/handle_images.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
# This is a workaround for environments where python -m doesn't automatically
# add the package root (the directory containing shared.py for this package)
# to sys.path correctly.
import sys
import os
from typing import Optional

# Get the directory of the current script (06_large_binary_data)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (level_up_drills)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py for this package.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


# This script illustrates storing large binary data (images)
# using two approaches: BLOBs in the database vs. file paths.

# Import necessary components and MODELS from shared.py
# REMOVE 'Base' and 'create_tables' from this import, as the model definitions should be ONLY in shared.py.
from shared import SessionLocal, engine, UserProfileBlob, UserProfileFilePath # Use appropriate SessionLocal/engine and import models

from sqlalchemy import Column, Integer, LargeBinary, String # Still needed for types if defining elsewhere or for context
from sqlalchemy.orm import Session # For type hinting
import os # For file path handling
import datetime # For generating unique filenames
import uuid # Alternative for unique filenames
import io # To simulate binary data

# --- REMOVE MODEL DEFINITIONS FROM HERE ---
# The definitions of class UserProfileBlob(Base): ... and
# class UserProfileFilePath(Base): ... should be ONLY in shared.py.
# Delete those entire class definition blocks from THIS file.


# Ensure tables exist (run once before saving images)
# ... (comments on running create_tables) ...

# --- Configuration for File Path Storage ---
# Define UPLOAD_DIRECTORY relative to the script's location for clarity
UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), "user_images")

# --- Functions for BLOB Storage ---
def save_image_as_blob(user_id: int, image_bytes: bytes) -> Optional[UserProfileBlob]:
    """Saves image bytes directly into the database as a BLOB."""
    db = SessionLocal()
    try:
        # Check if a profile already exists for this user
        existing_profile = db.query(UserProfileBlob).filter(UserProfileBlob.user_id == user_id).first()

        if existing_profile:
             # Update existing profile
             existing_profile.profile_image = image_bytes
             db.commit()
             print(f"Updated BLOB profile for user ID {user_id}.")
             db.refresh(existing_profile)
             return existing_profile
        else:
             # Create a new profile
             profile = UserProfileBlob(user_id=user_id, profile_image=image_bytes)
             db.add(profile)
             db.commit()
             db.refresh(profile)
             print(f"Created BLOB profile for user ID {user_id}.")
             return profile

    except Exception as e:
        db.rollback()
        print(f"Error saving image BLOB for user ID {user_id}: {e}")
        return None
    finally:
        db.close()

def get_image_blob(user_id: int) -> Optional[bytes]:
    """Retrieves image bytes stored as a BLOB."""
    db = SessionLocal()
    try:
        profile = db.query(UserProfileBlob.profile_image).filter(UserProfileBlob.user_id == user_id).first()
        return profile[0] if profile else None
    except Exception as e:
        print(f"Error retrieving image BLOB for user ID {user_id}: {e}")
        return None
    finally:
        db.close()


# --- Functions for File Path Storage ---
def save_image_as_filepath(user_id: int, image_bytes: bytes, upload_dir: str = UPLOAD_DIRECTORY) -> Optional[UserProfileFilePath]:
    """Saves image bytes to the filesystem and stores the path in the database."""
    db = SessionLocal()
    filepath = None # Define filepath outside try for potential cleanup
    try:
        # Ensure the upload directory exists
        os.makedirs(upload_dir, exist_ok=True)

        # Generate a unique filename (timestamp + uuid is robust)
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = uuid.uuid4().hex[:8] # Use part of a UUID
        # Define a more robust filename to avoid clashes and provide some info
        filename = f"user_{user_id}_{timestamp_str}_{unique_id}.bin" # Use .bin or appropriate extension if known
        filepath = os.path.join(upload_dir, filename)

        # Write the image bytes to the file
        with open(filepath, 'wb') as f:
            f.write(image_bytes)

        # Check if a profile already exists for this user
        existing_profile = db.query(UserProfileFilePath).filter(UserProfileFilePath.user_id == user_id).first()

        if existing_profile:
             # Optional: Clean up the old file before updating the path
             old_filepath = existing_profile.image_path
             if old_filepath and os.path.exists(old_filepath):
                  try:
                      os.remove(old_filepath)
                      print(f"Deleted old image file: {old_filepath}")
                  except OSError as e:
                      print(f"Warning: Could not delete old image file {old_filepath}: {e}")

             # Update existing profile with the new path
             existing_profile.image_path = filepath
             db.commit()
             print(f"Updated file path profile for user ID {user_id}.")
             db.refresh(existing_profile)
             return existing_profile
        else:
             # Create a new profile
             profile = UserProfileFilePath(user_id=user_id, image_path=filepath)
             db.add(profile)
             db.commit()
             db.refresh(profile)
             print(f"Created file path profile for user ID {user_id}.")
             return profile


    except Exception as e:
        # Important: If DB commit fails, the file might be orphaned.
        # Needs cleanup logic here if the DB operation fails after saving the file.
        db.rollback()
        print(f"Error saving image file path for user ID {user_id}: {e}")
        # Optional: Clean up the created file if the DB operation failed
        if filepath and os.path.exists(filepath):
            try: os.remove(filepath)
            except OSError: pass
        return None
    finally:
        db.close()


def get_image_filepath(user_id: int) -> Optional[str]:
    """Retrieves the image file path from the database."""
    db = SessionLocal()
    try:
        profile = db.query(UserProfileFilePath.image_path).filter(UserProfileFilePath.user_id == user_id).first()
        return profile[0] if profile else None
    except Exception as e:
        print(f"Error retrieving image file path for user ID {user_id}: {e}")
        return None
    finally:
        db.close()

def load_image_from_filepath(filepath: str) -> Optional[bytes]:
    """Loads image bytes from a given file path on the filesystem."""
    if not filepath or not os.path.exists(filepath):
        print(f"Error: File not found at path: {filepath}")
        return None
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except IOError as e:
        print(f"Error reading file at {filepath}: {e}")
        return None

if __name__ == "__main__":
    # Ensure UserProfileBlob and UserProfileFilePath tables exist
    # Add these models to your shared.py Base.metadata
    # and run create_tables() or create_async_tables() once before running this script.
    # You can add a temporary call here for setup if needed:
    # from shared import create_tables # Or create_async_tables
    # create_tables() # Call it once for setup

    # --- Simulate some binary image data ---
    # In a real app, this would come from a file upload etc.
    # Using simple byte strings for illustration
    dummy_image_data_small = b"\x89PNG\r\n\x1a\n" + os.urandom(1024) # Small dummy PNG data
    dummy_image_data_large = b"x" * 1024 * 1024 * 5 # 5MB of 'x' bytes

    user_id_1 = 1 # Example user ID (doesn't need to exist in 'users' table)
    user_id_2 = 2 # Example user ID

    # Clean up potential old files from previous runs
    if os.path.exists(UPLOAD_DIRECTORY):
         try:
             import shutil
             shutil.rmtree(UPLOAD_DIRECTORY)
             print(f"Cleaned up old upload directory: {UPLOAD_DIRECTORY}")
         except Exception as e:
             print(f"Warning: Could not clean up upload directory: {e}")


    # --- Scenario 1: Store as BLOB ---
    print("\n--- Demonstrating BLOB Storage ---")

    # Save a small image BLOB
    print(f"Saving small image as BLOB for user ID {user_id_1} ({len(dummy_image_data_small)} bytes)...")
    saved_blob_profile_small = save_image_as_blob(user_id_1, dummy_image_data_small)

    # Save a large image BLOB (can be slower/use more DB resources)
    print(f"Saving large image as BLOB for user ID {user_id_2} ({len(dummy_image_data_large)} bytes)...")
    saved_blob_profile_large = save_image_as_blob(user_id_2, dummy_image_data_large)

    # Retrieve BLOBs
    retrieved_blob_small = get_image_blob(user_id_1)
    if retrieved_blob_small:
        print(f"Retrieved BLOB for user ID {user_id_1}: {len(retrieved_blob_small)} bytes.")

    retrieved_blob_large = get_image_blob(user_id_2)
    if retrieved_blob_large:
        print(f"Retrieved BLOB for user ID {user_id_2}: {len(retrieved_blob_large)} bytes.")


    # --- Scenario 2: Store as File Path ---
    print("\n--- Demonstrating File Path Storage ---")

    # Save a small image to file and store path
    print(f"Saving small image to file path for user ID {user_id_1} ({len(dummy_image_data_small)} bytes)...")
    saved_filepath_profile_small = save_image_as_filepath(user_id_1, dummy_image_data_small, UPLOAD_DIRECTORY)

    # Save a large image to file and store path
    print(f"Saving large image to file path for user ID {user_id_2} ({len(dummy_image_data_large)} bytes)...")
    saved_filepath_profile_large = save_image_as_filepath(user_id_2, dummy_image_data_large, UPLOAD_DIRECTORY)


    # Retrieve file paths and then load files
    retrieved_filepath_small = get_image_filepath(user_id_1)
    if retrieved_filepath_small:
        print(f"Retrieved path for user ID {user_id_1}: {retrieved_filepath_small}")
        loaded_file_small = load_image_from_filepath(retrieved_filepath_small)
        if loaded_file_small:
            print(f"Loaded file content: {len(loaded_file_small)} bytes.")

    retrieved_filepath_large = get_image_filepath(user_id_2)
    if retrieved_filepath_large:
        print(f"Retrieved path for user ID {user_id_2}: {retrieved_filepath_large}")
        loaded_file_large = load_image_from_filepath(retrieved_filepath_large)
        if loaded_file_large:
            print(f"Loaded file content: {len(loaded_file_large)} bytes.")

    # You can manually check the 'user_images' directory created
    # and the size of the database file vs the size of the image files.