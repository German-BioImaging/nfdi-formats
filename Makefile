docs/formats.ttl: context.json to_rdf.py $(wildcard $(DIR)/formats/*.yaml)
	pipx run to_rdf.py
