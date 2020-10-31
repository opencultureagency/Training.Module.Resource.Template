'''
Converts ASKotec training module meta-data
(from module.yaml) into an RDF/Turtle.
'''

import re
import os
import yaml
import rdflib
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
from yaml2rdf_shared import *

def convert_module_yaml_to_rdf(yaml_cont, g):
    '''
    Converts ASKotec training module meta-data content
    into an RDF/Turtle string.
    '''

    supported_version = "1.0"
    if version_compare(yaml['version'], supported_version) < 0:
        raise 'The content version is not supported by this converter. Please get a newer version!'

    y = yaml_cont['training-module']
    m_s = ASKM[str2id(y['name'])]

    g.add(( m_s, RDF.type, ASK.Module ))
    g.add(( m_s, RDFS.label, rdf_str(y['name']) ))
    if 'manual' in y:
        g.add(( m_s, ASK.manual, rdf_str(y['manual']) ))
    elif os.path.exists('manual.md'):
        g.add(( m_s, ASK.manual, rdf_str('manual.md') ))
    else:
        conv_fail('Entry not found "%s", and default path "%s" does not exist'
                % (pre_path + '.' + 'manual', os.path.curdir + '/manual.md'))
    g.add(( m_s, ASK.release, rdf_str(y['release']) ))
    g.add(( m_s, ASK.duration, rdf_str(y['duration']) ))
    g.add(( m_s, ASK.maxParticipians, rdf_str(y['max-participians']) ))
    g.add(( m_s, ASK.compatibility, rdf_str(y['compatibility']) ))
    g.add(( m_s, ASK.blogPosts, rdf_str(y['blog-posts']) ))
    g.add(( m_s, ASK.issues, rdf_str(y['issues']) ))
    g.add(( m_s, ASK.newIssue, rdf_str(y['new-issue']) ))

    for elem in y['resources']:
        g.add(( m_s, ASKM.resource, rdf_str(elem['url']) ))

    conv_authors(y, g, m_s)
    conv_licenses(y, g, m_s)

