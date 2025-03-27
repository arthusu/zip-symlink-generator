import os
import argparse
import zipfile

def create_symlink(source_path, link_name):
    try:
        os.symlink(source_path, link_name)
    except FileExistsError:
        pass  # El enlace ya existe

def create_zip_with_symlink(link_name, output_dir):
    zip_path = os.path.join(output_dir, f"{link_name}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(link_name, arcname=link_name)
    print(f"[+] Created: {zip_path}")

def cleanup_symlinks():
    for entry in os.listdir('.'):
        if os.path.islink(entry) and entry.startswith("link"):
            os.unlink(entry)

def main():
    parser = argparse.ArgumentParser(description="Generador de ZIPs con symlinks")
    parser.add_argument("-f", "--file", required=True, help="Archivo con lista de rutas (una por línea)")
    args = parser.parse_args()

    if not os.path.exists("output"):
        os.makedirs("output")

    with open(args.file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    for idx, path in enumerate(lines):
        link_name = f"link{idx}"
        create_symlink(path, link_name)
        create_zip_with_symlink(link_name, "output")

    cleanup_symlinks()
    print("[✓] ZIPs generados y enlaces limpiados.")

if __name__ == "__main__":
    main()
