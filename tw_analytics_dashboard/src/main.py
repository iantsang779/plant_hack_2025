import argparse
from database import ComparaDB
from query import Query

def parse_args():
    args = argparse.ArgumentParser(prog = 'TW Analytics Dashboard',
                                   description='Argument Parser for TWA Dashboard')

    args.add_argument('-g', '--gene_id', help='Query Gene ID (Ensembl Format)', 
                      type=str, nargs='?', dest='query_gene_id', required=True)
    args.add_argument('-t', '--taxon', help='Taxon relating to the query gene ID.', 
                      type=str, nargs='?', dest='query_taxon', 
                      choices=['fungi', 'plants', 'metazoa', 'protists'], required=True)
    

    return args.parse_args()



def main():
    args = parse_args()
    q = Query()

    db_compara = ComparaDB(args.query_taxon, args.query_gene_id)
    db_compara.determine_database(q.taxon_query())
    res = db_compara.execute_homology_query(q.homology_query())
    

if __name__ == "__main__":
    main()