import questionary
import json
from pathlib import Path
import logging
from config.settings import MACRO_AREAS, MICRO_AREAS, PROJECT_FOLDER
from utils.file_utils import create_file_from_template, load_template
from utils.validation_utils import validate_project_name

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ask_macro_area():
    """Pergunta ao usuário para selecionar a macro-área."""
    return questionary.select("Selecione a macro-área:", choices=MACRO_AREAS).ask()


def ask_micro_area(macro_area):
    """Pergunta ao usuário para selecionar a micro-área com base na macro-área escolhida."""
    return questionary.select(
        "Selecione a micro-área:", choices=MICRO_AREAS[macro_area]
    ).ask()


def ask_project_name():
    """Pergunta ao usuário o nome do projeto."""
    project_name = questionary.text("Qual o nome do projeto?").ask()
    return validate_project_name(project_name)


def ask_yes_no_question(question):
    """Pergunta genérica de Sim/Não."""
    return questionary.confirm(question).ask()


from pathlib import Path


def create_project_folder(macro_area, micro_area, project_name):
    """Cria as pastas para o projeto, se elas não existirem."""
    workflows_path = (
        Path(PROJECT_FOLDER)
        / macro_area
        / micro_area
        / project_name
        / "workflows"
        / "etl_tools"
    )

    routes_path = (
        Path(PROJECT_FOLDER) / macro_area / micro_area / project_name / "routes"
    )

    # Verifica se as pastas já existem
    if workflows_path.exists() or routes_path.exists():
        raise FileExistsError(
            f"O projeto '{project_name}' já existe em '{macro_area}/{micro_area}'."
        )

    # Cria as pastas
    workflows_path.mkdir(parents=True, exist_ok=True)
    routes_path.mkdir(parents=True, exist_ok=True)

    return workflows_path, routes_path


def create_workflow_files(workflows_path, has_extractor, has_transform, has_loader):
    """Cria os arquivos de workflow com base nas respostas."""
    if has_extractor:
        template = load_template("extractor.py.template")
        create_file_from_template(workflows_path / "extractor.py", template)

    if has_transform:
        template = load_template("transform.py.template")
        create_file_from_template(workflows_path / "transform.py", template)

    if has_loader:
        template = load_template("loader.py.template")
        create_file_from_template(workflows_path / "loader.py", template)


def create_routes_file(routes_path, project_name):
    """Cria o arquivo de rotas com base no nome do projeto."""
    routes_file_name = f"{project_name}_routes.py"
    routes_file_path = routes_path / routes_file_name

    template = load_template("routes.py.template")
    routes_content = template.format(project_name=project_name)

    create_file_from_template(routes_file_path, routes_content)


def format_class_name(project_name):
    """Formata o nome do projeto para o padrão de nome de classe."""
    words = project_name.replace("_", " ").split()
    return "".join(word.capitalize() for word in words)


def create_etl_file(workflows_path, project_name, macro_area, micro_area):
    """Cria o arquivo etl.py com a classe <ProjectName>ETL."""
    etl_file_path = workflows_path.parent / "etl.py"

    class_name = format_class_name(project_name)
    template = load_template("etl.py.template")
    etl_content = template.format(
        macro_area=macro_area,
        micro_area=micro_area,
        project_name=project_name,
        class_name=class_name,
    )

    create_file_from_template(etl_file_path, etl_content)


def main():
    try:
        macro_area = ask_macro_area()
        micro_area = ask_micro_area(macro_area)
        project_name = ask_project_name()
        has_extractor = ask_yes_no_question("O projeto terá extractor?")
        has_transform = ask_yes_no_question("O projeto terá transform?")
        has_loader = ask_yes_no_question("O projeto terá loader?")

        workflows_path, routes_path = create_project_folder(
            macro_area, micro_area, project_name
        )

        create_workflow_files(workflows_path, has_extractor, has_transform, has_loader)
        create_routes_file(routes_path, project_name)
        create_etl_file(workflows_path, project_name, macro_area, micro_area)

        project_config = {
            "macro_area": macro_area,
            "micro_area": micro_area,
            "project_name": project_name,
            "has_extractor": has_extractor,
            "has_transform": has_transform,
            "has_loader": has_loader,
        }

        logger.info("\n--- Resumo do Projeto ---")
        logger.info(f"Macro-área: {macro_area}")
        logger.info(f"Micro-área: {micro_area}")
        logger.info(f"Nome do projeto: {project_name}")
        logger.info(f"Extractor: {'Sim' if has_extractor else 'Não'}")
        logger.info(f"Transform: {'Sim' if has_transform else 'Não'}")
        logger.info(f"Loader: {'Sim' if has_loader else 'Não'}")
        logger.info(f"Projeto criado em: {workflows_path.parent}")

    except Exception as e:
        logger.error(f"Erro ao criar o projeto: {e}")


if __name__ == "__main__":
    main()
