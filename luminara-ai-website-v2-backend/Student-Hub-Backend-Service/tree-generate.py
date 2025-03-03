import os

def generate_puml(directory):
    puml = ["@startuml", "skinparam FolderBackgroundColor LightGray"]

    def walk_dir(dir_path, prefix=""):
        for item in sorted(os.listdir(dir_path)):
            full_path = os.path.join(dir_path, item)
            if os.path.isdir(full_path):
                puml.append(f'folder "{item}" {{')
                walk_dir(full_path, prefix + "  ")
                puml.append("}")
            else:
                puml.append(f'  file "{item}"')

    walk_dir(directory)
    puml.append("@enduml")

    return "\n".join(puml)

directory = "."  # Setze hier dein Verzeichnis
puml_code = generate_puml(directory)

with open("tree.puml", "w") as f:
    f.write(puml_code)

print("PlantUML-Datei gespeichert als tree.puml")

