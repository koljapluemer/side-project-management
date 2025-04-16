#!/bin/bash

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
      # Directory: check for .doc.md
      local doc_file="$file/.doc.md"
      if [ -f "$doc_file" ]; then
        comment=$(head -n 1 "$doc_file" | sed 's/[[:space:]]*$//')
      fi
      lines+=("$line")
      comments+=("$comment")

      # Recurse into directory
      local new_prefix="$prefix"
      if [ "$connector" == "└──" ]; then
        new_prefix+="    "
      else
        new_prefix+="│   "
      fi
      generate_tree "$file" "$new_prefix"

    elif [ -f "$file" ]; then
      # File: check first line for a recognizable comment
      local first_line
      first_line=$(head -n 1 "$file" | sed 's/[[:space:]]*$//')
      if [[ "$first_line" =~ ^[[:space:]]*# ]]; then
        comment="${first_line#\#}"
      elif [[ "$first_line" =~ ^[[:space:]]*// ]]; then
        comment="${first_line#//}"
      elif [[ "$first_line" =~ ^[[:space:]]*\<\!\-\- ]]; then
        comment=$(echo "$first_line" | sed -E 's/<!--(.*)-->/\1/')
      fi
      comment=$(echo "$comment" | sed 's/^[[:space:]]*//')  # Trim leading whitespace
      lines+=("$line")
      comments+=("$comment")
    fi
  done
}

lines+=("$(basename "$TARGET_DIR")/")
comments+=("")
generate_tree "$TARGET_DIR" ""

# Output
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
