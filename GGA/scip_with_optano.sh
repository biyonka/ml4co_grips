while getopts ":i:a:" flag
do
    case $flag in
        i) instance="${OPTARG}";;
        a) arguments="${OPTARG}";;
    esac
done
python runOptano.py "$instance" "$arguments"
