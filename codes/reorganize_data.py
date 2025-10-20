import os
import shutil

def reorganize_chest_xray_data(base_chest_xray_dir: str):
    """
    Reorganizes the chest_xray dataset (located in 'base_chest_xray_dir')
    into 3 classes (NORMAL, VIRAL, BACTERIAL).
    
    It assumes the starting structure is:
    - {base_chest_xray_dir}/train/NORMAL/
    - {base_chest_xray_dir}/train/PNEUMONIA/
    
    It will transform it into:
    - {base_chest_xray_dir}/train/NORMAL/ (untouched)
    - {base_chest_xray_dir}/train/VIRAL/ (new folder)
    - {base_chest_xray_dir}/train/BACTERIAL/ (renamed from PNEUMONIA)

    Args:
        base_chest_xray_dir (str): The path to the 'chest_xray' directory.
                                   (e.g., 'codes/data/chest_xray')
    """
    
    # Iterate over 'train', 'test', and 'val'
    for set_name in ['train', 'test', 'val']:
        print(f"--- Processing folder: {set_name} ---")
        
        # Path to the specific set (e.g., .../codes/data/chest_xray/train)
        set_path = os.path.join(base_chest_xray_dir, set_name)
        
        if not os.path.exists(set_path):
            print(f"WARNING: Folder {set_path} not found. Skipping.")
            continue

        # Define paths for the original and new directories
        pneumonia_path = os.path.join(set_path, 'PNEUMONIA')
        viral_path = os.path.join(set_path, 'VIRAL')
        # This is the target name for the renamed PNEUMONIA folder
        bacterial_path = os.path.join(set_path, 'BACTERIAL') 
        
        # --- Safety Checks ---
        if not os.path.exists(pneumonia_path):
            if os.path.exists(bacterial_path) and os.path.exists(viral_path):
                print(f"Folder 'PNEUMONIA' not found in {set_path}.")
                print("Looks like this folder has already been reorganized. Skipping.")
            else:
                print(f"ERROR: Folder '{pneumonia_path}' not found! Cannot proceed.")
            continue
            
        # 1. Create the new 'VIRAL' directory
        os.makedirs(viral_path, exist_ok=True)
        print(f"Created/verified folder: {viral_path}")

        files_moved = 0
        
        # 2. Iterate through all files in 'PNEUMONIA'
        try:
            for filename in os.listdir(pneumonia_path):
                src_file_path = os.path.join(pneumonia_path, filename)
                
                # Check if it's a file (and not a subfolder)
                if not os.path.isfile(src_file_path):
                    continue
                
                # 3. If 'virus' is in the name, move it to 'VIRAL'
                if 'virus' in filename.lower():
                    dst_file_path = os.path.join(viral_path, filename)
                    try:
                        shutil.move(src_file_path, dst_file_path)
                        files_moved += 1
                    except Exception as e:
                        print(f"Error moving {src_file_path}: {e}")
        except Exception as e:
            print(f"Error reading {pneumonia_path}: {e}")
            continue # Skip to the next set ('test' or 'val')

        print(f"Moved {files_moved} 'virus' files to {viral_path}")
        
        # 4. Rename 'PNEUMONIA' (which now only has bacteria) to 'BACTERIAL'
        try:
            os.rename(pneumonia_path, bacterial_path)
            print(f"Renamed '{pneumonia_path}' to '{bacterial_path}'")
        except Exception as e:
            print(f"Error renaming {pneumonia_path}: {e}")
            
    print("\n--- Reorganization Complete! ---")
    print("Your data is now in 3 classes: NORMAL, VIRAL, BACTERIAL.")

# --- Main execution ---
if __name__ == "__main__":
    # This script (e.g., reorganize_data.py) is in the 'codes' folder.
    
    # Get the current working directory (e.g., '.../codes')
    current_dir = os.getcwd() 
    
    # --- THIS IS THE CORRECT PATH ---
    # The 'chest_xray' folder is at 'codes/data/chest_xray'
    base_chest_xray_dir = os.path.join(current_dir, 'data', 'chest_xray')
    
    if not os.path.exists(base_chest_xray_dir):
        print(f"Error: Directory not found at {base_chest_xray_dir}")
        print("Please ensure you are running this script from the 'codes' folder,")
        print("and the 'data/chest_xray' folder is inside 'codes/data'.")
    else:
        print(f"Starting reorganization in: {base_chest_xray_dir}")
        reorganize_chest_xray_data(base_chest_xray_dir)