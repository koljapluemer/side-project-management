#!/bin/bash

# Usage: ./generate-structure-aligned.sh [path] > structure.md
# Default path is the current directory.
TARGET_DIR="${1:-.}"

echo "\`\`\`bash"

lines=()
comments=()

# Helper function to check if a file or directory is ignored by Git.
is_ignored() {
  # Only if git is available and we're in a Git working tree.
  if command -v git >/dev/null && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if git check-ignore -q "$1"; then
      return 0  # The file is ignored.
    fi
  fi
  return 1  # Not ignored.
}

generate_tree() {
  local dir="$1"
  local prefix="$2"
  # Expand directory contents (suppress error if directory is empty).
  local files=("$dir"/*)
  local count=0

  for file in "${files[@]}"; do
    # Skip the file/directory if it is ignored by Git.
    if is_ignored "$file"; then
      continue
    fi

    ((count++))
    local name
    name=$(basename "$file")
    local connector="├──"
    [ "$count" -eq "${#files[@]}" ] && connector="└──"
    local line="${prefix}${connector} $name"
    local comment=""

    if [ -d "$file" ]; then
      # For directories, check for a .doc.md file to extract its first-line comment.
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
      # Process files only if the first line qualifies as documentation.
      local first_line
      first_line=$(head -n 1 "$file" | sed 's/[[:space:]]*$//')
      
      # Check for a valid comment: comment marker, whitespace, then an asterisk immediately.
      if [[ "$first_line" =~ ^[[:space:]]*\#[[:space:]]\*(.*) ]]; then
        comment="${BASH_REMATCH[1]}"
        comment=$(echo "$comment" | sed -E 's/\*$//')
      elif [[ "$first_line" =~ ^[[:space:]]*//[[:space:]]\*(.*) ]]; then
        comment="${BASH_REMATCH[1]}"
        comment=$(echo "$comment" | sed -E 's/\*$//')
      elif [[ "$first_line" =~ ^[[:space:]]*\<\!\-\-[[:space:]]\*(.*) ]]; then
        comment="${BASH_REMATCH[1]}"
        comment=$(echo "$comment" | sed -E 's/\*$//')
      fi
      
      # Remove any leading whitespace from the extracted comment.
      comment=$(echo "$comment" | sed 's/^[[:space:]]*//')
      
      # Skip adding this file if no valid documentation comment was extracted.
      if [ -z "$comment" ]; then
        continue
      fi

      lines+=("$line")
      comments+=("$comment")
    fi
  done
}

# Add the target directory as the root node.
lines+=("$(basename "$TARGET_DIR")/")
comments+=("")
generate_tree "$TARGET_DIR" ""

# Determine the maximum length among all tree lines to compute dynamic padding.
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
