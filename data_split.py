import shutil
import random
from pathlib import Path


# PATH TO YOUR IXI-T2 FOLDER (original data - will remain untouched)

input_root = Path("/media/server/Data/abdul/Passport")


split_root = Path("./IXI_split") # Subfolders will be: train/, val/, test/


# OUTPUT DIRECTORY FOR TEXT FILES (train.txt, val.txt, test.txt)

text_dir = Path("./splits")

# Create directories
for split in ["train", "val", "test"]:
    (split_root / split).mkdir(parents=True, exist_ok=True)
text_dir.mkdir(parents=True, exist_ok=True)


# GET ALL MRI FILES (NIfTI only)

all_files = [p.name for p in input_root.glob("*.nii*") if p.is_file()]

if len(all_files) == 0:
    raise ValueError(f"No NIfTI files found in {input_root}!")

# Sort for deterministic order before shuffling
all_files.sort()

print(f"Found {len(all_files)} NIfTI files in {input_root}")



random.seed(42)  # Remove or change this line if you want a different split each run
random.shuffle(all_files)


# SPLIT RATIOS (70% train, 20% test, 10% val)

train_ratio = 0.70
test_ratio = 0.20
val_ratio = 0.10

n = len(all_files)
n_train = int(n * train_ratio)
n_test = int(n * test_ratio)
n_val = n - n_train - n_test  # Ensures every file is used

train_files = all_files[:n_train]
test_files = all_files[n_train:n_train + n_test]
val_files = all_files[n_train + n_test:]


def copy_files(file_list, split_name):
    split_dir = split_root / split_name
    for f in file_list:
        src = input_root / f
        dst = split_dir / f
        shutil.copy2(src, dst)  

copy_files(train_files, "train")
copy_files(test_files, "test")
copy_files(val_files, "val")


# SAVE TEXT FILES (one filename per line)

def save_list(filepath: Path, file_list):
    filepath.write_text("\n".join(file_list) + "\n")

save_list(text_dir / "train.txt", train_files)
save_list(text_dir / "test.txt", test_files)
save_list(text_dir / "val.txt", val_files)


print("Dataset splitting completed !")


# print(f"Total files: {n}")
# print(f"Train ({train_ratio*100:.0f}%): {len(train_files)} copied to {split_root}/train/ and listed in {text_dir}/train.txt")
# print(f"Test  ({test_ratio*100:.0f}%): {len(test_files)} copied to {split_root}/test/ and listed in {text_dir}/test.txt")
# print(f"Val   ({val_ratio*100:.0f}%): {len(val_files)} copied to {split_root}/val/ and listed in {text_dir}/val.txt")