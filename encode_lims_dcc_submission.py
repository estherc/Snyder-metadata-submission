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
    "neural cell": "CL:0002319"
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
    "neural cell": "primary cell line"
    })

platform_map = dict({
    "HiSeq 2000": "ENCODE:HiSeq2000",
    "GAIIx": "ENCODE:GAIIx"
    })

possible_control_map = dict({
    "GM12878" : ["michael-snyder:GM12878-Rabbit_IgG", "michael-snyder:GM12878-Input_GM12878"],
    "HeLa-S3" : ["michael-snyder:HeLa-S3-Rabbit_IgG", "michael-snyder:HeLa-S3-Input_HelaS3"],
    "HepG2" : ["michael-snyder:HepG2-Rabbit_IgG", "michael-snyder:HepG2-Input_HepG2"],
    "K562" : ["michael-snyder:K562-Rabbit_IgG", "michael-snyder:K562-Input_K562"],
    "MCF-7" : ["michael-snyder:MCF-7-Mouse_IgG" , "michael-snyder:MCF-7-Rabbit_IgG", "michael-snyder:MCF-7-Input_MCF7"],
    "neural cell" : ["michael-snyder:neural cell-Rabbit_IgG", "michael-snyder:neural cell-Input_H1 Neurons"]
    })

## This is reversed because the control that needs to be removed is the opposite when sending to the DCC
##    The possible_control_map should be the opposite 
reverse_remove_ab_host_control_map = dict({
    "R" : "Rabbit_IgG",
    "M" : "Mouse_IgG",
    "G" : "Goat_IgG",
    "" : "Control"
    })

def getUsername():
    login_file = "~/Documents/SVNRepositories/security/encode_dcc_login"
    login_values = open(login_file, "rU")
    record_values = csv.DictReader(value_list, delimiter='\t')
    encode_dcc_user = ''
    encode_dcc_username = ''
    encode_dcc_password = ''

def read_objects(object_file):
    json_file = open(object_file)
    json_objects = json.load(json_file)
    json_file.close()
    return json_objects


def filter_object(json_object, key):
    json_duplicate = json_object
    json_duplicate.pop(key)
    return json.dumps(json_duplicate)

def postObject(object):
    HEADERS = {'content-type': 'application/json'}

    settings = dict()
    settings['USER'] = encode_dcc_user
    settings['SERVER'] = "http://test.encodedcc.org"
    settings['AUTHID'] = encode_dcc_username
    settings['AUTHPW'] = encode_dcc_password

    object_id = object['@id']
    post_object = filter_object(object, '@id')
    url = (settings.get('SERVER') + '/' + str(object_id))
    authid = settings.get('AUTHID')
    authpw = settings.get('AUTHPW')
    response = requests.post(url, auth=(authid, authpw), headers=HEADERS, data=post_object)
    return response.json()

def getObject(object):
    HEADERS = {'content-type': 'application/json'}

    settings = dict()
    settings['USER'] = encode_dcc_user
    settings['SERVER'] = "http://test.encodedcc.org"
    settings['AUTHID'] = encode_dcc_username
    settings['AUTHPW'] = encode_dcc_password

    #object_id = object['@id']
    #post_object = filter_object(object, '@id')
    url = (settings.get('SERVER') + '/' + str(object))  #Object
    authid = settings.get('AUTHID')
    authpw = settings.get('AUTHPW')
    #response = requests.patch(url, auth=(authid, authpw), headers=HEADERS, data=object)  #object
    response = requests.get(url, auth=(authid, authpw), headers=HEADERS, data=object)  #object
    return response.json()

def read_truptis_file(infile):
    value_list = open(infile, "rU")
    record_values = csv.DictReader(value_list, delimiter='\t')
    dict_output = open(args.outfile, "w")
    encsr_number = ''
    enclb_number = ''

    list_output = []
    experiment_check = {}
    for record in record_values:
        if record.get('Cell_line') is not '':
        # Register experiments
            experiments_dict = {}
            print 'Processing ID: ' + str(record.get('Serial_number'))
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
                experiments_dict['target'] = record.get('Target')
                experiments_dict['aliases'] = [experiment_alias]       ## Needs to be of type array
                experiments_dict['description'] = str(record.get('Target')).strip('-human') + ' ChIP-seq on human ' + str(record.get('Cell_line'))
                experiments_dict['documents'] = ['michael-snyder:' + str(record.get('Protocol_documents'))]

                ## Ignore if control
                if record.get('Target') != 'Control-human':
                    array_possible_controls = []
                    tmp_array_controls = possible_control_map[record.get('Cell_line')]
                    for rec in tmp_array_controls:
                        if str(reverse_remove_ab_host_control_map[record.get('Ab host for control')]) in str(rec):
                            array_possible_controls.append(rec)
                        if 'Input' in str(rec):
                            array_possible_controls.append(rec)
                        experiments_dict['possible_controls'] = array_possible_controls
                experiment_check[experiment_alias] = experiments_dict
                response = postObject(experiments_dict)
                if response is not None:
                    try:
                        record['ENCSR_No. '] = response['@graph'][0]['accession']
                        experiments_dict['ENCSR_No. '] = record['ENCSR_No. ']
                        encsr_number = str(experiments_dict['ENCSR_No. '])
                        list_output.append(experiments_dict)
                    except:
                        response_id = getObject(experiment_alias)
                        #response_id = getObject(experiments_dict)
                        encsr_number = str(response_id['accession'])
                        json.dump(response_id, dict_output, indent=4)

            # Register Library
            library_dict = {}
            library_dict['@id'] = 'library/'
            library_dict['biosample'] = record.get('ENCBS_no. ')
            library_dict['nucleic_acid_term_name'] = 'DNA'
            library_dict['nucleic_acid_term_id'] = 'SO:0000352'
            #library_dict['documents'] = need your protocol document
            #library_dict['nucleic_acid_starting_quantity'] = 'Unknown' - Where to get this information
            #library_dict['fragmentation_date'] = Might not need
            library_dict['size_range'] = record.get('Size_range').strip(' bp')
            library_dict['paired_ended'] = True
            library_dict['aliases'] = ['michael-snyder:' + str(record.get('TruSeq_library_name')).strip('# ') + '_' + str(record.get('Truseq_Barcode'))]
            library_dict['lab'] = "michael-snyder"
            library_dict['award'] = "U54HG006996"
            response = postObject(library_dict)
            if response is not None:
                try:
                    record['ENCLB_No. '] = response['@graph'][0]['accession']
                    library_dict['ENCLB_No. '] = record['ENCLB_No. ']
                    enclb_number = str(library_dict['ENCLB_No. '])
                    ist_output.append(library_dict)
                except:
                    response_id = getObject('michael-snyder:' + str(record.get('TruSeq_library_name')).strip('# ') + '_' + str(record.get('Truseq_Barcode')))
                    #response_id = getObject(library_dict)
                    enclb_number = str(response_id['accession'])
                    json.dump(response_id, dict_output, indent=4)

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
            response = postObject(replicates_dict)

            json.dump(list_output, dict_output, indent=4)

            dcc_response = open('response.txt', "a+")
            output_to_file = str(record.get('Serial_number')) + '\t' + enclb_number +'\t' + encsr_number # + '\t' + str(array_possible_controls)
            print output_to_file
            dcc_response.write(output_to_file + '\n')

    dict_output.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', '-i', help="A tab delimited file that needs processing")
    parser.add_argument('--outfile', '-o', help="An output file containing JSON objects to post")
    args = parser.parse_args()

    read_truptis_file(args.infile)

    #Commented out for now to make sure JSON objects are properly created before submitting
