#transform sam reads into fasq format
fastq-dump SRR031714.sra
#build reference genome index
bowtie-build d_melanogaster_BDGP5.25.62.fa d_melanogaster_BDGP5.25.62
#allign reads
if hash tophat 2> /dev/null ; then
tophat --output-dir tophat_out d_melanogaster_BDGP5.25.62 SRR031714_1.fastq SRR031714_2.fastq
;
else echo "cant run any implementation of step"; exit 1;
fi
