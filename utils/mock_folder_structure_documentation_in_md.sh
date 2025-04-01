#!/bin/bash

# Usage: ./generate-structure-aligned.sh [path] > structure.md
# Default path is current directory
TARGET_DIR="${1:-.}"
PADDING=50  # Column where the '#' should align

echo "\`\`\`bash"

lines=()

generate_tree() {
  local dir="$1"
  local prefix="$2"
  local files=("$dir"/*)
  local count=0

  for file in "${files[@]}"; do
    ((count++))
    local name=$(basename "$file")
    local connector="├──"
    [ "$count" -eq "${#files[@]}" ] && connector="└──"

    local line="${prefix}${connector} $name"

    lines+=("$line")

    if [ -d "$file" ]; then
      local new_prefix="$prefix"
      if [ "$connector" == "└──" ]; then
        new_prefix+="    "
      else
        new_prefix+="│   "
      fi
      generate_tree "$file" "$new_prefix"
    fi
  done
}

lines+=("$(basename "$TARGET_DIR")/")
generate_tree "$TARGET_DIR" ""

# Print all lines with `#` aligned at $PADDING
for line in "${lines[@]}"; do
  printf "%s%*s#\n" "$line" $((PADDING - ${#line})) ""
done

echo "\`\`\`"
