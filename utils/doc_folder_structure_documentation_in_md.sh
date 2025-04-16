#!/bin/bash

# Usage: ./generate-structure-aligned.sh [path] > structure.md
# Default path is current directory
TARGET_DIR="${1:-.}"

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
    local name
    name=$(basename "$file")
    local connector="├──"
    [ "$count" -eq "${#files[@]}" ] && connector="└──"

    local line="${prefix}${connector} $name"
    local comment=""

    if [ -d "$file" ]; then
      # For directories, check for a .doc.md file for a comment.
      local doc_file="$file/.doc.md"
      if [ -f "$doc_file" ]; then
        comment=$(head -n 1 "$doc_file" | sed 's/[[:space:]]*$//')
      fi
      lines+=("$line")
      comments+=("$comment")

      # Recurse into the directory.
      local new_prefix="$prefix"
      if [ "$connector" == "└──" ]; then
        new_prefix+="    "
      else
        new_prefix+="│   "
      fi
      generate_tree "$file" "$new_prefix"

    elif [ -f "$file" ]; then
      # For files, check if the first line is a proper comment.
      # It must start with a comment marker (e.g. '#', '//' or '<!--')
      # followed by whitespace then an asterisk immediately.
      local first_line
      first_line=$(head -n 1 "$file" | sed 's/[[:space:]]*$//')

      if [[ "$first_line" =~ ^[[:space:]]*\#[[:space:]]\*(.*) ]]; then
        comment="${BASH_REMATCH[1]}"
        # Remove only the very last asterisk, if present.
        comment=$(echo "$comment" | sed -E 's/\*$//')
      elif [[ "$first_line" =~ ^[[:space:]]*//[[:space:]]\*(.*) ]]; then
        comment="${BASH_REMATCH[1]}"
        comment=$(echo "$comment" | sed -E 's/\*$//')
      elif [[ "$first_line" =~ ^[[:space:]]*\<\!\-\-[[:space:]]\*(.*) ]]; then
        comment="${BASH_REMATCH[1]}"
        comment=$(echo "$comment" | sed -E 's/\*$//')
      fi

      # Trim any leading whitespace from the extracted comment.
      comment=$(echo "$comment" | sed 's/^[[:space:]]*//')
      lines+=("$line")
      comments+=("$comment")
    fi
  done
}

# Add the target directory as root.
lines+=("$(basename "$TARGET_DIR")/")
comments+=("")
generate_tree "$TARGET_DIR" ""

# Determine the maximum length among all tree lines.
max_length=0
for line in "${lines[@]}"; do
  [ ${#line} -gt $max_length ] && max_length=${#line}
done
# Set dynamic padding: maximum line length + 3.
PADDING=$((max_length + 3))

# Print the tree with comments aligned to the dynamic padding.
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
