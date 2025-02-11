#!/bin/bash -ex

OUTPUT_DIR="compressed_output"
RESULTS_DIR="benchmark_results"
RESULTS_FILE="$RESULTS_DIR/decompression_results.json"
FILES=("model.enet.intgemm.alphas.bin" "model.jaen.intgemm.alphas.bin")
LEVELS=(1 3 9)
ZSTD_LEVELS=(1 5 19)

mkdir -p "$RESULTS_DIR"
COMMANDS=()

for file in "${FILES[@]}"; do
    for level in "${LEVELS[@]}"; do
        COMMANDS+=("bzip2 -d -c $OUTPUT_DIR/${file}.bz2.$level > /dev/null")
        COMMANDS+=("xz -d -c $OUTPUT_DIR/${file}.xz.$level > /dev/null")
        COMMANDS+=("unzip -p $OUTPUT_DIR/${file}.zip.$level > /dev/null")
        COMMANDS+=("lz4 -d -c $OUTPUT_DIR/${file}.lz4.$level > /dev/null")
        COMMANDS+=("brotli -f -d -k $OUTPUT_DIR/${file}.$level.br > /dev/null")
    done

    for level in "${ZSTD_LEVELS[@]}"; do
        COMMANDS+=("zstd -d -c $OUTPUT_DIR/${file}.zst.$level > /dev/null")
    done
done

hyperfine --export-json "$RESULTS_FILE" "${COMMANDS[@]}"

