# Script to submit excel objects

import csv
import sys
import json
import requests
import argparse

biosample_term_id = ""
source = ""
product_id = ""
protocol_documents = []
donor_id = ""
biosample_type = ""
biosample_term_name = ""
possible_controls = []
award = "U54HG006996"
lab = "michael-snyder"

biosample_term_name_to_function_map = dict({
    "A549" : "A549",
    "GM12878" : "GM12878",
    "HeLa-S3" : "HeLaS3",
    "IMR90" : "IMR90",
    "K562" : "K562",
    "MCF-7" : "MCF7",
    "SK-N-SH" : "SKNSH",
    "HepG2" : "HepG2",
    "Neural Cell" : "Neural_Cell",
    "H1-hES" : "H1HESC"
    })

antibody_source_map = dict({
    "Abcam" : "abcam",
    "Novus" : "novus",
    "Santa Cruz Biotech" : "santa-cruz-biotech",
    "Sigma" : "sigma"
    })
antibody_host_organism_map = dict ({
    "Rabbit" : "rabbit",
    "Mouse" : "mouse",
    "Goat" : "goat"
    })

def A549():
    global biosample_term_id
    global source
    global product_id
    global protocol_documents
    global donor_id
    global biosample_type
    global biosample_term_name
    global possible_controls

    biosample_term_id = "EFO:0001086"
    source = "atcc"
    product_id = "CCL-185"
    protocol_documents = ["michael-snyder:Snyder_A549_Cell_Growth_Protocol"]
    donor_id = "encode:donor of A549"
    biosample_type = "immortalized cell line"
    biosample_term_name = "A549"
    possible_controls = []
    pass

def GM12878():
    global biosample_term_id
    global source
    global product_id
    global protocol_documents
    global donor_id
    global biosample_type
    global biosample_term_name
    global possible_controls

    biosample_term_id = "EFO:0002784"
    source = "coriell"
    product_id = "GM12878"
    protocol_documents = ["michael-snyder:Snyder_GM12878_Cell_Growth_Protocol"]
    donor_id = "encode:donor_of_GM12878"
    biosample_type = "immortalized cell line"
    biosample_term_name = "GM12878"
    possible_controls = ["michael-snyder:GM12878-Rabbit_IgG", "michael-snyder:GM12878-Input_GM12878"]
    pass

def HeLaS3():
    global biosample_term_id
    global source
    global product_id
    global protocol_documents
    global donor_id
    global biosample_type
    global biosample_term_name
    global possible_controls

    biosample_term_id = "EFO:0002791"
    source = "atcc"
    product_id = "CCL-2.2"
    protocol_documents = ["michael-snyder:Snyder_HeLa_S3_Spinner_Flask_Growth_Protocol"]
    donor_id = "encode:donor of HeLa-S3"
    biosample_type = "immortalized cell line"
    biosample_term_name = "HeLa-S3"
    possible_controls = ["michael-snyder:HeLa-S3-Rabbit_IgG", "michael-snyder:HeLa-S3-Input_HelaS3"]
    pass

def IMR90():
    global biosample_term_id
    global source
    global product_id
    global protocol_documents
    global donor_id
    global biosample_type
    global biosample_term_name
    global possible_controls

    biosample_term_id = "EFO:0001196"
    source = "atcc"
    product_id = "CCL-186"
    protocol_documents = ["michael-snyder:Snyder_IMR90_Cell_Growth_Protocol"]
    donor_id = "encode:donor of IMR-90"
    biosample_type = "immortalized cell line"
    biosample_term_name = "IMR90"
    possible_controls = []
    pass

def K562():
    global biosample_term_id
    global source
    global product_id
    global protocol_documents
    global donor_id
    global biosample_type
    global biosample_term_name
    global possible_controls

    biosample_term_id = "EFO:0002067"
    source = "atcc"
    product_id = "CCL-243"
    protocol_documents = ["michael-snyder:Snyder_K562_Cell_Growth_Protocol"]
    donor_id = "encode:donor of K562"
    biosample_type = "immortalized cell line"
    biosample_term_name = "K562"
    possible_controls = ["michael-snyder:K562-Rabbit_IgG", "michael-snyder:K562-Input_K562"]
    pass

