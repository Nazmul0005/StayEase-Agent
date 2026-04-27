import os

structure = {
    "StayEase-Agent": [
        "requirements.txt",
        "Dockerfile",
        "compose.yaml",
        ".env",
        "README.md",
        "api.md",

        {"com": [
            {"app": [
                "main.py",

                {"config": [
                    "config.py"
                ]},

                {"database": [
                    {"db_connection": [
                        "db_connection.py"
                    ]},
                    {"models": [
                        "models.py"
                    ]}
                ]},

                {"agent": [
                    "state.py",
                    "nodes.py",
                    "tools.py",
                    "graph.py"
                ]},

                {"services": [
                    {"chat": [
                        "chat.py",
                        "chat_router.py",
                        "chat_schema.py"
                    ]},
                    {"listings": [
                        "listings.py",
                        "listings_router.py",
                        "listings_schema.py"
                    ]}
                ]},

                {"utils": [
                    "__init__.py"
                ]}
            ]}
        ]}
    ]
}


def create_structure(base_path, items):
    """Recursively create folders and files."""
    for item in items:
        if isinstance(item, str):
            file_path = os.path.join(base_path, item)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if not os.path.exists(file_path):
                open(file_path, "w").close()
                print(f"Created file: {file_path}")
            else:
                print(f"File exists: {file_path}")

        elif isinstance(item, dict):
            for folder, subitems in item.items():
                folder_path = os.path.join(base_path, folder)
                os.makedirs(folder_path, exist_ok=True)
                print(f"Created folder: {folder_path}")
                create_structure(folder_path, subitems)


def main():
    for root, items in structure.items():
        os.makedirs(root, exist_ok=True)
        print(f"Created root folder: {root}")
        create_structure(root, items)


if __name__ == "__main__":
    main()