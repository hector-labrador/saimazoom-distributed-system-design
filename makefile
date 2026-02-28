PYTHON = python3
PROJECT_ROOT := $(shell pwd)

.PHONY: run_controller run_client run_robot run_repartidor test clean help

help:
	@echo "Make targets disponibles:"
	@echo "  run_controller    - Ejecuta launch_controller.py"
	@echo "  run_client        - Ejecuta launch_client.py"
	@echo "  run_robot         - Ejecuta launch_robot.py"
	@echo "  run_repartidor    - Ejecuta launch_delivery.py"
	@echo "  test              - Ejecuta tests unitarios"
	@echo "  clean             - Limpia archivos de base de datos o temporales"

run_controller:
	$(PYTHON) src/launch_controller.py

run_client:
	$(PYTHON) src/launch_client.py

run_robot:
	$(PYTHON) src/launch_robot.py

run_repartidor:
	$(PYTHON) src/launch_delivery.py

test:
	PYTHONPATH=$(PROJECT_ROOT)/src python3 -m unittest discover -s tests

test_integration:
	PYTHONPATH=$(PROJECT_ROOT)/src python3 -m unittest tests/test_integration.py

clean:
	rm -f data/*.db data/*.json
	@echo "Archivos de la carpeta data/ limpiados (DB, JSON)"