def MCF7():
    global biosample_term_id
    global source
    global product_id
    global protocol_documents
    global donor_id
    global biosample_type
    global biosample_term_name
    global possible_controls

    biosample_term_id = "EFO:0001203"
    source = "atcc"
    product_id = "HTB-22"
    protocol_documents = ["michael-snyder:Snyder_MCF7_Cell_Growth_Protocol"]
    donor_id = "encode:donor of MCF-7"
    biosample_type = "immortalized cell line"
    biosample_term_name = "MCF-7"
    possible_controls = ["michael-snyder:MCF-7-Mouse_IgG" , "michael-snyder:MCF-7-Rabbit_IgG", "michael-snyder:MCF-7-Input_MCF7"]
    pass

def SKNSH():
    global biosample_term_id
    global source
    global product_id
    global protocol_documents
    global donor_id
    global biosample_type
    global biosample_term_name
    global possible_controls

    biosample_term_id = "EFO:0003072"
    source = "atcc"
    product_id = ""
    protocol_documents = []
    donor_id = "encode:donor of SK-N-SH"
    biosample_type = "immortalized cell line"
    biosample_term_name = "SK-N-SH"
    possible_controls = []
    pass

def HepG2():
    global biosample_term_id
    global source
    global product_id
    global protocol_documents
    global donor_id
    global biosample_type
    global biosample_term_name
    global possible_controls

    biosample_term_id = "EFO:0001187"
    source = "atcc"
    product_id = "HB-8065"
    protocol_documents = ["michael-snyder:Snyder_HepG2_Cell_Growth_Protocol"]
    donor_id = "encode:donor of HepG2"
    biosample_type = "immortalized cell line"
    biosample_term_name = "HepG2"
    possible_controls = ["michael-snyder:HepG2-Rabbit_IgG", "michael-snyder:HepG2-Input_HepG2"]
    pass

def Neural_Cell():
    global biosample_term_id
    global source
    global product_id
    global protocol_documents
    global donor_id
    global biosample_type
    global biosample_term_name
    global possible_controls

    biosample_term_id = "CL:0002319"
    source = "cellular-dynamics"
    product_id = ""
    protocol_documents = []
    donor_id = "bradley-bernstein:Donor of H1 cells"
    biosample_type = "primary cell"
    biosample_term_name = "neural_cell"
    possible_controls = []
    pass

def H1HESC():
    global biosample_term_id
    global source
    global product_id
    global protocol_documents
    global donor_id
    global biosample_type
    global biosample_term_name
    global possible_controls

    biosample_term_id = "EFO:0003042"
    source = "cellular-dynamics"
    product_id = ""
    protocol_documents = []
    donor_id = "encode:donor of H1"
    biosample_type = "stem cell"
    biosample_term_name = "H1HESC"
    possible_controls = []
    pass

platform_map = dict({
    "HiSeq 2000": "ENCODE:HiSeq2000",
    "GAIIx": "ENCODE:GAIIx"
    })

## This is reversed because the control that needs to be removed is the opposite when sending to the DCC
##    The possible_control_map should be the opposite 
reverse_remove_ab_host_control_map = dict({
    "R" : "Rabbit_IgG",
    "M" : "Mouse_IgG",
    "G" : "Goat_IgG",
    "" : "Control"
    })

#MODE = 'Production'
MODE = 'Development'
encode_dcc_user = 'dsalins@stanford.edu'

if MODE == 'Production':
    print 'Production'
    #encode_dcc_username = '####'
    #encode_dcc_password = '####'
    #encode_dcc_url = '######'
else:   #Default Development
    print 'Development'


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

def handle_response(response):
    if response['status'] == 'error':
        print response['code']
        print response
    elif response['code'] == 'success':
        print "SUCCESS"

