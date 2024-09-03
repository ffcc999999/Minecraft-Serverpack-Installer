import os
import pathlib
import shutil
import json

def get_forge_or_fabric_version_from_manifest(path):
    with open(path, encoding="UTF-8") as f:
        data = json.load(f)

        # Если используется новая структура
        if "modloader" in data and "modloaderVersion" in data:
            modloader = data["modloader"].lower()
            minecraft_version = data["minecraftVersion"]
            modloader_version = data["modloaderVersion"]

            if "fabric" in modloader:
                return "fabric", minecraft_version

            if "forge" in modloader:
                return "forge", minecraft_version + "-" + modloader_version

        # Если используется старая структура
        elif "minecraft" in data and "modLoaders" in data["minecraft"]:
            modloaders = data["minecraft"]["modLoaders"]
            minecraft_version = data["minecraft"]["version"]

            for modloader in modloaders:
                if modloader["primary"] == True:
                    if "fabric" in modloader["id"].lower():
                        return "fabric", minecraft_version

                    if "forge" in modloader["id"].lower():
                        return "forge", minecraft_version + "-" + modloader["id"][6:]

        # Если структура не распознана
        print("Ошибка: Структура манифеста не поддерживается.")
        return None, None

# Пример использования:
# print(get_forge_or_fabric_version_from_manifest("manifest-fabric.json"))
