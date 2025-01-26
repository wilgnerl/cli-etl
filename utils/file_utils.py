from pathlib import Path


def create_file_from_template(file_path, template_content):
    """Cria um arquivo a partir de um template."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(template_content.strip())


def load_template(template_name):
    """Carrega um template de um arquivo."""
    template_path = Path("config/templates") / template_name
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as file:
            return file.read()
    raise FileNotFoundError(f"Template '{template_name}' não encontrado.")