def filter_object(json_object, key):
    json_duplicate = json_object
    json_duplicate.pop(key)
    return json.dumps(json_duplicate)

def postObject(object):
    HEADERS = {'content-type': 'application/json'}

    settings = dict()
    settings['USER'] = encode_dcc_user
    settings['SERVER'] = encode_dcc_url
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
    settings['SERVER'] = encode_dcc_url
    settings['AUTHID'] = encode_dcc_username
    settings['AUTHPW'] = encode_dcc_password

    #object_id = object['@id']
    #post_object = filter_object(object, '@id')
    url = (settings.get('SERVER') + '/' + str(object))  #Object
    authid = settings.get('AUTHID')
    authpw = settings.get('AUTHPW')
    response = requests.get(url, auth=(authid, authpw), headers=HEADERS, data=object)
    #response = requests.patch(url, auth=(authid, authpw), headers=HEADERS, data=object)
    return response.json()

def process_submit_experiments():
# Register experiments

    experiment_check = {}
    print 'Processing ID: ' + str(record.get('Serial_number')).strip()
    experiment_alias = 'michael-snyder:' + str(record.get('Cell_line')).strip() + '-' + str(record.get('Factor')).strip()
    if experiment_alias not in experiment_check.keys():
        experiments_dict['@id'] = 'experiment/'
        enclb_number = ''
        encsr_number = ''
        experiments_dict = {}

        get_function_name = biosample_term_name_to_function_map[record.get('Cell Line').strip()]
        getattr(sys.modules[__name__], "%s" % str(get_function_name))()

        experiments_dict['biosample_term_id'] = biosample_term_id
        experiments_dict['biosample_term_name'] = str(record.get('Cell_line')).strip()
        experiments_dict['biosample_type'] = biosample_type
        experiments_dict['assay_term_id'] = "OBI:0000716"
        experiments_dict['assay_term_name'] = "ChIP-seq"
        experiments_dict['lab'] = "michael-snyder"
        experiments_dict['award'] = "U54HG006996"
        experiments_dict['target'] = str(record.get('Target')).strip()
        experiments_dict['aliases'] = [experiment_alias]       ## Needs to be of type array
        experiments_dict['description'] = str(record.get('Target')).strip('-human') + ' ChIP-seq on human ' + str(record.get('Cell_line')).strip()
        experiments_dict['documents'] = ['michael-snyder:' + str(record.get('Protocol_documents')).strip()]

        ## Ignore if control
        if record.get('Target') != 'Control-human':
            array_possible_controls = []
            tmp_array_controls = possible_control_map[record.get('Cell_line').strip()]
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
            list_output.append(library_dict)
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

    return None

def process_submit_library():
    return None

def process_biosamples():
    biosample_count = 0
    encbs_number = ''
    biosample_check = {}
    biosample_dict = {}
    biosample_alias = str(record.get('alias')).strip()
    if biosample_alias not in biosample_check.keys():
        biosample_count =+ 1

        get_function_name = biosample_term_name_to_function_map[record.get('Cell Line').strip()]
        getattr(sys.modules[__name__], "%s" % str(get_function_name))()

        #if (record.get('ENCBS accession').strip()) != "":
        #    biosample_dict['@id'] = record.get('ENCBS accession').strip()
        #else:
        biosample_dict['@id'] = "biosample/"
        biosample_dict['aliases'] = [str(biosample_alias.strip())]
        biosample_dict['award'] = award
        biosample_dict['lab'] = lab
        biosample_dict['source'] = source
        biosample_dict['product_id'] = product_id
        biosample_dict['organism'] = "human"
        biosample_dict['biosample_term_id'] = biosample_term_id
        biosample_dict['biosample_type'] = biosample_type
        biosample_dict['biosample_term_name'] = biosample_term_name
        biosample_dict['protocol_documents'] = protocol_documents
        biosample_dict['culture_harvest_date'] = str(record.get('Cross link Date')).strip()
        biosample_dict['donor'] = donor_id

        biosample_check[biosample_alias] = biosample_dict
        response = postObject(biosample_dict)
        #if (record.get('ENCBS accession').strip()) != "":
        #    print "Patching"
        #    response = getObject(biosample_dict)
        #print response
        if response is not None:
            try:
                record['ENCBS_No. '] = response['@graph'][0]['accession']
                library_dict['ENCBS_No. '] = record['ENCBS_No. ']
                encbs_number = str(library_dict['ENCBS_No. '])
                list_output.append(library_dict)
            except:
                response_id = getObject(biosample_alias)
                encbs_number = str(response_id['accession'])
                json.dump(response_id, dict_output, indent=4)
    return None

