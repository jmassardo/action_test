#!/usr/bin/awk -f
# Set the input and output field separators to newline characters
BEGIN {
    FS="\n"
    RS="\n"
    OFS="\n"
}
# If processing the first input file (urls.txt), read the URLs into the urls array
FNR==NR {
    urls[FNR] = $0
    next
}
# If processing the second input file (pr-body-orig.txt), iterate over each line
{
    # For each URL in the urls array, check if the current line matches the format of a markdown checklist item
    for (i in urls) {
        if ($0 ~ /^\s*-\s*\[[ x]\]\s*.*/) {
            # If the line matches the format of a markdown checklist item, construct a hyperlink using the corresponding URL
            # and replace the text of the checklist item with the hyperlink using the gensub function
            $0 = gensub(/^\s*-\s*\[[ x]\]\s*(.*)$/, "- [ ] [\\1](\"" urls[i] "\")", "")
            break
        }
    }
    # Append the modified line to the output variable
    output = output $0 ORS
}
# Remove the extra newline at the end of the output variable and print the output
END {
    sub(/\n$/, "", output)
    print output
}
