# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
from kbase_protein_network_analysis_toolkit.check_existence import ProteinExistenceChecker
from kbase_protein_network_analysis_toolkit.storage import ProteinStorage
#END_HEADER

class kbase_protein_network_analysis_toolkit:
    '''
    Module Name:
    kbase_protein_network_analysis_toolkit

    Module Description:
    A KBase module: kbase_protein_network_analysis_toolkit
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ.get('SDK_CALLBACK_URL')
        if self.callback_url is None:
            raise RuntimeError('SDK_CALLBACK_URL environment variable must be set.')
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s', level=logging.INFO)
        self.storage = ProteinStorage()
        self.checker = ProteinExistenceChecker(storage=self.storage)
        #END_CONSTRUCTOR

    def get_protein_embedding_by_uniprot_id(self, ctx, params):
        #BEGIN get_protein_embedding_by_uniprot_id
        import time
        start_time = time.time()
        protein_id = params.get('protein_id')
        if not protein_id or not isinstance(protein_id, str) or not protein_id.strip():
            return [{
                'exists': False,
                'family_id': None,
                'metadata': None,
                'embedding': None,
                'summary': 'No protein_id provided.',
                'input_parameters': params,
                'start_time': start_time,
                'validation_status': 'error',
                'error': 'Parameter "protein_id" must be a non-empty string.'
            }]
        result = self.checker.check_protein_existence(protein_id)
        embedding = None
        if result['exists']:
            family_id = result['family_id']
            # Find index of protein in family
            embeddings, protein_ids = self.storage.load_family_embeddings(family_id)
            try:
                idx = protein_ids.index(protein_id)
                embedding = embeddings[idx].tolist()
            except Exception:
                embedding = None
        summary = f"Protein {protein_id} existence: {result['exists']}"
        if result['exists']:
            summary += f"; Family: {result['family_id']}"
        return [{
            'exists': result['exists'],
            'family_id': result['family_id'],
            'metadata': result['metadata'],
            'embedding': embedding,
            'summary': summary,
            'input_parameters': params,
            'start_time': start_time,
            'validation_status': 'success' if result['exists'] else 'not_found',
            'error': None if result['exists'] else 'Protein not found.'
        }]
        #END get_protein_embedding_by_uniprot_id