def process_antibody():
    encab_number = ''
    antibody_count = 0

    list_output = []
    for record in record_values:
        antibody_check = {}
        antibody_dict = {}
        antibody_alias = 'michael-snyder:' + str(record.get('Target')).strip() + '_' + str(record.get('Product ID')).strip() + '_' + str(record.get('Lot ID')).strip()
        if antibody_alias not in antibody_check.keys():
            antibody_count =+ 1

            antibody_dict['@id'] = "antibody-lots/"
            antibody_dict['aliases'] = [antibody_alias]
            antibody_dict['award'] = award
            antibody_dict['lab'] = lab
            antibody_dict['source'] = antibody_source_map[str(record.get('Source')).strip()]
            antibody_dict['product_id'] = str(record.get('Product ID')).strip()
            antibody_dict['lot_id'] = str(record.get('Lot ID')).strip()
            antibody_dict['host_organism'] = antibody_host_organism_map[str(record.get('Host Organism')).strip()]
            #antibody_dict['target'] = str(record.get('Target')).strip()

            antibody_check[antibody_alias] = antibody_dict
            response = postObject(antibody_dict)
            if response is not None:
                try:
                    record['ENCAB_No. '] = response['@graph'][0]['accession']
                    library_dict['ENCAB_No. '] = record['ENCAB_No. ']
                    encab_number = str(library_dict['ENCAB_No. '])
                    list_output.append(library_dict)
                except:
                    response_id = getObject(antibody_alias)
                    encab_number = str(response_id['accession'])
                    json.dump(response_id, dict_output, indent=4)

        dcc_response = open('response.txt', "a+")
#            output_to_file = str(record.get('Serial_number')) + '\t' + enclb_number +'\t' + encsr_number # + '\t' + str(array_possible_controls)
        output_to_file = str(antibody_count) + '\t' + str(encab_number)
        print output_to_file
        dcc_response.write(output_to_file + '\n')


