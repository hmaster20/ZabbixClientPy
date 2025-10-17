import uuid  
import sys  
from ruamel.yaml import YAML  
  
def replace_uuids_in_yaml(file_path, output_path):  
    yaml = YAML()  
    yaml.preserve_quotes = True  
  
    with open(file_path, 'r', encoding='utf-8') as f:  
        data = yaml.load(f)  
  
    uuid_map = {}  
    generated_uuids = set()  
  
    def generate_unique_uuid():  
        new_uuid = str(uuid.uuid4())  
        while new_uuid in generated_uuids:  
            new_uuid = str(uuid.uuid4())  
        generated_uuids.add(new_uuid)  
        return new_uuid  
  
    def traverse(obj):  
        if isinstance(obj, dict):  
            for k, v in obj.items():  
                if k.lower() == "uuid":  # ключ называется uuid  
                    if v not in uuid_map:  
                        uuid_map[v] = generate_unique_uuid()  
                    obj[k] = uuid_map[v]  
                else:  
                    traverse(v)  
        elif isinstance(obj, list):  
            for i, v in enumerate(obj):  
                traverse(v)  
  
    traverse(data)  
  
    # Проверка уникальности  
    if len(set(uuid_map.values())) != len(uuid_map.values()):  
        raise ValueError("Обнаружены дубликаты UUID — что-то пошло не так!")  
  
    with open(output_path, 'w', encoding='utf-8') as f:  
        yaml.dump(data, f)  
  
    print(f"Заменено {len(uuid_map)} UUID. Файл сохранён в {output_path}")  
  
if __name__ == "__main__":  
    if len(sys.argv) != 3:  
        print(f"Использование: {sys.argv[0]} input.yaml output.yaml")  
        sys.exit(1)  
    replace_uuids_in_yaml(sys.argv[1], sys.argv[2])  