import pyvan

OPTIONS = {
  "main_file_name": "UI_main.py",
  "show_console": False,
  "use_existing_requirements": True,
  "extra_pip_install_args": ["--ignore-requires-python"],
  "python_version": "3.12.1",
  "use_pipreqs": False,
  "install_only_these_modules": [],
  "exclude_modules": [],
  "include_modules": [],
  "path_to_get_pip_and_python_embedded_zip": "",
  "build_dir": "InvSoft alpha build 0.7",
  "pydist_sub_dir": "dist",
  "source_sub_dir": "",
  "icon_file": None,
}

pyvan.build(**OPTIONS)