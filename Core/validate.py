from lxml import etree

def validate(document, schema):
    schema_tree = etree.parse(schema)
    relaxng = etree.RelaxNG(schema_tree)
    doc_tree = etree.parse(document)
    if not relaxng.validate(doc_tree):
        print(relaxng.error_log)


def main():
    #document = '../Test/diff_expr/pipeline.xml'
    document = '/home/fedor/DSL/BioinformaticsDSL/Utils/genome/fastq-dump.xml'
    schema = 'Syntax/pipeline.rng'

    validate(document, schema)


if __name__ == '__main__':
    main()