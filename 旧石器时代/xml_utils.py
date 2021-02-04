import tempfile
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element


class XMLUtil:

    @classmethod
    def str2xml_tree(cls, xml_str):
        tf = tempfile.NamedTemporaryFile()
        tf.write(xml_str.encode())
        tf.seek(0)
        xml_tree = ElementTree()
        xml_tree.parse(tf)
        return xml_tree

    @classmethod
    def get_node_by_path(cls, xml_tree_obj, path):
        return xml_tree_obj.find(path)

    @classmethod
    def xml_tree2str(cls, xml_tree):
        tf = tempfile.NamedTemporaryFile()
        xml_tree.write(tf)
        tf.seek(0)
        return tf.read().decode()
