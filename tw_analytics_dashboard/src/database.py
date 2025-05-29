import MySQLdb
import pandas as pd

class ComparaDB:
    def __init__(self, taxon: str, gene: str):
        self.host = 'mysql-eg-publicsql.ebi.ac.uk'
        self.port= 4157
        self.user = 'anonymous'
        self.gene = gene
        self.taxon = taxon
        self.database = 'ensembl_compara_plants_61_114' # set default schema
        self.db = MySQLdb.connect(host=self.host,
                                 port=self.port,
                                 user=self.user,
                                 database=self.database)
        self.cursor = self.db.cursor()
        self.res = None
        self.df = None
        self.ref_seq = None

    def determine_database(self, query: str) -> None:
        """
        Connect to relevant database and ensure connection to the newest schema
        """
        self.cursor.execute(query)       
        res = self.cursor.fetchall() # fetch all schemas
        self.database = [i[0] for i in res if i[0].split('_')[2] == self.taxon][-1] # filter schema name by taxon and get the most up to date schema
        
        # update connection
        self.db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, database=self.database)
        self.cursor = self.db.cursor()

    def execute_homology_query(self, query: str) -> tuple[str, str, str]:
        """
        Fetch orthologs/paralogs/homologs for input gene id
        """
        self.cursor.execute(query, (self.gene,))

        self.res = self.cursor.fetchall()
        cols = ['Input_Gene_ID',
                'Query_ID%',
                'Type',
                'Homology_Gene_ID',
                'Species_Name',
                'Target_ID%',
                'Reference_Sequence',
                'Query_Sequence',
                'Cigar_Line']
        self.df = pd.DataFrame(list(self.res), columns=[cols])
        ref_seq = self.res[0][6]
        print(self.res[0])
        query_seq = [i[7] for i in self.res]
        cigar = [i[8] for i in self.res]

        return ref_seq, query_seq, cigar

    




