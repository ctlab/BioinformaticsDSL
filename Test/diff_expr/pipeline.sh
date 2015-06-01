DIR="${BASH_SOURCE%/*}"
. "$DIR/include.sh"

step fastq-dump
try fastq-dump --split-files SRR031714.sra
next

step bowtie
try bowtie-build d_melanogaster_BDGP5.25.62.fa d_melanogaster_BDGP5.25.62
next

#allign reads
if true ; then
step tophat
try tophat --num-threads 4 --mate-inner-dist 200 --output-dir tophat_out d_melanogaster_BDGP5.25.62 SRR031714_1.fastq SRR031714_2.fastq
next


else echo "cant run any implementation of step"; exit 1;
fi
