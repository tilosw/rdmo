import logging

from rdmo.core.imports import utf8_to_bool, get_value_from_xml_node
from rdmo.core.utils import get_ns_map, get_ns_tag


from .models import OptionSet, Option

log = logging.getLogger(__name__)


def import_options(optionsets_node):
    log.info('Importing options')

    nsmap = get_ns_map(optionsets_node.getroot())

    for optionset_node in optionsets_node.findall('optionset'):
        uri = optionset_node.find(get_ns_tag('dc:uri', nsmap)).text

        try:
            optionset = OptionSet.objects.get(uri=uri)
        except OptionSet.DoesNotExist:
            optionset = OptionSet()
            log.info('Optionset not in db. Created with uri ' + str(uri))
        else:
            log.info('Optionset does exist. Loaded from uri ' + str(uri))

        optionset.uri_prefix = uri.split('/options/')[0]
        optionset.key = uri.split('/')[-1]
        optionset.comment = get_value_from_xml_node(optionset_node, get_ns_tag('dc:comment', nsmap))
        optionset.order = get_value_from_xml_node(optionset_node, 'order')
        log.info('Optionset saving to "' + str(uri) + '"')
        optionset.save()

        for options_node in optionset_node.findall('options'):
            for option_node in options_node.findall('option'):
                uri = option_node.find(get_ns_tag('dc:uri', nsmap)).text

                try:
                    option = Option.objects.get(uri=uri)
                except Option.DoesNotExist:
                    log.info(Option.DoesNotExist)
                    option = Option()

                option.optionset = optionset
                option.uri_prefix = uri.split('/options/')[0]
                option.key = uri.split('/')[-1]
                option.comment = get_value_from_xml_node(option_node, get_ns_tag('dc:comment', nsmap))
                option.order = get_value_from_xml_node(option_node, 'order')
                for element in option_node.findall('text'):
                    setattr(option, 'text_' + element.get('lang'), element.text)
                option.additional_input = utf8_to_bool(get_value_from_xml_node(option_node, 'additional_input'))
                log.info('Option saving to "' + str(uri) + '"')
                option.save()
