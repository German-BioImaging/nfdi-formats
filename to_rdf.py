# /// script
# requires-python = ">=3.12"
# dependencies = [ "rdflib", "pyyaml" ]
# ///
from rdflib import Graph, URIRef
import json
import yaml
import glob

# Aggregate formats metadata
formats = {}
for file in glob.glob("formats/*.yaml"):
    id = file.split("/")[1][0:-5]
    data = yaml.safe_load(open(file, "r"))
    data["handle"] = id
    formats[id] = data

# Check formats metadata
for f in formats:
    # base formats must exist and not be itself
    if "base" in formats[f]:
        base = formats[f]["base"]
        if base is f or base not in formats:
            raise ValueError(f"base '{base}' of {f} not found!")

# Convert to RDF
data = yaml.safe_load(open("nfdi.yaml", "r"))

data["handle"] = ""
data["file_formats"] = [formats[id] for id in formats.keys()],
data["@context"] = json.load(open("context.json", "r"))

g = Graph()
g.parse(data=json.dumps(data), format="json-ld")

# save as Turtle
g.bind("", None, replace=True)
g.bind("schema", URIRef("https://schema.org/"))
g.bind("wd", URIRef("http://www.wikidata.org/entity/"))
g.serialize(destination="rdf/nfdi_formats.ttl", format="turtle")
