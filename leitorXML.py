# -*- coding: utf-8 -*-
import xmlschema
from pprint import pprint


def LerXML(arq):
    xs = xmlschema.XMLSchema('instancia.xsd')
    print xs.is_valid('i0.xml')
    pprint(xs.to_dict('i0.xml'))
    my_dict = xs.to_dict('i0.xml')
    return my_dict

