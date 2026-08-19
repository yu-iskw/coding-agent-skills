.PHONY: lint
lint:
	trunk check -a -y

.PHONY: format
format:
	trunk fmt -a

.PHONY: validate
validate:
	bash ./scripts/validate_agent_skills.sh

.PHONY: contracts
contracts:
	python3 ./scripts/validate_skill_contracts.py

.PHONY: security
security:
	python3 ./scripts/security_scan.py

.PHONY: security-report
security-report:
	python3 ./scripts/security_scan.py --output ./catalog/security-report.json

.PHONY: catalog
catalog:
	python3 ./scripts/generate_catalog.py

.PHONY: generated-check
generated-check:
	python3 ./scripts/generate_catalog.py --check

.PHONY: check
check: validate contracts security generated-check
