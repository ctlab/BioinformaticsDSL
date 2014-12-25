#transform sam reads into fasq format
fastq-dump SRR031714.sra
#build reference genome index
bowtie-build d_melanogaster_BDGP5.25.62.fa d_melanogaster_BDGP5.25.62
#allign reads
tophat tophat_out d_melanogaster_BDGP5.25.62 SRR031714_1.fastq SRR031714_2.fastq