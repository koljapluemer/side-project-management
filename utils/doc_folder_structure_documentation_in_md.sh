#!/bin/bash

# similar to mock_folder_structure_documentation_in_md.sh, only this one takes into account .doc.md

# Usage: ./generate-structure-aligned.sh [path] > structure.md
# Default path is current directory
TARGET_DIR="${1:-.}"
PADDING=50  # Column where the '#' should align

echo "\`\`\`bash"

lines=()
comments=()

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
    local comment=""

    if [ -d "$file" ]; then
      # If directory has a .doc.md file, get the first line
      local doc_file="$file/.doc.md"
      if [ -f "$doc_file" ]; then
        comment=$(head -n 1 "$doc_file" | sed 's/[[:space:]]*$//')  # Trim trailing whitespace
      fi
      local new_prefix="$prefix"
      if [ "$connector" == "└──" ]; then
        new_prefix+="    "
      else
        new_prefix+="│   "
      fi
      generate_tree "$file" "$new_prefix"
    fi

    lines+=("$line")
    comments+=("$comment")
  done
}

lines+=("$(basename "$TARGET_DIR")/")
comments+=("")  # Root directory has no comment
generate_tree "$TARGET_DIR" ""

# Print all lines with `#` aligned at $PADDING
for i in "${!lines[@]}"; do
  line="${lines[$i]}"
  comment="${comments[$i]}"
  if [ -n "$comment" ]; then
    printf "%s%*s# %s\n" "$line" $((PADDING - ${#line})) "" "$comment"
  else
    printf "%s\n" "$line"
  fi
done


echo "\`\`\`"
