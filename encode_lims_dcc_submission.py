# Script to submit excel objects

import csv
import json
import requests
import argparse

cell_line_map = dict({
    "A549": "EFO:0001086",
    "GM12878": "EFO:0002784",
    "HeLa-S3": "EFO:0002791",
    "IMR90": "EFO:0001196",
    "K562": "EFO:0002067",
    "MCF-7": "EFO:0001203",
    "SK-N-SH": "EFO:0003072",
    "HepG2": "EFO:0001187",
    "H1 Neurons": "CL:0002319"
    })

biosample_type_map = dict({
    "A549": "immortalized cell line",
    "GM12878": "immortalized cell line",
    "HeLa-S3": "immortalized cell line",
    "IMR90": "immortalized cell line",
    "K562": "immortalized cell line",
    "MCF-7": "immortalized cell line",
    "SK-N-SH": "immortalized cell line",
    "HepG2": "immortalized cell line",
    "H1 Neurons": "primary cell line"
    })

platform_map = dict({
    "HiSeq 2000": "03a96eaf-75da-44e2-b4f6-e349e8c3655e",
    "GAIIx": "7efe9ddc-bbe6-457d-bc98-f8bac2478bda"
    })


def read_truptis_file(infile):
    value_list = open(infile, "rU")
    record_values = csv.DictReader(value_list, delimiter='\t')
    dict_output = open(args.outfile, "w")

    list_output = []
    experiment_check = {}
    for record in record_values:

        # Register experiments
        experiments_dict = {}
        experiment_alias = 'michael-snyder:' + str(record.get('Cell_line')) + '-' + str(record.get('Factor'))
        if experiment_alias not in experiment_check.keys():
            experiments_dict['@id'] = 'experiment/'
            experiments_dict['biosample_term_id'] = cell_line_map[record.get('Cell_line')]
            experiments_dict['biosample_term_name'] = record.get('Cell_line')
            experiments_dict['biosample_type'] = biosample_type_map[record.get('Cell_line')]
            experiments_dict['assay_term_id'] = "OBI:0000716"
            experiments_dict['assay_term_name'] = "ChIP-seq"
            experiments_dict['lab'] = "michael-snyder"
            experiments_dict['award'] = "U54HG006996"
            experiments_dict['target'] = record.get('Targets')
            experiments_dict['aliases'] = [experiment_alias]
            experiments_dict['description'] = ""
            experiments_dict['documents'] = 'michael-snyder:' + str(record.get('Protocol_documents'))

            experiment_check[experiment_alias] = experiments_dict
            list_output.append(experiments_dict)

        # Register Library
        library_dict = {}
        library_dict['@id'] = 'library/'
        library_dict['biosample'] = record.get('ENCBS_no. ')
        library_dict['nucleic_acid_term_name'] = 'DNA'
        library_dict['nucleic_acid_term_id'] = 'SO:0000352'
        #library_dict['documents'] = need your protocol document
        #library_dict['nucleic_acid_starting_quantity'] = 'Unknown' - Where to get this information
        #library_dict['fragmentation_date'] = Might not need
        library_dict['size_range'] = record.get('Size range').strip(' bp')
        library_dict['paired_ended'] = True
        library_dict['aliases'] = ['michael-snyder:' + str(record.get('TruSeq_library_name')) + '_' + str(record.get('Truseq_Barcode'))]
        library_dict['lab'] = "michael-snyder"
        library_dict['award'] = "U54HG006996"
        list_output.append(library_dict)

        # Register replicates
        replicates_dict = {}
        replicates_dict['@id'] = 'replicate/'
        replicates_dict['antibody'] = record.get('ENCAB_no. ')
        replicates_dict['biological_replicate_number'] = int(record.get('Replicate')[-1:])
        replicates_dict['technical_replicate_number'] = 1
        replicates_dict['experiment'] = experiment_alias
        replicates_dict['library'] = library_dict['aliases'][0]
        replicates_dict['platform'] = platform_map["HiSeq 2000"]

        # Parse Flowcell information
        flowcell = {}
        Flow_cell = record.get('Flow_Cell')
        flowcell['lane'] = record.get('Lane')
        flowcell['barcode'] = record.get('Truseq_Barcode')
        flowcell['machine'] = Flow_cell.split('_', 3)[1]
        flowcell['flowcell'] = Flow_cell.split('_', 3)[3]

        replicates_dict['flowcell_details'] = [flowcell]
        replicates_dict['paired_ended'] = True
        replicates_dict['read_length'] = 100
        replicates_dict['read_length_units'] = 'nt'
        list_output.append(replicates_dict)

    json.dump(list_output, dict_output, indent=4)

    dict_output.close()


def read_objects(object_file):
    json_file = open(object_file)
    json_objects = json.load(json_file)
    json_file.close()
    return json_objects


def filter_object(json_object, key):
    json_duplicate = json_object
    json_duplicate.pop(key)
    return json.dumps(json_duplicate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', '-i', help="A tab delimited file that needs processing")
    parser.add_argument('--outfile', '-o', help="An output file containing JSON objects to post")
    args = parser.parse_args()

    read_truptis_file(args.infile)

    '''
    #Commented out for now to make sure JSON objects are properly created before submitting

    # set headers.  UNCLEAR IF THIS IS USED PROPERLY
    HEADERS = {'content-type': 'application/json'}

    settings = dict()
    settings['USER'] = "dsalins@stanford.edu"
    settings['SERVER'] = "http://test.encodedcc.org"
    settings['AUTHID'] = "Y5PLREWZ"
    settings['AUTHPW'] = "nnug55q6mnlsgwze"

    post_objects = read_objects("truptis_output_file.json")

    for i in range(0, len(post_objects)):
        object_id = post_objects[i]['@id']
        post_object = filter_object(post_objects[i], '@id')
        url = (settings.get('SERVER') + '/' + str(object_id))
        authid = settings.get('AUTHID')
        authpw = settings.get('AUTHPW')
        response = requests.post(url, auth=(authid, authpw), headers=HEADERS, data=post_object)
        print response.text
    '''