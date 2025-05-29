class Query:
    def __init__(self):
        pass
    
    def taxon_query(self) -> str:
        query = '''
                show databases like 'ensembl_compara%';                
                '''
        return query

    def homology_query(self) -> str:
        query = """         
            SELECT
                gm1.stable_id,
                hm1.perc_id,
                h.description,
                gm2.stable_id,
                gdb2.name,
                hm2.perc_id,
                s1.sequence,
                s2.sequence,
                hm2.cigar_line
            FROM
                homology h 
                JOIN (homology_member hm1 JOIN gene_member gm1 USING (gene_member_id)
                JOIN genome_db gdb1 USING (genome_db_id)
                JOIN seq_member sm1 USING (seq_member_id)
                JOIN sequence s1 USING (sequence_id))USING (homology_id)
                JOIN (homology_member hm2 
                JOIN gene_member gm2 USING (gene_member_id)
                JOIN genome_db gdb2 USING (genome_db_id)
                JOIN seq_member sm2 USING (seq_member_id) 
                JOIN sequence s2 USING (sequence_id))
                USING (homology_id)
            WHERE gm1.gene_member_id != gm2.gene_member_id
            AND gm1.stable_id = %s;"""
        return query