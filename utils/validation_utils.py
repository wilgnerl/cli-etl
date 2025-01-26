import re


def validate_project_name(project_name):
    """Valida o nome do projeto."""
    if not re.match(r"^[a-zA-Z0-9_]+$", project_name):
        raise ValueError(
            "O nome do projeto deve conter apenas letras, números e underscores."
        )
    return project_name
