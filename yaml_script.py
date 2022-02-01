from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

yaml_file = open("gitlab/cypress_run.yml", 'r')
yaml_content = load(yaml_file, Loader=Loader)

print("Key: Value")
for key, value in yaml_content.items():
    print(f"{key}: {value}")