import os
import shutil
import json
import re
import random


def split_img_notes():
    src_dir = "data/imgs&anotacoes"

    for filename in os.listdir(src_dir):
        if filename.endswith(".png"):
            img_path = os.path.join(src_dir, filename)
            note_path = os.path.join(src_dir, filename.replace(".png", ".json"))

            if os.path.exists(note_path):
                shutil.move(img_path, "data/imgs")
                shutil.move(note_path, "data/anotacoes")

    print("Imagens e anotações foram movidas para os diretórios correspondentes.")

    return


def json_to_txt():
    labels_dir = "data/anotacoes"
    output_dir = "data/labels"

    for filename in os.listdir(labels_dir):
        if filename.endswith(".json"):
            json_path = os.path.join(labels_dir, filename)
            txt_path = os.path.join(output_dir, filename.replace(".json", ".txt"))

            try:
                with open(json_path, "r") as json_file:
                    data = json.load(json_file)

            except json.JSONDecodeError:
                print(f"Erro ao decodificar o arquivo JSON: {json_path}")
                break

            with open(txt_path, "w") as txt_file:
                for item in data["shapes"]:
                    category_id = 0  # Só há uma categoria, então o ID é 0
                    bbox = item["points"]
                    txt_file.write(
                        f"{category_id} {bbox[0][0]} {bbox[0][1]} {bbox[1][0]} {bbox[1][1]}\n"
                    )

    return


def fix_json_files():
    def remove_imageData(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # remove o campo "imageData": "...."
        content = re.sub(r'"imageData"\s*:\s*".*?",?', "", content, flags=re.DOTALL)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def fix_truncated_json(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        if '"imageData"' in content:
            # corta antes do imageData
            content = content.split('"imageData"')[0]

            # remove vírgula final se tiver
            content = content.rstrip().rstrip(",")

            # fecha o JSON corretamente
            content += "\n}"

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    path = "data/anotacoes"

    for filename in os.listdir(path):
        if filename.endswith(".json"):
            remove_imageData(os.path.join(path, filename))
            fix_truncated_json(os.path.join(path, filename))


def verify_equivalence():
    img_files = set(os.listdir("data/imgs"))
    label_files = set(os.listdir("data/labels"))

    img_basenames = {os.path.splitext(f)[0] for f in img_files}
    label_basenames = {os.path.splitext(f)[0] for f in label_files}

    if img_basenames == label_basenames:
        print("Todos os arquivos de imagem têm um arquivo de rótulo correspondente.")
    else:
        missing_labels = img_basenames - label_basenames
        missing_images = label_basenames - img_basenames

        if missing_labels:
            print(
                "Imagens sem rótulos correspondentes:",
                os.path.join("data/imgs", f"{missing_labels.pop()}.png"),
            )
        if missing_images:
            print(
                "Rótulos sem imagens correspondentes:",
                os.path.join("data/labels", f"{missing_images.pop()}.txt"),
            )


def split_train_val(train_ratio=0.7, val_ratio=0.2, test_ratio=0.1, random_seed=42):
    img_dir = "data/images"
    files = os.listdir(img_dir)

    random.seed(random_seed)
    random.shuffle(files)

    total_files = len(files)
    train_end = int(total_files * train_ratio)
    val_end = train_end + int(total_files * val_ratio)

    train_files = files[:train_end]
    val_files = files[train_end:val_end]
    test_files = files[val_end:]

    os.makedirs("data/train", exist_ok=True)
    os.makedirs("data/train/images", exist_ok=True)
    os.makedirs("data/train/labels", exist_ok=True)

    os.makedirs("data/val", exist_ok=True)
    os.makedirs("data/val/images", exist_ok=True)
    os.makedirs("data/val/labels", exist_ok=True)

    os.makedirs("data/test", exist_ok=True)
    os.makedirs("data/test/images", exist_ok=True)
    os.makedirs("data/test/labels", exist_ok=True)

    for f in train_files:
        shutil.copy(os.path.join(img_dir, f), os.path.join("data/train/images", f))
        shutil.copy(
            os.path.join("data/labels", f.replace(".png", ".txt")),
            os.path.join("data/train/labels", f.replace(".png", ".txt")),
        )

    for f in val_files:
        shutil.copy(os.path.join(img_dir, f), os.path.join("data/val/images", f))
        shutil.copy(
            os.path.join("data/labels", f.replace(".png", ".txt")),
            os.path.join("data/val/labels", f.replace(".png", ".txt")),
        )

    for f in test_files:
        shutil.copy(os.path.join(img_dir, f), os.path.join("data/test/images", f))
        shutil.copy(
            os.path.join("data/labels", f.replace(".png", ".txt")),
            os.path.join("data/test/labels", f.replace(".png", ".txt")),
        )

    return {
        "total": total_files,
        "train": len(train_files),
        "val": len(val_files),
        "test": len(test_files),
    }


def main():
    # split_img_notes()
    # fix_json_files()
    # json_to_txt()

    # verify_equivalence()

    return


if __name__ == "__main__":
    main()
