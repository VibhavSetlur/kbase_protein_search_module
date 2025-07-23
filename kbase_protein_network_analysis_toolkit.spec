/*
A KBase module: kbase_protein_network_analysis_toolkit
*/

module kbase_protein_network_analysis_toolkit {
    /*
        Output structure for get_protein_embedding_by_uniprot_id.
    */
    typedef structure {
        int exists;
        string family_id;
        mapping<string, UnspecifiedObject> metadata;
        list<float> embedding;
        string summary;
        mapping<string, UnspecifiedObject> input_parameters;
        float start_time;
        string validation_status;
        string error;
    } GetProteinEmbeddingByUniprotIdResults;

    /*
        Get protein embedding and metadata by UniProt ID.
    */
    funcdef get_protein_embedding_by_uniprot_id(mapping<string, UnspecifiedObject> params) returns (GetProteinEmbeddingByUniprotIdResults output) authentication required;
};
