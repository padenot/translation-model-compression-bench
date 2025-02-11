#!/bin/bash

OUTPUT_DIR="compressed_output"
FILES=("model.enet.intgemm.alphas.bin" "model.jaen.intgemm.alphas.bin")
LEVELS=(1 3 9)
ZSTD_LEVELS=(1 5 19)

mkdir -p "$OUTPUT_DIR"

for file in "${FILES[@]}"; do
    for level in "${LEVELS[@]}"; do
        bzip2 -k -z -"$level" -c "$file" > "$OUTPUT_DIR/${file}.bz2.$level"
        xz -k -"$level" -c "$file" > "$OUTPUT_DIR/${file}.xz.$level"
        zip -"$level" "$OUTPUT_DIR/${file}.zip.$level" "$file"
        lz4 -"$level" -c "$file" > "$OUTPUT_DIR/${file}.lz4.$level"
        brotli -"$level" "$file" -o "$OUTPUT_DIR/${file}.brotli.$level"
    done

    for level in "${ZSTD_LEVELS[@]}"; do
        zstd -"$level" -c "$file" > "$OUTPUT_DIR/${file}.zst.$level"
    done
done