def submit_excel_file(infile):
    value_list = open(infile, "rU")
    record_values = csv.DictReader(value_list, delimiter='\t')
    dict_output = open(args.outfile, "w")
    enclb_number = ''
    encsr_number = ''
    experiment_check = {}
    list_output = []
    for record in record_values:
        #print 'Processing ID: ' + str(record.get('Serial number')).strip()
        get_function_name = biosample_term_name_to_function_map[record.get('Cell Line').strip()]
        getattr(sys.modules[__name__], "%s" % str(get_function_name))()
        experiment_alias = 'michael-snyder:' + biosample_term_name + '-' + str(record.get('Factor')).strip()
        if experiment_alias not in experiment_check.keys():
            enclb_number = ''
            encsr_number = ''

            experiments_dict = {}
            experiments_dict['@id'] = 'experiment/'
            experiments_dict['biosample_term_id'] = biosample_term_id
            experiments_dict['biosample_term_name'] = str(record.get('Cell Line')).strip()
            experiments_dict['biosample_type'] = biosample_type
            experiments_dict['assay_term_id'] = "OBI:0000716"
            experiments_dict['assay_term_name'] = "ChIP-seq"
            experiments_dict['lab'] = "michael-snyder"
            experiments_dict['award'] = "U54HG006996"
            experiments_dict['target'] = str(record.get('Target')).strip()
            experiments_dict['aliases'] = [experiment_alias]       ## Needs to be of type array
            experiments_dict['description'] = str(record.get('Target')).strip('-human') + ' ChIP-seq on human ' + str(record.get('Cell Line')).strip()
            experiments_dict['documents'] = ['michael-snyder:' + str(record.get('Protocol documents')).strip()]

            ## Ignore if control
            if record.get('Target') != 'Control-human':
                array_possible_controls = []
                tmp_array_controls = possible_controls
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
                    encsr_number = str(response_id['accession'])
                    # json.dump(response_id, dict_output, indent=4)

        # Register Library
        library_dict = {}
        library_dict['@id'] = 'library/'
        library_dict['biosample'] = record.get('ENCBS No. ')
        library_dict['nucleic_acid_term_name'] = 'DNA'
        library_dict['nucleic_acid_term_id'] = 'SO:0000352'
        #library_dict['documents'] = need your protocol document
        #library_dict['nucleic_acid_starting_quantity'] = 'Unknown' - Where to get this information
        #library_dict['fragmentation_date'] = Might not need
        library_dict['size_range'] = record.get('Size range').strip(' bp')
        library_dict['paired_ended'] = True
        #Use for Multiplexed
        # library_alias = ['michael-snyder:' + str(record.get('TruSeq_library_name')).strip('# ') + '_' + str(record.get('Truseq_Barcode'))]
        library_alias = ['michael-snyder:' + str(record.get('Sample'))]
        library_dict['aliases'] = library_alias
        library_dict['lab'] = "michael-snyder"
        library_dict['award'] = "U54HG006996"
        response = postObject(library_dict)
        if response is not None:
            print response
            try:
                record['ENCLB_No. '] = response['@graph'][0]['accession']
                library_dict['ENCLB_No. '] = record['ENCLB_No. ']
                enclb_number = str(library_dict['ENCLB_No. '])
                list_output.append(library_dict)
            except:
                response_id = getObject(library_alias[0])
                #response_id = getObject(library_dict)
                print response_id
                enclb_number = str(response_id['accession'])
        #        json.dump(response_id, dict_output, indent=4)

        # Register replicates
        replicates_dict = {}
        replicates_dict['@id'] = 'replicate/'
        replicates_dict['antibody'] = record.get('ENCAB No. ')
        replicates_dict['biological_replicate_number'] = int(record.get('Replicate')[-1:])
        replicates_dict['technical_replicate_number'] = 1
        replicates_dict['experiment'] = experiment_alias
        replicates_dict['library'] = library_dict['aliases'][0]
        replicates_dict['platform'] = platform_map["HiSeq 2000"]

        # Parse Flowcell information
        flowcell = {}
        Flow_cell = record.get('Flow Cell')
        flowcell['lane'] = record.get('Lane')
        flowcell['barcode'] = record.get('Truseq Barcode')
        flowcell['machine'] = Flow_cell.split('_', 3)[1]
        flowcell['flowcell'] = Flow_cell.split('_', 3)[2]

        replicates_dict['flowcell_details'] = [flowcell]
        replicates_dict['paired_ended'] = True
        replicates_dict['read_length'] = 100
        replicates_dict['read_length_units'] = 'nt'
        list_output.append(replicates_dict)
        response = postObject(replicates_dict)

        #json.dump(list_output, dict_output, indent=4)

        dcc_response = open('response.txt', "a+")
        output_to_file = str(record.get('Serial number')).strip() + '\t' + enclb_number +'\t' + encsr_number + '\t' #+ str(array_possible_controls)
        print output_to_file
        dcc_response.write(output_to_file + '\n')

        dict_output.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', '-i', help="A tab delimited file that needs processing")
    parser.add_argument('--outfile', '-o', help="An output file containing JSON objects to post")
    parser.add_argument('--mode', '-m', help="Connection Mode default Dev, else --Mode Production")
    args = parser.parse_args()

    MODE = args.mode
    submit_excel_file(args.infile)

