from lxml import etree

def validate(document, interface=False):
    if interface:
        schema = 'Syntax/pipeline.rng'
    else:
        schema = 'Syntax/interface.rng'
    schema_tree = etree.parse(schema)
    relaxng = etree.RelaxNG(schema_tree)
    doc_tree = etree.parse(document)
    if not relaxng.validate(doc_tree):
        print(relaxng.error_log)
        return False
    return True


def main():
    #document = '../Test/diff_expr/pipeline.xml'
    document = '/home/fedor/DSL/BioinformaticsDSL/Utils/genome/fastq-dump.xml'

    validate(document)


if __name__ == '__main__':
    main()