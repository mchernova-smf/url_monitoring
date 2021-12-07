
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -c|--conf_file) conf_file="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

python3 main_monitor.py --url "$conf_file"
python3 main_dashboard.py
