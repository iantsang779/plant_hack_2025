import re

class ReconstructFromCIGAR:
    def __init__(self, reference:str, target:str, cigar:str) -> None:
        self.reference = reference
        self.target = target
        self.cigar = cigar
        self.cigar_split_pairs = None
        self.start_pos, self.end_pos = 0, 0 # start and end pos for slicing the input sequences
        self.global_gap_target, self.global_gap_ref = 0,0 # global number of gaps in target and ref seq
        self.gap_target, self.gap_reference = 0, 0 # local number of gaps in target and ref seq (per iteration over parsed cigar line)
        self.target_seq_full, self.ref_seq_full = [], []

    def parse_cigar_line(self) -> None:
        """ 
        Split cigar line into nested list
        """
        cigar_split = re.findall('\d+|\D+', self.cigar)
        self.cigar_split_pairs = [cigar_split[i:i+2] for i in range(0, len(cigar_split), 2)]
        

    def add_seq_gaps(self, gap_target, gap_reference) -> tuple[str, str]:
        """
        Adjust indexes for list slicing of sequences if gaps ('-') are present in the alignment 
        Return strings of target and reference sequence for each corresponding section in the CIGAR line
        """
        if gap_target > 0:
            target_seq = f'{self.target[self.start_pos-self.global_gap_target:self.end_pos-self.global_gap_target]}'
        else:
            target_seq = f'{self.target[self.start_pos:self.end_pos]}'
        
        if gap_reference > 0:
            ref_seq = f'{self.reference[self.start_pos-self.global_gap_ref:self.end_pos-self.global_gap_ref]}'
        else:
            ref_seq = f'{self.reference[self.start_pos:self.end_pos]}'

        return target_seq, ref_seq
    
    def reconstruct_alignment(self):
        """
        Iterate over cigar line and construct alignment based on each key value pair generated in parse_cigar_line
        """
        
        self.parse_cigar_line()

        for pair in self.cigar_split_pairs:
            gap_target, gap_reference = 0,0
            key, length  = pair[0], pair[1]
            length = int(length)
            
            if key == 'M': # match between reference and target
                self.start_pos = self.end_pos if self.end_pos != 0 else 0
                self.end_pos = self.start_pos + length 
                target_seq, ref_seq = self.add_seq_gaps(gap_target, gap_reference)

                self.ref_seq_full.append(ref_seq)
                self.target_seq_full.append(target_seq)
                

            elif key == 'D': # gap inserted into target sequence
                self.start_pos = self.end_pos 
                self.end_pos = self.start_pos + length 

                dashes = '-' * length
                self.global_gap_target += len(dashes)
                gap_target = len(dashes)

                _, ref_seq = self.add_seq_gaps(gap_target, gap_reference)

                self.ref_seq_full.append(ref_seq)
                self.target_seq_full.append(f'{dashes}') # add dashes to target
               
            
            elif key == 'I': # gap inserted into the reference sequence
                self.start_pos = self.end_pos
                self.end_pos = self.start_pos + length

                dashes = '-' * length
                self.global_gap_ref += len(dashes)     
                gap_reference = len(dashes)

                target_seq, _ = self.add_seq_gaps(gap_target, gap_reference)

                self.ref_seq_full.append(f'{dashes}') # add dashes to reference
                self.target_seq_full.append(target_seq)
        
        print(f'\nReference: {''.join(self.ref_seq_full)}')
        print(f'\nTarget:    {''.join(self.target_seq_full)}')

    
    def combine_sequences(self):
        
