#!/usr/bin/env python3  
import uuid  
import argparse  
import logging  
from ruamel.yaml import YAML  
  
def replace_uuids_in_yaml(input_file, output_file=None, dry_run=False):  
    yaml = YAML()  
    yaml.preserve_quotes = True  
  
    with open(input_file, 'r', encoding='utf-8') as f:  
        data = yaml.load(f)  
  
    uuid_map = {}  
    generated_uuids = set()  
  
    def generate_unique_uuid():  
        """Генерация UUIDv4 без дефисов для Zabbix"""  
        new_uuid = uuid.uuid4().hex.lower()  # hex гарантирует без дефисов  
        while new_uuid in generated_uuids:  
            new_uuid = uuid.uuid4().hex.lower()  
        generated_uuids.add(new_uuid)  
        return new_uuid  
  
    def traverse(obj):  
        if isinstance(obj, dict):  
            for k, v in obj.items():  
                if k.lower() == "uuid":  
                    if v not in uuid_map:  
                        new_uuid = generate_unique_uuid()  
                        uuid_map[v] = new_uuid  
                        logging.info(f"Замена: {v} -> {new_uuid}")  
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
  
    logging.info(f"Всего найдено и заменено UUID: {len(uuid_map)}")  
  
    if dry_run:  
        logging.info("Dry-run режим: файл не будет изменён.")  
    else:  
        if not output_file:  
            raise ValueError("Не указан выходной файл для сохранения результата.")  
        with open(output_file, 'w', encoding='utf-8') as f:  
            yaml.dump(data, f)  
        logging.info(f"Файл сохранён в {output_file}")  
  
def main():  
    parser = argparse.ArgumentParser(description="Замена UUID в YAML-файле Zabbix на уникальные UUIDv4 без дефисов")  
    parser.add_argument("-i", "--input", required=True, help="Путь к входному YAML-файлу")  
    parser.add_argument("-o", "--output", help="Путь к выходному YAML-файлу (не нужен в dry-run)")  
    parser.add_argument("--dry-run", action="store_true", help="Режим теста без сохранения изменений")  
    parser.add_argument("-v", "--verbose", action="store_true", help="Включить подробный вывод логов")  
  
    args = parser.parse_args()  
  
    logging.basicConfig(  
        level=logging.INFO if args.verbose else logging.WARNING,  
        format="%(levelname)s: %(message)s"  
    )  
  
    replace_uuids_in_yaml(args.input, args.output, args.dry_run)  
  
if __name__ == "__main__":  
    main()  