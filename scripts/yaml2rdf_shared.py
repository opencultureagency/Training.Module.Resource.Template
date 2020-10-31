'''
Common functionality for ASKotec training meta-data conversion
from YAML into an RDF/Turtle.
'''

import re
import os
from packaging import version
import yaml
import rdflib
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD

SCHEMA  = rdflib.Namespace('http://schema.org/')
ASK  = rdflib.Namespace('http://myontology.com/')
ASKA = rdflib.Namespace('http://myontology.com/authors/')
ASKM = rdflib.Namespace('http://myontology.com/modules/')
ASKR = rdflib.Namespace('http://myontology.com/resources/')
ASKC = rdflib.Namespace('http://myontology.com/materials/')
ASKT = rdflib.Namespace('http://myontology.com/tools/')

def version_compare(ver1, ver2):
    '''
    Compares two version strings.
    '''
    return version.parse(ver1) < version.parse(ver2)

def conv_license(yaml_cont, g):

    subj  = ASK[str2id(yaml_cont['name'])]
    g.add(( subj, RDF.type, ASK.License ))
    g.add(( subj, RDFS.label, rdf_str(yaml_cont['name']) ))
    g.add(( subj, SCHEMA.file, rdf_str(yaml_cont['file']) ))
    return subj

def rdf_str(s):
    '''
    Converts a simple string into an RDF string (xsd:string).
    '''
    return rdflib.Literal(s, datatype=XSD.string)

def rdf_int(s):
    '''
    Converts a simple string into an RDF int (xsd:int).
    '''
    return rdflib.Literal(s, datatype=XSD.int)

def str2id(s):
    '''
    Converts a random string into a valid RDF id (the last part of an IRI).
    '''
    return re.sub('[^a-zA-Z0-9_-]+', '_', s)

def conv_fail(msg):
    raise RuntimeError(msg)

def conv_licenses(yaml_cont, g, parent_subj):

    if 'licenses' in yaml_cont:
        for yaml_cont_part in yaml_cont['licenses']:
            g.add(( parent_subj, ASK.license, conv_license(yaml_cont_part, g) ))

def conv_author(yaml_cont, g):

	subj  = ASKA[str2id(yaml_cont['name'])]
	g.add(( subj, RDF.type, ASK.Author ))
	g.add(( subj, RDFS.label, rdf_str(yaml_cont['name']) ))
	g.add(( subj, SCHEMA.mbox, rdf_str(yaml_cont['mail']) ))
	g.add(( subj, SCHEMA.github, rdf_str(yaml_cont['github-profile']) ))
	if 'telegram' in yaml_cont:
	    g.add(( subj, SCHEMA.telegram, rdf_str(yaml_cont['telegram']) ))
	return subj

def conv_authors(yaml_cont, g, parent_subj):

    if 'authors' in yaml_cont:
        for yaml_cont_part in yaml_cont['authors']:
            g.add(( parent_subj, ASK.author, conv_author(yaml_cont_part, g) ))

