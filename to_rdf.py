# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rdflib",
#     "pyld == 2.0.4",
#     "yaml-ld == 1.1.18",
# ]
# ///
import rdflib
import yaml_ld

n_quads_formats = yaml_ld.to_rdf("formats.yaml", {"format": "application/n-quads"})
n_quads_nfdi = yaml_ld.to_rdf("nfdi.yaml", {"format": "application/n-quads"})

g = rdflib.ConjunctiveGraph()
g.parse(data=n_quads_formats, format="nquads")

g.parse(data=n_quads_nfdi, format="nquads")

# save as Turtle
g.serialize(destination="rdf/nfdi_formats.ttl", format="turtle")
